import pandas as pd
import json

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.tables import BinTable
from binanalyze.forms import BinForm

from django_tables2 import SingleTableMixin
from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

@method_decorator(cache_control(no_cache= True, must_revalidate= True, no_store= True), name= 'dispatch')
class BinListView(SingleTableMixin, TemplateView):
    table_class = BinTable
    table_data = Bin.objects.all()
    template_name = 'binanalyze/bin/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BinForm
        return context

class BinDetailView(DetailView):
    model = Bin
    template_name = 'binanalyze/bin/detail.html'
    
class BinUpdateView(UpdateView):
    model = Bin
    template_name = 'binanalyze/bin/create_update.html'
    fields = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight']
    
class BinCreateView(CreateView):
    model = Bin
    template_name = 'binanalyze/bin/create_update.html'
    fields = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight']

class BinDeleteView(DeleteView):
    model = Bin
    success_url = '/binanalyze'
    template_name = 'binanalyze/bin/delete.html'

# Copied from items
def table_bin_create(request):
    if request.method == 'POST':
        newbinform = BinForm(request.POST)
        if newbinform.is_valid():
            newbin = newbinform.save()
            messages.add_message(request, messages.SUCCESS, f'Created {newbin.name}')

        else:
            # Basic error handeling, however, form is not passed, errors on form not directly displayed
            messages.add_message(request, messages.WARNING, "Couldn't create bin")

    updatedtable = BinTable(Bin.objects.all())

    return render(request, 'binanalyze/bin/partials/table.html', {'table': updatedtable})

def table_bin_delete(request, pk):
    if request.method == 'DELETE':
        removebin = Bin.objects.get(pk = pk)
        removebin.delete()
        messages.add_message(request, messages.SUCCESS, f'Deleted {removebin.name}')

    updatedtable = BinTable(Bin.objects.all())

    return render(request, 'binanalyze/bin/partials/table.html', {'table': updatedtable})