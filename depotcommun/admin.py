from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from solo.admin import SingletonModelAdmin
from django.db import models
from .models import ExtraItem, ShoppingBasket, UserProfile, Customer, Article, ArticleGroup, Purchase, Invoice, Settings, EmailTask
from .email import send_invoice_mails
from admin_totals.admin import ModelAdminTotals


class UserProfileAdmin(UserAdmin):
    model = UserProfile


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'group', 'active')
    ordering = ('group__idx', 'sortidx', 'name')
    search = ('name')
    list_filter = ('group', 'active')


class InvoicePurchaseInline(admin.TabularInline):
    model = Purchase
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


class InvoiceAdmin(ModelAdminTotals):
    # actions = ['query_pending_invoices', 'do_create_invoices']
    actions = ['send_invoices_email', 'mark_as_paid']
    list_display = ('id', 'customer', 'date', 'amount', 'paid', 'email_sent')
    list_totals = [('amount', models.Sum)]
    date_hierarchy = 'date'
    ordering = ('-id',)
    list_filter = ('paid',)
    search_fields = ('id', 'customer__name')
    inlines = (InvoicePurchaseInline, InvoiceExtraInline)

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

    @admin.action(description=_('Mark selected invoices as paid'))
    def mark_as_paid(self, request, queryset):
        for invoice in queryset.all():
            invoice.paid = True
            invoice.save()


class BasketPurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 1
    fields = ('article', 'price', 'quantity')


class ShoppingBasketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date')
    date_hierarchy = 'date'
    ordering = ('-date',)
    search_fields = ('customer__name',)
    inlines = (BasketPurchaseInline,)


class SettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        (_('Payment Account'), {
            'fields': (
                'payment_bank',
                'payment_account_number',
                'payment_account_name',
                'payment_account_street',
                'payment_account_place')
        }),
    )


class EmailTaskAdmin(admin.ModelAdmin):
    list_display = ('started', 'finished', 'successful', 'email_count')


# register model admins
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Article, ItemAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(ShoppingBasket, ShoppingBasketAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ArticleGroup)
admin.site.register(EmailTask, EmailTaskAdmin)
admin.site.register(Settings, SettingsAdmin)

# customize site
admin.site.site_header = 'Depot Commün'
