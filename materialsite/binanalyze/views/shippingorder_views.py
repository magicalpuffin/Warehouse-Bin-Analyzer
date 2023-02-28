import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.utils.py3dbp_wrapper import pack_SO
from binanalyze.tables import ItemTable, ShippingOrderTable, ShippingOrderItemTable
from binanalyze.forms import ShippingOrderForm, ShippingOrderItemForm

from django_tables2 import SingleTableView, SingleTableMixin
from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

@method_decorator(cache_control(no_cache= True, must_revalidate= True, no_store= True), name= 'dispatch')
class ShippingOrderListView(SingleTableMixin, TemplateView):
    # default context name for table_class is table
    # tables need have data passed
    table_class = ShippingOrderTable
    table_data = ShippingOrder.objects.all()
    template_name = 'binanalyze/shippingorder/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ShippingOrderForm
        return context

# Fix naming, should use shipping order item table
# Use better context names
# Will probably need to also pass in a form
# It seems like get_context_data is the easiest way to pass in context variables
@method_decorator(cache_control(no_cache= True, must_revalidate= True, no_store= True), name= 'dispatch')
class ShippingOrderDetailView(TemplateView):

    template_name = 'binanalyze/shippingorder/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shippingorder = ShippingOrder.objects.get(pk= kwargs.get('pk'))

        shippingorderitems = ShippingOrderItem.objects.filter(shippingorder = shippingorder)

        # Could pass in an exclude for shipping order, leaving it for debug
        # Could pass more info about each item?
        shippingorderitems_table = ShippingOrderItemTable(shippingorderitems)

        context['object'] = shippingorder
        context['table'] = shippingorderitems_table
        context['form'] = ShippingOrderItemForm

        return context


class ShippingOrderUpdateView(UpdateView):
    model = ShippingOrder
    template_name = 'binanalyze/shippingorder/create_update.html'
    fields = ['name', 'order_date', 'items']
    
class ShippingOrderCreateView(CreateView):
    model = ShippingOrder
    template_name = 'binanalyze/shippingorder/create_update.html'
    fields = ['name', 'order_date', 'items']

class ShippingOrderDeleteView(DeleteView):
    model = ShippingOrder
    success_url = '/binanalyze'
    template_name = 'binanalyze/shippingorder/delete.html'

def table_shippingorder_create(request):
    if request.method == 'POST':
        newshippingorderform = ShippingOrderForm(request.POST)
        if newshippingorderform.is_valid():
            newshippingorder = newshippingorderform.save()
            messages.add_message(request, messages.SUCCESS, f'Created {newshippingorder.name}')
        else:
            messages.add_message(request, messages.WARNING, "Couldn't create shippingorder")

    updatedtable = ShippingOrderTable(ShippingOrder.objects.all())

    return render(request, 'binanalyze/shippingorder/partials/table.html', {'table': updatedtable})

def table_shippingorder_delete(request, pk):
    if request.method == 'DELETE':
        removeshippingorder = ShippingOrder.objects.get(pk = pk)
        removeshippingorder.delete()
        messages.add_message(request, messages.SUCCESS, f'Deleted {removeshippingorder.name}')

    updatedtable = ShippingOrderTable(ShippingOrder.objects.all())

    return render(request, 'binanalyze/shippingorder/partials/table.html', {'table': updatedtable})

# Used for editing the table in the detail view
# Could rename stuff to be more clear
def table_shippingorderitem_create(request, pk):
    if request.method == 'POST':
        shippingorder = ShippingOrder.objects.get(pk = pk)
        item = Item.objects.get(pk = request.POST.get('item'))

        # This could be an shippingorder.add()
        newshippingorderitem = ShippingOrderItem(
            shippingorder= shippingorder, 
            item= item, 
            quantity= request.POST.get('quantity')
        )

        # Adds exception message, not best practice if public
        try:
            newshippingorderitem.full_clean()
        except Exception as e:
            messages.add_message(request, messages.WARNING, f'Error: {e}')
        else:
            newshippingorderitem.save()
            messages.add_message(request,messages.SUCCESS, f'Added {item.name} to {shippingorder.name}')

    updatedtable = ShippingOrderItemTable(ShippingOrderItem.objects.filter(shippingorder = shippingorder))

    return render(request, 'binanalyze/shippingorder/partials/table.html', {'table': updatedtable, 'object': shippingorder})

def table_shippingorderitem_delete(request, pk, pk_1):
    if request.method == 'DELETE':
        shippingorder = ShippingOrder.objects.get(pk = pk)
        removeshippingorderitem = ShippingOrderItem.objects.get(pk = pk_1)
        removeshippingorderitem.delete()
        messages.add_message(request, messages.SUCCESS, f'Removed {removeshippingorderitem.item.name} from {shippingorder.name}')

    updatedtable = ShippingOrderItemTable(ShippingOrderItem.objects.filter(shippingorder = shippingorder))

    return render(request, 'binanalyze/shippingorder/partials/table.html', {'table': updatedtable, 'object': shippingorder})