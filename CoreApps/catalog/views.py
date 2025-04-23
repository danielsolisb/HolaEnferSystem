from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Service, Product
from .forms import ServiceForm, ProductForm

# CRUD Services
class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'main/catalog/service_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Otros datos de contexto (título, subtítulo, etc.)
        context['title'] = "Servicios"
        context['subtitle'] = "Lista de servicios"
        context['user'] = user
        return context

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'main/catalog/service_form.html'
    success_url = reverse_lazy('catalog:service-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Otros datos de contexto (título, subtítulo, etc.)
        context['title'] = "Nuevo Servicio"
        context['subtitle'] = "Nuevo"
        context['user'] = user
        return context

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'main/catalog/service_form.html'
    success_url = reverse_lazy('catalog:service-list')

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'main/catalog/service_confirm_delete.html'
    success_url = reverse_lazy('catalog:service-list')

# CRUD Products
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'main/catalog/product_list.html'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user = self.request.user
       # Otros datos de contexto (título, subtítulo, etc.)
       context['title'] = "Productos"
       context['subtitle'] = "Lista de Productos"
       context['user'] = user
       return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/catalog/product_form.html'
    success_url = reverse_lazy('catalog:product-list')

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user = self.request.user
       # Otros datos de contexto (título, subtítulo, etc.)
       context['title'] = "Nuevo Producto"
       context['subtitle'] = "Nuevo"
       context['user'] = user
       return context

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/catalog/product_form.html'
    success_url = reverse_lazy('catalog:product-list')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'main/catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product-list')
