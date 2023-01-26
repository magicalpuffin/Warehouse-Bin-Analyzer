from django.urls import path

from . import views

app_name = 'binanalyze'

urlpatterns = [
    path('', views.SOListView.as_view(), name= 'home'),
    path('so/create/', views.SOCreateView.as_view(), name= 'so-create'),
    path('so/detail/<int:pk>/', views.SODetailView.as_view(), name= 'so-detail'),
    path('so/update/<int:pk>/', views.SOUpdateView.as_view(), name= 'so-update'),
    path('so/delete/<int:pk>/', views.SODeleteView.as_view(), name= 'so-delete'),
    path('item/create/', views.ItemCreateView.as_view(), name= 'item-create'),
    path('item/detail/<int:pk>/', views.ItemDetailView.as_view(), name= 'item-detail'),
    path('item/update/<int:pk>/', views.ItemUpdateView.as_view(), name= 'item-update'),
    path('item/delete/<int:pk>/', views.ItemDeleteView.as_view(), name= 'item-delete'),
    path('bin/create/', views.BinCreateView.as_view(), name= 'bin-create'),
    path('bin/detail/<int:pk>/', views.BinDetailView.as_view(), name= 'bin-detail'),
    path('bin/update/<int:pk>/', views.BinUpdateView.as_view(), name= 'bin-update'),
    path('bin/delete/<int:pk>/', views.BinDeleteView.as_view(), name= 'bin-delete'),
    path('analyze/', views.AnalyzeView.as_view(), name= 'analyze'),
]