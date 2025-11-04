from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from solo.models import SingletonModel
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Customer(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_('Name'))
    email = models.EmailField(
        max_length=50, blank=True, verbose_name=_('E-Mail'))
    street = models.CharField(
        max_length=100, blank=True, verbose_name=_('Street'))
    house_number = models.CharField(
        max_length=10, blank=True, verbose_name=_('House Number'))
    zip = models.CharField(
        max_length=10, verbose_name=_('ZIP'))
    city = models.CharField(
        max_length=50, blank=True, verbose_name=_('City'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class UserProfile(AbstractUser):
    customer = models.ForeignKey(
        Customer,
        related_name='users',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Customer'))


class ArticleGroup(models.Model):
    idx = models.PositiveSmallIntegerField(default=0, verbose_name=_('Idx'))
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['idx']
        verbose_name = _('Articlegroup')
        verbose_name_plural = _('Articlegroups')


class Article(models.Model):
    group = models.ForeignKey(
        ArticleGroup, models.PROTECT, related_name='items',
        verbose_name=_('Group'))
    sortidx = models.PositiveSmallIntegerField(
        default=0, verbose_name=_('Sort Index'))
    name = models.CharField(
        max_length=200, verbose_name=_('Name'))
    price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name=_('Price'))
    active = models.BooleanField(
        default=True, verbose_name=_('Active'))

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

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['group', 'sortidx', 'name']


class Invoice(models.Model):
    customer = models.ForeignKey(
        Customer, related_name='invoices', on_delete=models.PROTECT,
        verbose_name=_('Customer'))
    date = models.DateTimeField(
        default=timezone.now, verbose_name=_('Date'))
    amount = models.DecimalField(
        max_digits=7, decimal_places=2, default=0, verbose_name=_('Amount'))
    paid = models.BooleanField(_('Paid'), default=False)
    payment_date = models.DateField(
        null=True, blank=True,
        verbose_name=_('Payment date'))
    email_sent = models.BooleanField('Email gesendet', default=False)

    def update_amount(self):
        purchase_amount = sum([p.price * p.quantity for p in self.purchases.all()])
        extra_amount = sum([itm.amount for itm in self.extra_items.all()])
        self.amount = purchase_amount + extra_amount
        self.save()

    def save(self, *args, **kwargs):
        """
        override save to automatically set
        payment date.
        """
        if self.paid and self.payment_date is None:
            self.payment_date = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return gettext('Invoice %d') % self.id

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['date']


class Purchase(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.PROTECT,
        verbose_name=_('Article'))
    quantity = models.PositiveSmallIntegerField(
        default=1, verbose_name=_('Quantity'))
    price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name=_('Price'))
    invoice = models.ForeignKey(
        Invoice, related_name='purchases',
        on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Invoice'))
    basket = models.ForeignKey(
        'ShoppingBasket', related_name='purchases',
        on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('Basket'))

    def __str__(self):
        return f"{self.quantity} x {self.article.name}"

    def clean(self):
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

    class Meta:
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')


class ShoppingBasket(models.Model):
    date = models.DateTimeField(
        default=timezone.now, verbose_name=_('Date'))
    customer = models.ForeignKey(
        Customer, related_name='shopping_baskets',
        on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Customer'))
    invoice = models.ForeignKey(
        Invoice, related_name='baskets',
        on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Invoice'))

    class Meta:
        verbose_name = _('Shopping Basket')
        verbose_name_plural = _('Shopping Baskets')


class ExtraItem(models.Model):
    """
    extra invoice item not based on an article.
    may be used to charge other stuff to users.
    """
    text = models.CharField(
        max_length=200, verbose_name=_('Text'))
    amount = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name=_('Amount'))
    invoice = models.ForeignKey(
        Invoice, related_name='extra_items',
        on_delete=models.CASCADE,
        verbose_name=_('Invoice'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update amount on invoice
        if self.invoice:
            self.invoice.update_amount()

    def delete(self):
        """
        override delete to update invoice amount.
        """
        super().delete()
        if self.invoice:
            self.invoice.update_amount()

    class Meta:
        verbose_name = _('Extra Item')
        verbose_name_plural = _ ('Extra Items')


class EmailTask(models.Model):
    started = models.DateTimeField(
        verbose_name='Gestartet',
        default=timezone.now)
    finished = models.DateTimeField(
        verbose_name='Beendet',
        null=True, blank=True)
    email_count = models.IntegerField(
        verbose_name='Anzahl E-Mails',
        default=0)
    successful = models.BooleanField(
        verbose_name='Erfolgreich',
        default=False)
    log_text = models.TextField(
        verbose_name='Log')


class Settings(SingletonModel):
    payment_bank = models.CharField(
        verbose_name=_('Bank'),
        max_length=50, blank=True)
    payment_account_number = models.CharField(
        verbose_name=_('Account Number'),
        max_length=50, blank=True)
    payment_account_name = models.CharField(
        verbose_name=_('Account Name'),
        max_length=100, blank=True)
    payment_account_street = models.CharField(
        verbose_name=_('Account Street'),
        max_length=100, blank=True)
    payment_account_house_number = models.CharField(
        verbose_name=_('Account House Number'),
        max_length=10, blank=True)
    payment_account_place = models.CharField(
        verbose_name=_('Account Place'),
        max_length=100, blank=True)
    payment_account_postal_code = models.CharField(
        verbose_name=_('Account Postal Code'),
        max_length=10, blank=True)

    def __str__(self):
        return gettext('Settings')

    class Meta:
        verbose_name = _('Settings')
