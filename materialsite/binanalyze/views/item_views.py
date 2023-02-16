import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.tables import ItemTable
from binanalyze.forms import ItemForm

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

class ItemListView(SingleTableMixin, TemplateView):
    table_class = ItemTable
    table_data = Item.objects.all()
    template_name = 'binanalyze/item/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemForm
        return context

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

def add_item(request):
    newitem = ItemForm(request.POST)
    newitem.save()

    return render(request, 'binanalyze/partials/item-table.html', {'table': ItemTable(Item.objects.all())})
