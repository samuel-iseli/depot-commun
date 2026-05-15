from dataclasses import field

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import gettext as _
from solo.admin import SingletonModelAdmin
from django.utils import timezone
from django.db import models
from .models import ExtraItem, ShoppingBasket, UserProfile, Customer, Article, ArticleGroup, Purchase, Invoice, Settings, EmailTask
from .email import send_invoice_mails, send_reminder_mails
from admin_totals.admin import ModelAdminTotals

from .billing import get_billable_purchases, create_invoices


class UserProfileAdmin(UserAdmin):
    model = UserProfile


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user')
    search_fields = ('name', 'email')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'group', 'active')
    ordering = ('group__idx', 'sortidx', 'name')
    search = ('name')
    list_filter = ('group', 'active')


class InvoicePurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # adjust article choices to only show active articles, but include the currently selected article if it is inactive
        article_field = self.fields['article']
        visible_queryset = Article.objects.filter(active=True)
        if self.instance.pk and self.instance.article_id:
            visible_queryset = Article.objects.filter(
                models.Q(active=True) | models.Q(pk=self.instance.article_id)
            )

        article_field.widget.choices = forms.ModelChoiceField(
            queryset=visible_queryset,
            required=article_field.required,
            empty_label=article_field.empty_label,
        ).choices


class InvoicePurchaseInline(admin.TabularInline):
    model = Purchase
    form = InvoicePurchaseForm
    extra = 1
    fields = ('article', 'price', 'quantity', 'summe')
    readonly_fields = ('price', 'summe')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """
        override method to remove the add, change, delete buttons
        from the related control (article) in this inline
        """
        formfield = super().formfield_for_dbfield(
            db_field, request, **kwargs)
        if isinstance(db_field, models.ForeignKey):
            formfield.widget.can_add_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_delete_related = False
        return formfield
 
    def summe(self, purchase):
        if purchase.price:
            return purchase.price * purchase.quantity
        return 0.0


class InvoiceExtraInline(admin.TabularInline):
    model = ExtraItem
    extra = 0
    fields = ('text', 'amount')


class InvoiceBasketInline(admin.TabularInline):
    model = ShoppingBasket
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ('completed', 'purchase_count', 'purchase_total')
    readonly_fields = ('completed', 'purchase_count', 'purchase_total')

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description='Anzahl Einkäufe')
    def purchase_count(self, basket):
        return basket.purchases.count()

    @admin.display(description='Einkauf Total')
    def purchase_total(self, basket):
        return sum((purchase.total_price for purchase in basket.purchases.all()), 0)


class InvoiceAdmin(ModelAdminTotals):
    actions = ['send_invoices_email', 'send_reminder_email', 'mark_as_paid']
    list_display = ('id', 'customer', 'date', 'amount', 'paid', 'email_sent')
    list_totals = [('amount', models.Sum)]
    date_hierarchy = 'date'
    ordering = ('-id',)
    list_filter = ('paid',)
    search_fields = ('id', 'customer__name')
    inlines = (InvoicePurchaseInline, InvoiceExtraInline, InvoiceBasketInline)

    @admin.action(description=_('Send selected invoices per e-mail'))
    def send_invoices_email(self, request, queryset):
        """
        send the selected invoices per e-mail.
        """
        invoices = queryset.all()
        success, message = send_invoice_mails(invoices)

        if success:
            self.message_user(
                request,
                message,
                'SUCCESS'
                )
        else:
            self.message_user(
                request,
                message,
                'WARNING'
                )

    @admin.action(description='Zahlungserinnerungen für ausgewählte Rechnungen senden')
    def send_reminder_email(self, request, queryset):
        """
        send the selected invoices per e-mail.
        """
        invoices = queryset.all()
        success, message = send_reminder_mails(invoices)

        if success:
            self.message_user(
                request,
                message,
                'SUCCESS'
                )
        else:
            self.message_user(
                request,
                message,
                'WARNING'
                )

    @admin.action(description=_('Mark selected invoices as paid'))
    def mark_as_paid(self, request, queryset):
        for invoice in queryset.all():
            invoice.paid = True
            invoice.save()

    def query_pending_invoices(self, request, queryset):
        """
        Display the number and total amount of invoices that
        would be generated now.
        """
        billables = get_billable_purchases(timezone.now())
        purchases = []
        for plist in billables.values():
            purchases.extend(plist)

        total = sum([purchase.total_price for purchase in purchases])

        # show message
        self.message_user(
            request,
            _(f'{len(billables)} invoices with a total amount of {total} would be generated.'),
            messages.SUCCESS)

    def do_create_invoices(self, request, queryset):
        """
        create all pending invoices.
        """
        effective_date = timezone.now()
        invoices = create_invoices(effective_date, effective_date)
        total = sum([inv.amount for inv in invoices])

        # show created invoice count
        self.message_user(
            request,
            _(f'{len(invoices)} invoices with a total amount of {total} have been generated.'),
            messages.SUCCESS)

class ShoppingBasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'invoice', 'date', 'completed')
    search_fields = ('customer__name',)
    ordering = ('-date',)
    inlines = (InvoicePurchaseInline,)

class SettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ( _('Payment Account'), {
            'fields': (
                'payment_bank',
                'payment_account_number',
                'payment_account_name',
                'payment_account_street',
                'payment_account_house_number',
                'payment_account_postal_code',
                'payment_account_place')
        }),
    )


class EmailTaskAdmin(admin.ModelAdmin):
    list_display = ('started', 'finished', 'successful', 'email_count')


# register model admins
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Article, ItemAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ArticleGroup)
admin.site.register(EmailTask, EmailTaskAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(ShoppingBasket, ShoppingBasketAdmin)

# customize site
admin.site.site_header = 'Depot Commün'
