from django import forms
from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem

# form used to quick create items, other item creation uses create view
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight']

class BinForm(forms.ModelForm):
    class Meta:
        model = Bin
        fields = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight']

# DateTimeInput just defaults to normal text box
class ShippingOrderForm(forms.ModelForm):
    class Meta:
        model = ShippingOrder
        fields = ['name', 'order_date']
        widgets = {
            'order_date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }

# Used to add new items in the shippingorder detail view
class ShippingOrderItemForm(forms.ModelForm):
    class Meta:
        model = ShippingOrderItem
        fields = ['item', 'quantity']
