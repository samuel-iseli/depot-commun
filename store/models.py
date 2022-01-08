import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True)
    street = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    customer = models.ForeignKey(
        Customer,
        related_name='users',
        on_delete=models.SET_NULL,
        null=True, blank=True)


class ArticleGroup(models.Model):
    idx = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    group = models.ForeignKey(
        ArticleGroup, models.PROTECT, related_name='items')
    sortidx = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    active = models.BooleanField(default=True)

    @property
    def code(self):
        """
        generate a 3 digit code for easy identification.
        first digit is group idx afterward alphabetic index in group
        """
        # todo: implement
        return '123'

    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer = models.ForeignKey(
        Customer, related_name='invoices', on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def update_amount(self):
        self.amount = sum([p.price * p.quantity for p in self.purchases.all()])
        self.save()


class Purchase(models.Model):
    article = models.ForeignKey(Article, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    customer = models.ForeignKey(
        Customer, related_name='purchases', on_delete=models.PROTECT)
    invoice = models.ForeignKey(
        Invoice, related_name='purchases',
        on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.quantity} x {self.article.name}"

    def clean(self):
        if self.invoice:
            self.customer = self.invoice.customer
        if self.article:
            self.price = self.article.price
        super().clean()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update price on invoice
        if self.invoice:
            self.invoice.update_amount()

    def delete(self):
        """
        override delete to update invoice amount.
        """
        super().delete()
        if self.invoice:
            self.invoice.update_amount()
