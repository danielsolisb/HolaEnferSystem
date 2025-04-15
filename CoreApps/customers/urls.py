from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.CustomerListView.as_view(), name='customer-list'),
    path('nuevo/', views.CustomerCreateView.as_view(), name='customer-create'),
    path('detalle/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
]
