from django.urls import path

from . import views

app_name = 'binanalyze'

urlpatterns = [
    path('', views.ShippingOrderListView.as_view(), name= 'index'),
    path('analyze/', views.AnalyzeView.as_view(), name= 'analyze'),
]

item_urlpatterns = [
    path('item/list/', views.ItemListView.as_view(), name= 'item-list'),
    path('item/create/', views.ItemCreateView.as_view(), name= 'item-create'),
    path('item/detail/<int:pk>/', views.ItemDetailView.as_view(), name= 'item-detail'),
    path('item/update/<int:pk>/', views.ItemUpdateView.as_view(), name= 'item-update'),
    path('item/delete/<int:pk>/', views.ItemDeleteView.as_view(), name= 'item-delete'),
]

bin_urlpatterns = [
    path('bin/create/', views.BinCreateView.as_view(), name= 'bin-create'),
    path('bin/detail/<int:pk>/', views.BinDetailView.as_view(), name= 'bin-detail'),
    path('bin/update/<int:pk>/', views.BinUpdateView.as_view(), name= 'bin-update'),
    path('bin/delete/<int:pk>/', views.BinDeleteView.as_view(), name= 'bin-delete'),
]

shippingorder_urlpatterns = [
    path('shippingorder/list/', views.ShippingOrderListView.as_view(), name= 'shippingorder-list'),
    path('shippingorder/create/', views.ShippingOrderCreateView.as_view(), name= 'shippingorder-create'),
    path('shippingorder/detail/<int:pk>/', views.ShippingOrderDetailView.as_view(), name= 'shippingorder-detail'),
    path('shippingorder/update/<int:pk>/', views.ShippingOrderUpdateView.as_view(), name= 'shippingorder-update'),
    path('shippingorder/delete/<int:pk>/', views.ShippingOrderDeleteView.as_view(), name= 'shippingorder-delete'),
]

htmx_urlpatterns = [
    path('item/list/table-item-create/', views.table_item_create, name= 'table-item-create'),
    path('item/list/table-item-delete/<int:pk>/', views.table_item_delete, name= 'table-item-delete'),
    path('shippingorder/list/table-item-create/', views.table_shippingorder_create, name= 'table-shippingorder-create'),
    path('shippingorder/list/table-item-delete/<int:pk>/', views.table_shippingorder_delete, name= 'table-shippingorder-delete'),
]

urlpatterns += item_urlpatterns
urlpatterns += bin_urlpatterns
urlpatterns += shippingorder_urlpatterns

urlpatterns += htmx_urlpatterns