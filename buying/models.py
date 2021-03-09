import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

from django.contrib.auth.models import AbstractUser


UUID_LENGTH = 6


def make_uuid():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choices(alphabet, k=UUID_LENGTH))


def create_uuid_field():
    return models.CharField(unique=True, default=make_uuid, max_length=UUID_LENGTH)


class UserProfile(AbstractUser):
    uuid = create_uuid_field()


class Depot(models.Model):
    uuid = create_uuid_field()
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=400)
    sign_up_secret = models.CharField(default=make_uuid, max_length=UUID_LENGTH)
    users = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    product_nr = models.PositiveSmallIntegerField(unique=True)

    depot = models.ForeignKey(Depot, related_name='items', on_delete=models.PROTECT)

    name = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    tags = models.ManyToManyField(Tag, related_name='items', blank=True)

    number_of_items_in_stock = models.PositiveSmallIntegerField(default=0)

    active_from = models.DateTimeField(default=timezone.now)
    active_until = models.DateTimeField(blank=True, null=True)

    @property
    def is_active(self):
        now = timezone.now()
        return self.active_from <= now <= self.active_until

    def __str__(self):
        return f"{self.product_nr} - {self.name}: {self.price} ({self.number_of_items_in_stock})"


class Purchase(models.Model):
    uuid = create_uuid_field()
    user = models.ForeignKey(UserProfile, related_name='purchases', on_delete=models.PROTECT)
    datetime = models.DateTimeField(default=timezone.now)

    @property
    def total_price(self):
        return sum(i.item.price * i.quantity for i in self.items.all())

    def __str__(self):
        return f"{self.datetime} by {self.user}"


class ItemPurchase(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='items', on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    # TODO add unique constraint: (purchase, item)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
