from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Servicios
    path('servicios/', views.ServiceListView.as_view(), name='service-list'),
    path('servicios/nuevo/', views.ServiceCreateView.as_view(), name='service-create'),
    path('servicios/<int:pk>/editar/', views.ServiceUpdateView.as_view(), name='service-update'),
    path('servicios/<int:pk>/eliminar/', views.ServiceDeleteView.as_view(), name='service-delete'),

    # Productos
    path('productos/', views.ProductListView.as_view(), name='product-list'),
    path('productos/nuevo/', views.ProductCreateView.as_view(), name='product-create'),
    path('productos/<int:pk>/editar/', views.ProductUpdateView.as_view(), name='product-update'),
    path('productos/<int:pk>/eliminar/', views.ProductDeleteView.as_view(), name='product-delete'),
]
