from django import forms
from binanalyze.models import Item, ShippingOrder, ShippingOrderItem

class ShippingOrderItemForm(forms.ModelForm):
    class Meta:
        model = ShippingOrderItem
        fields = ['shippingorder', 'item', 'quantity']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'unitlength', 'length', 'width', 'height', 'weight']