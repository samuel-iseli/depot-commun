import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    street = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)


class ItemGroup(models.Model):
    idx = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    group = models.ForeignKey(
        ItemGroup, models.PROTECT, related_name='items')
    code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    user = models.ForeignKey(
        UserProfile, related_name='invoices', on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def update_amount(self):
        self.amount = sum([p.price * p.quantity for p in self.purchases.all()])
        self.save()


class Purchase(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(
        UserProfile, related_name='purchases', on_delete=models.PROTECT)
    invoice = models.ForeignKey(
        Invoice, related_name='purchases',
        on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def clean(self):
        if self.invoice:
            self.user = self.invoice.user
        if self.item:
            self.price = self.item.price * self.quantity
        super().clean()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update price on invoice
        if self.invoice:
            self.invoice.update_amount()
