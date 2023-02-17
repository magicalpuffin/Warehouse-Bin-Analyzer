from django import forms
from binanalyze.models import Item, ShippingOrder, ShippingOrderItem

class ShippingOrderItemForm(forms.ModelForm):
    class Meta:
        model = ShippingOrderItem
        fields = ['shippingorder', 'item', 'quantity']

# form used to quick create items, other item creation uses create view
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight']

class ShippingOrderForm(forms.ModelForm):
    class Meta:
        model = ShippingOrder
        fields = ['name', 'order_date']
        widgets = {
            'order_date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }