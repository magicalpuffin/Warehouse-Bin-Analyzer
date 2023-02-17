import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.forms import ShippingOrderItemForm
from binanalyze.utils.py3dbp_wrapper import pack_SO
from binanalyze.tables import ShippingOrderTable
from binanalyze.forms import ShippingOrderForm

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

class ShippingOrderDetailView(DetailView):
    model = ShippingOrder
    template_name = 'binanalyze/shippingorder/detail.html'

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