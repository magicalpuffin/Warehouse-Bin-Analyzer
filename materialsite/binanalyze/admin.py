from django.contrib import admin

from .models import Item, Bin, ShippingOrder

# Register your models here.
admin.site.register(Item)
admin.site.register(Bin)
admin.site.register(ShippingOrder)