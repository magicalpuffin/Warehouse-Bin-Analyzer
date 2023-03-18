import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.tables import ItemTable, BinTable, ShippingOrderTable
from binanalyze.utils.py3dbp_wrapper import pack_SO

from django_tables2 import MultiTableMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

# Consider just displaying all tables, multiple table mixin
# I don't think there is a way to set context name, just use list index

# @method_decorator(cache_control(no_cache= True, must_revalidate= True, no_store= True), name= 'dispatch')
class IndexView(MultiTableMixin, TemplateView):
    template_name = 'binanalyze/index.html'
    tables = [ItemTable, BinTable, ShippingOrderTable]
    tables_data = [Item.objects.all(), Bin.objects.all(), ShippingOrder.objects.all()]
    
    table_pagination = {
        'per_page': 5
    }
    
    # Uhh sketchy work around, overrides the default function, changes object to exclude the col
    def get_tables(self):
        tablelist = super().get_tables()
        for tableinst in tablelist:
            tableinst.exclude = ['delete']
        return tablelist