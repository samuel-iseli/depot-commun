from django.contrib import admin

from .models import Item, Purchase, ItemPurchase, UserProfile, Depot, Tag


class ItemPurchaseInline(admin.TabularInline):
    model = ItemPurchase
    extra = 1


class PurchaseAdmin(admin.ModelAdmin):
    search_fields = ('user', )
    inlines = (ItemPurchaseInline, )


admin.site.register(Item)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(UserProfile)
admin.site.register(Depot)
admin.site.register(Tag)
