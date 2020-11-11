from django.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    number_of_items_in_stock = models.PositiveSmallIntegerField(default=0)
    active_from = models.DateTimeField(default=timezone.now)
    active_until = models.DateTimeField(blank=True, null=True)


class Purchase(models.Model):
    datetime = models.DateTimeField(default=timezone.now)


class ItemPurchase(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2)



