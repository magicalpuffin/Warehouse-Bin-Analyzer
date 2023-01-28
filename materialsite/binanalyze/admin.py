from django.contrib import admin

from .models import Item, Bin, ShippingOrder

# Register your models here.
# Check django admin site documentation about many to many models
# TODO After updating model, attempt to enable tablular based editing

class ItemInline(admin.TabularInline):
    model = ShippingOrder.items.through

class ShippingOrderAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

admin.site.register(Item)
admin.site.register(Bin)
admin.site.register(ShippingOrder, ShippingOrderAdmin)