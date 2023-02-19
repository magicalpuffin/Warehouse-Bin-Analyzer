import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.utils.py3dbp_wrapper import pack_SO
from binanalyze.tables import ItemTable, ShippingOrderTable, ShippingOrderItemTable
from binanalyze.forms import ShippingOrderForm, ShippingOrderItemForm

from django_tables2 import SingleTableView, SingleTableMixin
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

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
    newshippingorder = ShippingOrderForm(request.POST)
    newshippingorder.save()

    updatedtable = ShippingOrderTable(ShippingOrder.objects.all())

    return render(request, 'binanalyze/shippingorder/partials/table.html', {'table': updatedtable})

def table_shippingorder_delete(request, pk):
    removeshippingorder = ShippingOrder.objects.get(pk = pk)
    removeshippingorder.delete()

    updatedtable = ShippingOrderTable(ShippingOrder.objects.all())

    return render(request, 'binanalyze/shippingorder/partials/table.html', {'table': updatedtable})

# Used for editing the table in the detail view
# Could rename stuff to be more clear
def table_shippingorderitem_create(request, pk):
    shippingorder = ShippingOrder.objects.get(pk = pk)
    item = Item.objects.get(pk = request.POST.get('item'))

    newshippingorderitem = ShippingOrderItem(
        shippingorder= shippingorder, 
        item= item, 
        quantity= request.POST.get('quantity')
    )
    newshippingorderitem.save()

    updatedtable = ShippingOrderItemTable(ShippingOrderItem.objects.filter(shippingorder = shippingorder))

    return render(request, 'binanalyze/shippingorder/partials/table.html', {'table': updatedtable, 'object': shippingorder})

def table_shippingorderitem_delete(request, pk, pk_1):
    shippingorder = ShippingOrder.objects.get(pk = pk)
    removeshippingorderitem = ShippingOrderItem.objects.get(pk = pk_1)
    removeshippingorderitem.delete()

    updatedtable = ShippingOrderItemTable(ShippingOrderItem.objects.filter(shippingorder = shippingorder))

    return render(request, 'binanalyze/shippingorder/partials/table.html', {'table': updatedtable, 'object': shippingorder})