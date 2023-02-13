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
        so_items = ShippingOrderItem.objects.all()
        so_df = pd.DataFrame.from_records(so_items.values('shippingorder__name', 'quantity', 'item__name', 'item__length', 'item__width', 'item__height', 'item__weight'))
        so_df.columns = ['shippingorder_name', 'quantity', 'item_name', 'item_length', 'item_width', 'item_height', 'item_weight']
        so_df = so_df.set_index('shippingorder_name')

        binobjs = Bin.objects.all()
        bin_df = pd.DataFrame.from_records(binobjs.values('name', 'length', 'width', 'height', 'weight'))
        bin_df.columns = ['bin_name', 'bin_length', 'bin_width', 'bin_height', 'bin_weight']

        result_df = so_df.groupby(level= 0).apply(pack_SO, bin_df=bin_df)

        # TODO Check if this actually fine for displaying dataframes as tables
        json_records = result_df.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)

        context['d'] = data
        return render(request, self.template_name, context)