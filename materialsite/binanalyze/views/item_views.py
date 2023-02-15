import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.tables import ItemTable

from django_tables2 import SingleTableView
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

class ItemListView(SingleTableView):
    model = Item
    table_class = ItemTable
    template_name = 'binanalyze/item/list.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'binanalyze/item/detail.html'
    
class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'binanalyze/item/create_update.html'
    fields = ['name', 'unitlength', 'length', 'width', 'height', 'weight']
    
class ItemCreateView(CreateView):
    model = Item
    template_name = 'binanalyze/item/create_update.html'
    fields = ['name', 'unitlength', 'length', 'width', 'height', 'weight']

class ItemDeleteView(DeleteView):
    model = Item
    success_url = '/binanalyze'
    template_name = 'binanalyze/item/delete.html'