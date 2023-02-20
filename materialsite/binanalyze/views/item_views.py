import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.tables import ItemTable
from binanalyze.forms import ItemForm

from django_tables2 import SingleTableMixin
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

# Seems to have a bug when caching and reloading page showing deleted items
# Should add error messages
class ItemListView(SingleTableMixin, TemplateView):
    # default context name for table_class is table
    # tables need have data passed
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

# These views don't use the modelform
class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'binanalyze/item/create_update.html'
    fields = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight']
    
class ItemCreateView(CreateView):
    model = Item
    template_name = 'binanalyze/item/create_update.html'
    fields = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight']

class ItemDeleteView(DeleteView):
    model = Item
    success_url = '/binanalyze'
    template_name = 'binanalyze/item/delete.html'

# Function based views used to update table as part of htmx
# Might need to display and render the entire section, or have multiple sections being updated...
# Could refresh the entire content every post and delete
# Not sure if it is possible to use a class based view for these
def table_item_create(request):
    if request.method == 'POST':
        newitemform = ItemForm(request.POST)
        if newitemform.is_valid():
            newitem = newitemform.save()

            # Currently base and the table view has messages, which may result in duplicate messages...
            # Could add extra tags to check
            # Some formatting issues with table moving
            messages.add_message(request, messages.SUCCESS, f'Created {newitem.name}')

        else:
            # Basic error handeling, however, form is not passed, errors on form not directly displayed
            messages.add_message(request, messages.WARNING, "Couldn't create item")

    updatedtable = ItemTable(Item.objects.all())

    return render(request, 'binanalyze/item/partials/table.html', {'table': updatedtable})

def table_item_delete(request, pk):
    if request.method == 'DELETE':
        removeitem = Item.objects.get(pk = pk)
        removeitem.delete()
        messages.add_message(request, messages.SUCCESS, f'Deleted {removeitem.name}')

    updatedtable = ItemTable(Item.objects.all())

    return render(request, 'binanalyze/item/partials/table.html', {'table': updatedtable})