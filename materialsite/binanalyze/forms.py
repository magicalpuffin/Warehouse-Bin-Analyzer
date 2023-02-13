from django import forms
from binanalyze.models import ShippingOrder, ShippingOrderItem

class ShippingOrderItemForm(forms.ModelForm):
    class Meta:
        model = ShippingOrderItem
        fields = ['shippingorder', 'item', 'quantity']