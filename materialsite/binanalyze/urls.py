from django.urls import path

from . import views

app_name = 'binanalyze'

urlpatterns = [
    path('', views.SOListView.as_view(), name= 'home'),
    path('detail/<int:pk>/', views.SODetailView.as_view(), name= 'so-detail'),
    path('update/<int:pk>/', views.SOUpdateView.as_view(), name= 'so-update'),
]