import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.tables import ItemTable, BinTable, ShippingOrderTable, ShippingOrderItemTable, PackResultTable
from binanalyze.utils.py3dbp_wrapper import pack_SO

from django_tables2 import MultiTableMixin
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
class AnalyzeView(MultiTableMixin, TemplateView):
    template_name = 'binanalyze/analyze.html'
    
    tables = [ShippingOrderItemTable, BinTable]
    tables_data = [ShippingOrderItem.objects.all(), Bin.objects.all()]
    
    table_pagination = {
        'per_page': 5
    }

    # Uhh sketchy work around, overrides the default function, changes object to exclude the col
    def get_tables(self):
        tablelist = super().get_tables()
        for tableinst in tablelist:
            tableinst.exclude = ['delete']
        return tablelist

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['shipords'] = ShippingOrder.objects.all()
    #     context['bins'] = Bin.objects.all()

    #     return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        recordlist = []
        for shippingorderitem in ShippingOrderItem.objects.all():
            rowdict = {
                'shippingorder_name':shippingorderitem.shippingorder.name,
                'quantity': shippingorderitem.quantity,
                'item_length': shippingorderitem.item.get_length(True),
                'item_width': shippingorderitem.item.get_width(True),
                'item_height': shippingorderitem.item.get_height(True),
                'item_weight': shippingorderitem.item.get_weight(True),
            }
            recordlist.append(rowdict)

        binlist = []
        for bin in Bin.objects.all():
            rowdict = {
                'bin_name':bin.name,
                'bin_length': bin.get_length(True),
                'bin_width': bin.get_width(True),
                'bin_height': bin.get_height(True),
                'bin_weight': bin.get_weight(True),
            }
            binlist.append(rowdict)

        bin_df = pd.DataFrame.from_records(binlist)
        so_df = pd.DataFrame.from_records(recordlist)
        so_df = so_df.set_index('shippingorder_name')

        result_df = so_df.groupby(level= 0).apply(pack_SO, bin_df=bin_df)

        numeric_cols = ['volume_difference', 'weight_difference', 'volume_utilization', 'weight_utilization']
        result_df.loc[:, numeric_cols] = result_df.loc[:, numeric_cols].apply(pd.to_numeric, axis=1).round(6)

        result_records = result_df.reset_index().to_dict(orient ='records')
        context['packresulttable'] = PackResultTable(result_records)
        
        return render(request, self.template_name, context)