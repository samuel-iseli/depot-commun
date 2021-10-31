from django.contrib import admin, messages
from django.utils import timezone
from .models import Item, Purchase, ItemPurchase, UserProfile, Depot, Tag, Invoice

from .billing import get_billable_purchases


class ItemAdmin(admin.ModelAdmin):
    list_display = ('product_nr', 'name', 'price', 'number_of_items_in_stock')


class ItemPurchaseInline(admin.TabularInline):
    model = ItemPurchase
    extra = 1


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'total_price')
    search_fields = ('user', )
    inlines = (ItemPurchaseInline, )


class InvoiceAdmin(admin.ModelAdmin):
    actions = ['query_pending_invoices', 'create_invoices']

    def query_pending_invoices(self, request, queryset):
        """
        Display the number and total amount of invoices that
        would be generated now.
        """
        # determine depot of currently logged in user
        # todo: changes this to get the home depot of user
        depot = Depot.objects.all()[0]

        billables = get_billable_purchases(depot, timezone.now())
        purchases = []
        for plist in billables.values():
            purchases.extend(plist)

        total = sum([purchase.total_price for purchase in purchases])

        # show message
        self.message_user(
            request,
            f'{len(billables)} invoices with a total amount of {total} would be generated.',
            messages.SUCCESS)


admin.site.register(Item, ItemAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(UserProfile)
admin.site.register(Depot)
admin.site.register(Tag)
