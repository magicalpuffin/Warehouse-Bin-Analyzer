from django.shortcuts import render
from binanalyze.models import ShippingOrder
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from .models import ShippingOrder, Item, Bin

from binanalyze.binpackfunctions import pack_SO

import pandas as pd
import json

# Create your views here.

# def index(request):
#     context = {'so_list' : ShippingOrder.objects.all()}
#     return render(request, 'binanalyze/index.html', context)

# TODO Reorganize, separate views into multiple files, consider using inheritence
# TODO Use forms and template based views
# TODO Create a home page view
# TODO pagination

# Changes for templates
    # Proper table view of items in shipping orders
    # Ideally table editing of multiple items, consider formsets
    # Have a better way for selecting items in a shipping order

class SOListView(ListView):
    model = ShippingOrder
    template_name = 'binanalyze/so_list.html'
    context_object_name = 'shipords'

class SODetailView(DetailView):
    model = ShippingOrder
    template_name = 'binanalyze/so_detail.html'
    context_object_name = 'shipord'

class SOUpdateView(UpdateView):
    model = ShippingOrder
    template_name = 'binanalyze/form.html'
    fields = ['name', 'order_date', 'items']
    
class SOCreateView(CreateView):
    model = ShippingOrder
    template_name = 'binanalyze/form.html'
    fields = ['name', 'order_date', 'items']

class SODeleteView(DeleteView):
    model = ShippingOrder
    success_url = '/binanalyze'
    template_name = 'binanalyze/confirm_delete.html'

# Items
class ItemDetailView(DetailView):
    model = Item
    template_name = 'binanalyze/itembin_detail.html'
    
class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'binanalyze/form.html'
    fields = ['name', 'length', 'width', 'height', 'weight']
    
class ItemCreateView(CreateView):
    model = Item
    template_name = 'binanalyze/form.html'
    fields = ['name', 'length', 'width', 'height', 'weight']

class ItemDeleteView(DeleteView):
    model = Item
    success_url = '/binanalyze'
    template_name = 'binanalyze/confirm_delete.html'

# Bins
class BinDetailView(DetailView):
    model = Bin
    template_name = 'binanalyze/itembin_detail.html'
    
class BinUpdateView(UpdateView):
    model = Bin
    template_name = 'binanalyze/form.html'
    fields = ['name', 'length', 'width', 'height', 'weight']
    
class BinCreateView(CreateView):
    model = Bin
    template_name = 'binanalyze/form.html'
    fields = ['name', 'length', 'width', 'height', 'weight']

class BinDeleteView(DeleteView):
    model = Bin
    success_url = '/binanalyze'
    template_name = 'binanalyze/confirm_delete.html'

# TODO Create multiple analyze views
    # Bin packing and results
    # Bins and bin ussage
    # Items and item frequencies
    # Shipping order volumes
    # Data visualizations
    # Individually pack certain orders
    # Data visualization on volume and weight utilization
    # Many of these will probably need to merge with dash

# Analyze
class AnalyzeView(TemplateView):
    template_name = 'binanalyze/analyze.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shipords'] = ShippingOrder.objects.all()
        context['bins'] = Bin.objects.all()

        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Selects all shipping orders, renames due to how the current binpackfunction works
        # Manually sets all quantities to 1 because I haven't figured that out yet
        soobjs = ShippingOrder.objects.all()
        so_df = pd.DataFrame.from_records(soobjs.values('name', 'items__name', 'items__length', 'items__width', 'items__height', 'items__weight'))
        so_df.columns = ['Shipment_Number', 'Item Number', 'Length', 'Width', 'Height', 'Weight']
        so_df.loc[:, 'Quantity'] = 1
        so_df = so_df.set_index('Shipment_Number')

        binobjs = Bin.objects.all()
        bin_df = pd.DataFrame.from_records(binobjs.values('name', 'length', 'width', 'height', 'weight'))
        bin_df.columns = ['Bin Name', 'Length', 'Width', 'Height', 'Weight']

        result_df = so_df.groupby(level= 0).apply(pack_SO, bin_df=bin_df)

        # TODO Check if this actually fine for displaying dataframes as tables
        json_records = result_df.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)

        context['d'] = data
        return render(request, self.template_name, context)