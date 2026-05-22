import logging

from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode, urlsafe_base64_encode
from django.utils import timezone
from urllib.parse import urlencode
from . import models
from .models import Article, Purchase, ShoppingBasket
from .invoice_pdf import InvoicePdfRenderer
from .articles_pdf import ArticlesPdfRenderer


logger = logging.getLogger(__name__)


def _build_unique_username_from_email(user_model, email):
    local_part = (email.split('@', 1)[0] or 'user').strip().lower()
    base = ''.join(char if char.isalnum() else '-' for char in local_part).strip('-')
    if not base:
        base = 'user'

    username = base
    suffix = 1
    while user_model.objects.filter(username=username).exists():
        suffix += 1
        username = f'{base}-{suffix}'
    return username


def _get_or_create_login_user_for_email(email):
    user_model = get_user_model()
    user = user_model.objects.filter(
        is_active=True,
        email__iexact=email,
    ).order_by('id').first()
    if user is not None:
        return user

    matching_customers = models.Customer.objects.filter(email__iexact=email)
    unassigned_customers = matching_customers.filter(users__isnull=True).distinct()
    if not unassigned_customers.exists():
        return None

    user = user_model.objects.create_user(
        username=_build_unique_username_from_email(user_model, email),
        email=email,
    )

    # if single customer, assign name to user
    if unassigned_customers.count() == 1:
        customer = unassigned_customers.first()
        first_name, last_name = customer.name.split(' ', 1) if ' ' in customer.name else (customer.name, '')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    for customer in unassigned_customers:
        customer.users.add(user)
    return user


def _get_safe_next_url(request, fallback='/store/'):
    next_url = request.POST.get('next') or request.GET.get('next') or fallback
    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return fallback
    return next_url


def email_login_request(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/store/')

    next_url = _get_safe_next_url(request)
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        user = _get_or_create_login_user_for_email(email)

        if user is not None:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            query_string = urlencode({'next': next_url})
            confirm_url = f'/store/login/confirm/{uidb64}/{token}/?{query_string}'
            confirmation_link = request.build_absolute_uri(confirm_url)

            text_body = (
                'Hallo\n\n'
                'bitte bestätige Deine Anmeldung mit folgendem Link:\n'
                f'{confirmation_link}\n\n'
                'Wenn Du diese Anmeldung nicht angefordert hast, ignoriere diese E-Mail.'
            )
            html_body = (
                '<p>Hallo</p>'
                '<p>bitte bestätige Deine Anmeldung mit folgendem Link:</p>'
                f'<p><a href="{confirmation_link}">{confirmation_link}</a></p>'
                '<p>Wenn Du diese Anmeldung nicht angefordert hast, ignoriere diese E-Mail.</p>'
            )
            msg = EmailMultiAlternatives(
                subject='Depot Commün: Anmeldung bestätigen',
                body=text_body,
                from_email=None,
                to=[user.email],
            )
            msg.attach_alternative(html_body, 'text/html')
            msg.send(fail_silently=False)

        return render(request, 'store/login_email_sent.html', {'email': email})

    return render(request, 'store/login_email.html', {'next': next_url})


def email_login_confirm(request, uidb64, token):
    token_preview = f"{token[:8]}..." if token else "<missing>"
    logger.debug(
        "email_login_confirm called: method=%s path=%s host=%s uidb64=%s token=%s next=%s",
        request.method,
        request.path,
        request.get_host(),
        uidb64,
        token_preview,
        request.GET.get('next'),
    )

    user_model = get_user_model()
    user = None
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=user_id)
        logger.debug(
            "email_login_confirm user resolved: user_id=%s is_active=%s",
            user.id,
            user.is_active,
        )
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        logger.exception(
            "email_login_confirm failed to decode/resolve user: uidb64=%s token=%s",
            uidb64,
            token_preview,
        )
        user = None

    token_valid = user is not None and default_token_generator.check_token(user, token)
    if request.method == 'GET' and user is not None and user.is_active and token_valid:
        logger.info("email_login_confirm token accepted on GET: user_id=%s", user.id)
        return render(
            request,
            'store/login_email_confirm.html',
            {
                'user': user,
                'next': _get_safe_next_url(request),
            },
        )

    if request.method == 'POST' and user is not None and user.is_active and token_valid:
        logger.info("email_login_confirm success: user_id=%s", user.id)
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(_get_safe_next_url(request))

    logger.warning(
        "email_login_confirm rejected: has_user=%s is_active=%s token_valid=%s uidb64=%s token=%s",
        user is not None,
        user.is_active if user is not None else None,
        token_valid,
        uidb64,
        token_preview,
    )
    return render(request, 'store/login_email_invalid.html', status=400)


def _get_selected_customer(request):
    customers = request.user.customers.order_by('name', 'id')
    selected_customer_id = request.session.get('selected_customer_id')

    selected_customer = None
    if selected_customer_id is not None:
        selected_customer = customers.filter(id=selected_customer_id).first()

    if selected_customer is None:
        selected_customer = customers.first()
        if selected_customer is not None:
            request.session['selected_customer_id'] = selected_customer.id

    return selected_customer, customers


@login_required
def home(request):
    selected_customer, customers = _get_selected_customer(request)

    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        customer = customers.filter(id=customer_id).first()
        if customer is None:
            return HttpResponseForbidden("You do not have permission to select this customer.")
        request.session['selected_customer_id'] = customer.id
        return HttpResponseRedirect('/store/')

    open_baskets = ShoppingBasket.objects.filter(
        customer=selected_customer,
        user=request.user,
        completed__isnull=True,
    ).order_by('-date')
    is_staff = request.user.is_staff

    return render(
        request,
        'store/home.html',
        {
            'open_baskets': open_baskets,
            'customers': customers,
            'selected_customer': selected_customer,
            'is_staff': is_staff,
        },
    )


@login_required
def new_basket(request):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    selected_customer, _ = _get_selected_customer(request)
    if selected_customer is None:
        return HttpResponseForbidden("No customer account associated with this user.")

    open_basket = ShoppingBasket.objects.filter(
        customer=selected_customer,
        user=request.user,
        completed__isnull=True,
    ).order_by('-date').first()
    if open_basket is not None:
        return HttpResponseRedirect(f'/store/basket/{open_basket.id}/')

    # create a new shopping basket for the user
    basket = ShoppingBasket.objects.create(customer=selected_customer, user=request.user)
    return HttpResponseRedirect(f'/store/basket/{basket.id}/')


@login_required
def logout_view(request):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    auth_logout(request)
    return HttpResponseRedirect('/store/login/')


@login_required
def edit_profile(request):
    user = request.user
    errors = {}
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        if len(first_name) > 150:
            errors['first_name'] = 'Vorname darf maximal 150 Zeichen enthalten.'
        if len(last_name) > 150:
            errors['last_name'] = 'Nachname darf maximal 150 Zeichen enthalten.'
        if not errors:
            user.first_name = first_name
            user.last_name = last_name
            user.save(update_fields=['first_name', 'last_name'])
            return HttpResponseRedirect('/store/')
    return render(request, 'store/edit_profile.html', {'errors': errors})


@login_required
@require_http_methods(["GET", "POST"])
def customer_page(request):
    selected_customer, _ = _get_selected_customer(request)
    errors = {}

    if not selected_customer:
        return HttpResponseForbidden("Kein Kunde ausgewählt.")

    if request.method == "POST":
        customer_name = request.POST.get('customer_name', '').strip()
        if not customer_name:
            errors['customer_name'] = 'Bitte einen Kundennamen eingeben.'
        elif len(customer_name) > 50:
            errors['customer_name'] = 'Kundenname darf maximal 50 Zeichen enthalten.'
        else:
            selected_customer.name = customer_name
            selected_customer.save(update_fields=['name'])
            return HttpResponseRedirect('/store/customer/')

    users = selected_customer.users.all()
    return render(
        request,
        'store/customer.html',
        {
            'users': users,
            'selected_customer': selected_customer,
            'errors': errors,
        },
    )

@login_required
@require_http_methods(["GET", "POST"])
def add_user(request):
    from .context_processors import selected_customer as get_selected_customer
    ctx = get_selected_customer(request)
    selected_customer = ctx['selected_customer']
    error = None
    if not selected_customer:
        return HttpResponseForbidden("Kein Kunde ausgewählt.")
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        if not email or not first_name or not last_name:
            error = "Bitte alle Felder ausfüllen."
        else:
            User = get_user_model()
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email,
                'first_name': first_name,
                'last_name': last_name,
            })
            if not created:
                user.first_name = first_name
                user.last_name = last_name
                user.save(update_fields=['first_name', 'last_name'])
            selected_customer.users.add(user)
            return HttpResponseRedirect('/store/customer/')
    return render(request, 'store/add_user.html', {'selected_customer': selected_customer, 'error': error})

@login_required
def show_basket(request, basket_id):
    basket = ShoppingBasket.objects.get(id=basket_id)
    if basket.user_id != request.user.id:
        return HttpResponseForbidden("You do not have permission to view this basket.")
    if basket.completed is not None:
        return HttpResponseRedirect('/store/')

    purchases = basket.purchases.all()
    purchases_total = sum(purchase.total_price for purchase in purchases)
    return render(request, 'store/show_basket.html', {'basket': basket, 'purchases': purchases, 'purchases_count': len(purchases), 'purchases_total': purchases_total})


@cache_page(60 * 5)  # cache for 5 minutes, since article data changes rarely
@login_required
def choose_article(request, basket_id):
    basket = ShoppingBasket.objects.get(id=basket_id)
    if basket.user_id != request.user.id:
        return HttpResponseForbidden("You do not have permission to modify this basket.")
    if basket.completed is not None:
        return HttpResponseForbidden("This basket is already completed.")

    articles = Article.objects.filter(active=True).order_by(
        'group__idx',
        'group__name',
        'sortidx',
        'name',
    )
    return render(request, 'store/choose_article.html', {'articles': articles, 'basket_id': basket_id})


@login_required
def create_purchase(request, basket_id, article_id):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    article = Article.objects.get(id=article_id)
    basket = ShoppingBasket.objects.get(id=basket_id)

    # check if basket belongs to user
    if basket.user_id != request.user.id:
        return HttpResponseForbidden("You do not have permission to add to this basket.")
    if basket.completed is not None:
        return HttpResponseForbidden("This basket is already completed.")

    # create new purchase in current shopping basket
    purchase = Purchase.objects.create(
            article=article,
            quantity=1,
            price=article.price,
            customer=basket.customer,
            basket=basket,
    )
    purchase.save()
    return HttpResponseRedirect(f'/store/basket/{basket.id}/')


@login_required
def inc_quantity(request, purchase_id):
    return inc_dec_quantity(request, purchase_id, 1)


@login_required
def dec_quantity(request, purchase_id):
    return inc_dec_quantity(request, purchase_id, -1)


@login_required
def delete_purchase(request, purchase_id):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    purchase = Purchase.objects.get(id=purchase_id)

    # check if purchase belongs to user
    if purchase.basket is None or purchase.basket.user_id != request.user.id:
        return HttpResponseForbidden("You do not have permission to edit this purchase.")
    if purchase.basket.completed is not None:
        return HttpResponseForbidden("This basket is already completed.")

    basket_id = purchase.basket.id
    purchase.delete()
    return HttpResponseRedirect(f'/store/basket/{basket_id}/')


def inc_dec_quantity(request, purchase_id, delta):
    """
    Helper function to increase or decrease the quantity of a purchase.
    """
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    purchase = Purchase.objects.get(id=purchase_id)

    # check if purchase belongs to user
    if purchase.basket is None or purchase.basket.user_id != request.user.id:
        return HttpResponseForbidden("You do not have permission to edit this purchase.")
    if purchase.basket.completed is not None:
        return HttpResponseForbidden("This basket is already completed.")

    purchase.quantity += delta

    if purchase.quantity < 1:
        purchase.delete()
    else:
        purchase.save()

    # no redirect after post for better UX - just show updated basket
    return show_basket(request, purchase.basket.id)


@login_required
def finish_basket(request, basket_id):
    basket = ShoppingBasket.objects.get(id=basket_id)

    # check if basket belongs to user
    if basket.user_id != request.user.id:
        return HttpResponseForbidden("You do not have permission to finish this basket.")
    if basket.completed is not None:
        return HttpResponseRedirect('/store/')

    purchases = basket.purchases.all()
    purchases_total = sum(purchase.total_price for purchase in purchases)

    if request.method == 'GET':
        return render(
            request,
            'store/confirm_finish_basket.html',
            {
                'basket': basket,
                'purchases': purchases,
                'purchases_count': len(purchases),
                'purchases_total': purchases_total,
            },
        )

    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    action = request.POST.get('action')
    if action == 'cancel':
        return HttpResponseRedirect(f'/store/basket/{basket.id}/')

    if action == 'delete':
        basket.delete()
        return HttpResponseRedirect('/store/')

    if action != 'confirm':
        return HttpResponseForbidden("Invalid finish action.")

    basket.completed = timezone.now()
    basket.save(update_fields=['completed'])
    return HttpResponseRedirect('/store/')

@permission_required('store.view_invoice', raise_exception=True)
def invoice_pdf(request, id):
    invoice = get_object_or_404(models.Invoice, pk=id)

    filename = "DC Rechnung %d.pdf" % invoice.id
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = \
        f'attachment; filename="{filename}"'

    InvoicePdfRenderer().render(invoice, response)
    return response


@permission_required('store.view_article', raise_exception=True)
def articles_pdf(request):
    """
    generate pdf of all active articles.
    """
    articles = models.Article.objects.filter(active=True)

    filename = "Artikel Liste.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = \
        f'attachment; filename="{filename}"'

    ArticlesPdfRenderer().render(articles, response)
    return response

