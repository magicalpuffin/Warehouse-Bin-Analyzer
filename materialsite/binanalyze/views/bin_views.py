import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
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

class BinDetailView(DetailView):
    model = Bin
    template_name = 'binanalyze/bin/detail.html'
    
class BinUpdateView(UpdateView):
    model = Bin
    template_name = 'binanalyze/bin/create_update.html'
    fields = ['name', 'unitlength', 'length', 'width', 'height', 'weight']
    
class BinCreateView(CreateView):
    model = Bin
    template_name = 'binanalyze/bin/create_update.html'
    fields = ['name', 'unitlength', 'length', 'width', 'height', 'weight']

class BinDeleteView(DeleteView):
    model = Bin
    success_url = '/binanalyze'
    template_name = 'binanalyze/bin/delete.html'