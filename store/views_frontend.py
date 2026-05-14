from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Article, Purchase, ShoppingBasket


@login_required
def home(request):
    return render(request, 'store/home.html')

@login_required
def new_basket(request):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")
    
    # create a new shopping basket for the user
    basket = ShoppingBasket.objects.create(customer=request.user.customer)
    basket.save()
    return HttpResponseRedirect(f'/store/basket/{basket.id}/')

@login_required
def show_basket(request, basket_id):
    basket = ShoppingBasket.objects.get(id=basket_id)
    if basket.customer != request.user.customer:
        return HttpResponseForbidden("You do not have permission to view this basket.")
    
    purchases = basket.purchases.all()
    purchases_total = sum(purchase.total_price for purchase in purchases)
    return render(request, 'store/show_basket.html', {'basket': basket, 'purchases': purchases, 'purchases_count': len(purchases), 'purchases_total': purchases_total})

@login_required
def choose_article(request, basket_id):
    articles = Article.objects.all()
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

    purchase.quantity += delta

    if purchase.quantity < 1:
        purchase.delete()
    else:
        purchase.save()
    return HttpResponseRedirect(f'/store/basket/{purchase.basket.id}/')

@login_required
def finish_basket(request, basket_id):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")
    
    basket = ShoppingBasket.objects.get(id=basket_id)

    # check if basket belongs to user
    if basket.customer != request.user.customer:
        return HttpResponseForbidden("You do not have permission to finish this basket.")

    # here you would typically trigger the checkout process, e.g. by sending a message to a message queue
    # for now, we just mark the basket as finished
    # basket.is_finished = True
    # basket.save()
    return HttpResponseRedirect('/store/')