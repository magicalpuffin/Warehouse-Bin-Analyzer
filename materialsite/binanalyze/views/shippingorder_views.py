import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.forms import ShippingOrderItemForm
from binanalyze.utils.py3dbp_wrapper import pack_SO

from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

class ShippingOrderListView(ListView):
    model = ShippingOrder
    template_name = 'binanalyze/shippingorder/list.html'
    context_object_name = 'shipords'

class ShippingOrderDetailView(DetailView):
    model = ShippingOrder
    template_name = 'binanalyze/shippingorder/detail.html'
    context_object_name = 'shipord'

class ShippingOrderUpdateView(UpdateView):
    model = ShippingOrder
    template_name = 'binanalyze/shippingorder/create_update.html'
    fields = ['name', 'order_date', 'items']
    
class ShippingOrderCreateView(CreateView):
    model = ShippingOrder
    template_name = 'binanalyze/shippingorder/create_update.html'
    fields = ['name', 'order_date', 'items']
# Diffuclt to use forms
# class ShippingOrderCreateView(CreateView):
#     model = ShippingOrder
#     template_name = 'binanalyze/shippingorder/create_update.html'
#     form_class = ShippingOrderItemForm

class ShippingOrderDeleteView(DeleteView):
    model = ShippingOrder
    success_url = '/binanalyze'
    template_name = 'binanalyze/shippingorder/delete.html'
