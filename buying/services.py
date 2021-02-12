from django.db.transaction import atomic

from rest_framework import exceptions

from . import models


@atomic()
def create_purchase(user, purchase_items_data):
    purchase = models.Purchase.objects.create(user=user)

    _create_purchase_items(purchase, purchase_items_data)

    purchase.save()
    return purchase


def _create_purchase_items(purchase, purchase_items_data):
    for purchase_item_data in purchase_items_data:
        item_data = purchase_item_data['item']
        item = _find_item_and_verify_price_or_throw(item_data)

        quantity = purchase_item_data['quantity']
        if item.number_of_items_in_stock < quantity:
            raise exceptions.ValidationError(detail=f'There are only {item.number_of_items_in_stock} items '
                                                    f'"{item.name}" in stock but you requested {quantity}.')

        item.number_of_items_in_stock -= quantity
        item.save()

        purchase_item = purchase.items.create(item=item, quantity=quantity)
        purchase_item.save()


def _find_item_and_verify_price_or_throw(item_data):
    item = _find_item_or_throw(item_data)
    _check_price_or_throw(item, item_data)
    return item


def _check_price_or_throw(item, item_data):
    price = item_data.get('price')
    if price and item.price != price:
        message = f"The price provided ({price}) didn't match the actual price ({item.price}) of \"{item.name}\". " \
                  f"It looks like your local pricing data is stale."

        raise exceptions.ValidationError(detail=message)


def _find_item_or_throw(item_data):
    product_nr = item_data['product_nr']

    items = models.Item.objects.filter(product_nr=product_nr)
    if not items:
        raise exceptions.ValidationError(detail=f"Didn't find any item with `product_nr' {product_nr}")
    item = items.first()

    return item


