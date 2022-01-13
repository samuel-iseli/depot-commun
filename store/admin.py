from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from solo.admin import SingletonModelAdmin
from django.utils import timezone
from django.db import models
from .models import UserProfile, Customer, Article, ArticleGroup, Purchase, Invoice, Settings

from .billing import get_billable_purchases, create_invoices


class UserProfileAdmin(UserAdmin):
    model = UserProfile


class CustomerAdmin(admin.ModelAdmin):
    fields = ('name', 'email')


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


class InvoiceAdmin(admin.ModelAdmin):
    actions = ['query_pending_invoices', 'do_create_invoices']
    list_display = ('id', 'customer', 'date')
    inlines = (InvoicePurchaseInline,)

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


class SettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ( _('Payment Account'), {
            'fields': (
                'payment_bank',
                'payment_account_number',
                'payment_account_name')
        }),
    )


# register model admins
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Article, ItemAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ArticleGroup)
admin.site.register(Settings, SettingsAdmin)

# customize site
admin.site.site_header = 'Depot Commün'