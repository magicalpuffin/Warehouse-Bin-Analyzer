import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.tables import ItemTable, ShippingOrderTable
from binanalyze.utils.py3dbp_wrapper import pack_SO

from django_tables2 import MultiTableMixin
from django.shortcuts import render
from django.views.generic import TemplateView

# Consider just displaying all tables, multiple table mixin
# I don't think there is a way to set context name, just use list index
class IndexView(MultiTableMixin, TemplateView):
    template_name = 'binanalyze/index.html'
    tables = [
        ItemTable(Item.objects.all(), exclude= ['delete']),
        ShippingOrderTable(ShippingOrder.objects.all(), exclude= ['delete'])
        ]
    
    table_pagination = {
        'per_page': 5
    }