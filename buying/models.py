import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


UUID_LENGTH = 6


def make_uuid():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choices(alphabet, k=UUID_LENGTH))


def create_uuid_field():
    return models.CharField(
        unique=True, default=make_uuid, max_length=UUID_LENGTH)


class Depot(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=400)
    sign_up_secret = models.CharField(
        default=make_uuid, max_length=UUID_LENGTH)

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    depot = models.ForeignKey(
        Depot, related_name='users', on_delete=models.PROTECT,
        null=True, blank=True)
    street = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)


class ItemGroup(models.Model):
    idx = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    depot = models.ForeignKey(
        Depot, models.PROTECT, related_name='items', )

    group = models.ForeignKey(
        ItemGroup, models.PROTECT, related_name='items')
    code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    depot = models.ForeignKey(
        Depot, related_name='invoices', on_delete=models.PROTECT)
    user = models.ForeignKey(
        UserProfile, related_name='invoices', on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def update_amount(self):
        self.amount = sum([p.price * p.quantity for p in self.itempurchases.all()])
        self.save()


class Purchase(models.Model):
    depot = models.ForeignKey(
        Depot, related_name='purchases', on_delete=models.PROTECT)
    user = models.ForeignKey(
        UserProfile, related_name='purchases', on_delete=models.PROTECT)
    datetime = models.DateTimeField(default=timezone.now)
    invoice = models.ForeignKey(
        Invoice, related_name='purchases',
        on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def total_price(self):
        return sum(i.item.price * i.quantity for i in self.items.all())

    def __str__(self):
        return self.datetime.strftime('%Y-%m-%d %H:%M')


class ItemPurchase(models.Model):
    purchase = models.ForeignKey(
        Purchase, related_name='items',
        null=True, blank=True,
        on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    depot = models.ForeignKey(
        Depot, related_name='itempurchases', on_delete=models.PROTECT)
    user = models.ForeignKey(
        UserProfile, related_name='itempurchases', on_delete=models.PROTECT)
    invoice = models.ForeignKey(
        Invoice, related_name='itempurchases',
        on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


    def clean(self):
        print("ItemPurchase clean")
        if self.invoice:
            print(f"itemPurchase invoice set. depot:{self.invoice.depot}, user: {self.invoice.user}")
            self.depot = self.invoice.depot
            self.user = self.invoice.user
        if self.item:
            self.price = self.item.price * self.quantity
        super().clean()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update price on invoice
        if self.invoice:
            self.invoice.update_amount()
