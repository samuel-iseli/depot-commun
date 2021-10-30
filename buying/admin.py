from django.contrib import admin

from .models import Item, Purchase, ItemPurchase, UserProfile, Depot, Tag


class ItemAdmin(admin.ModelAdmin):
    list_display = ('product_nr', 'name', 'price', 'number_of_items_in_stock')


class ItemPurchaseInline(admin.TabularInline):
    model = ItemPurchase
    extra = 1


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'total_price')
    search_fields = ('user', )
    inlines = (ItemPurchaseInline, )


admin.site.register(Item, ItemAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(UserProfile)
admin.site.register(Depot)
admin.site.register(Tag)
