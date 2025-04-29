from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.CustomerListView.as_view(), name='customer-list'),
    path('nuevo/', views.CustomerCreateView.as_view(), name='customer-create'),
    path('detalle/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('editar/<int:pk>/', views.CustomerUpdateView.as_view(), name='customer-update'),
    path('eliminar/<int:pk>/', views.CustormerDeleteView.as_view(), name='customer-delete'),
    path('api/zonas/', views.obtener_zonas_por_ciudad, name='api-obtener-zonas'),
]
