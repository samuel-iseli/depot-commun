from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from . import models
from .models import Article, Purchase, ShoppingBasket
from .invoice_pdf import InvoicePdfRenderer
from .articles_pdf import ArticlesPdfRenderer


@login_required
def home(request):
    open_baskets = ShoppingBasket.objects.filter(
        customer=request.user.customer,
        completed__isnull=True,
    ).order_by('-date')
    return render(request, 'store/home.html', {'open_baskets': open_baskets})


@login_required
def new_basket(request):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    open_basket = ShoppingBasket.objects.filter(
        customer=request.user.customer,
        completed__isnull=True,
    ).order_by('-date').first()
    if open_basket is not None:
        return HttpResponseRedirect(f'/store/basket/{open_basket.id}/')

    # create a new shopping basket for the user
    basket = ShoppingBasket.objects.create(customer=request.user.customer)
    basket.save()
    return HttpResponseRedirect(f'/store/basket/{basket.id}/')


@login_required
def show_basket(request, basket_id):
    basket = ShoppingBasket.objects.get(id=basket_id)
    if basket.customer != request.user.customer:
        return HttpResponseForbidden("You do not have permission to view this basket.")
    if basket.completed is not None:
        return HttpResponseRedirect('/store/')

    purchases = basket.purchases.all()
    purchases_total = sum(purchase.total_price for purchase in purchases)
    return render(request, 'store/show_basket.html', {'basket': basket, 'purchases': purchases, 'purchases_count': len(purchases), 'purchases_total': purchases_total})


@login_required
def choose_article(request, basket_id):
    basket = ShoppingBasket.objects.get(id=basket_id)
    if basket.customer != request.user.customer:
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
    if basket.customer != request.user.customer:
        return HttpResponseForbidden("You do not have permission to add to this basket.")
    if basket.completed is not None:
        return HttpResponseForbidden("This basket is already completed.")

    # create new purchase in current shopping basket
    purchase = Purchase.objects.create(
            article=article,
            quantity=1,
            price=article.price,
            customer=request.user.customer,
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
    if purchase.customer != request.user.customer:
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
    if purchase.customer != request.user.customer:
        return HttpResponseForbidden("You do not have permission to edit this purchase.")
    if purchase.basket.completed is not None:
        return HttpResponseForbidden("This basket is already completed.")

    purchase.quantity += delta

    if purchase.quantity < 1:
        purchase.delete()
    else:
        purchase.save()
    return HttpResponseRedirect(f'/store/basket/{purchase.basket.id}/')


@login_required
def finish_basket(request, basket_id):
    basket = ShoppingBasket.objects.get(id=basket_id)

    # check if basket belongs to user
    if basket.customer != request.user.customer:
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

