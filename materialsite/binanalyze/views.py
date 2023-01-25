from django.shortcuts import render
from binanalyze.models import ShippingOrder
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import ShippingOrder

# Create your views here.

# def index(request):
#     context = {'so_list' : ShippingOrder.objects.all()}
#     return render(request, 'binanalyze/index.html', context)

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
    template_name = 'binanalyze/so_form.html'
    fields = ['name', 'order_date', 'items']
    