from django.contrib import admin, messages
from django.utils import timezone
from .models import Customer, Item, ItemGroup, Purchase, Invoice

from .billing import get_billable_purchases, create_invoices


class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price', 'group')
    ordering = ('code',)
    search = ('code', 'name')


class InvoicePurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 1
    fields = ('item', 'price', 'quantity', 'summe')
    readonly_fields = ('price', 'summe')

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
            f'{len(billables)} invoices with a total amount of {total} would be generated.',
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
            f'{len(invoices)} invoices with a total amount of {total} have been generated.',
            messages.SUCCESS)


admin.site.register(Item, ItemAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Customer)
admin.site.register(ItemGroup)
