from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CustomerProfile
from .forms import CustomerProfileForm
from CoreApps.core.models import Zona
from django.http import JsonResponse

class CustomerListView(LoginRequiredMixin, ListView):
    model = CustomerProfile
    #template_name = 'main/customers/customer_list.html'
    template_name = 'main/customers/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return CustomerProfile.objects.select_related('ciudad', 'zona').all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Otros datos de contexto (título, subtítulo, etc.)
        context['title'] = "Clientes"
        context['subtitle'] = "Lista de clientes"
        context['user'] = user
        return context

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = CustomerProfile
    form_class = CustomerProfileForm
    template_name = 'main/customers/customer_form.html'
    success_url = reverse_lazy('customers:customer-list')

    def form_valid(self, form):
        form.instance.registrado_por = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Otros datos de contexto (título, subtítulo, etc.)
        context['title'] = "Nuevo Cliente"
        context['subtitle'] = "Nuevo"
        context['zona_inicial'] = None
        context['user'] = user
        return context

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = CustomerProfile
    template_name = 'main/customers/customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Otros datos de contexto (título, subtítulo, etc.)
        context['title'] = "Nuevo Cliente"
        context['subtitle'] = "Nuevo"
        context['user'] = user
        return context

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomerProfile
    form_class = CustomerProfileForm
    template_name = 'main/customers/customer_form.html'
    success_url = reverse_lazy('customers:customer-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Otros datos de contexto (título, subtítulo, etc.)
        context['title'] = "Editar Cliente"
        context['subtitle'] = "Editar"
        context['zona_inicial'] = self.object.zona_id
        context['user'] = user
        return context

class CustormerDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomerProfile
    template_name = 'main/customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customers:customer-list')

def obtener_zonas_por_ciudad(request):
    """
    Endpoint que recibe GET?ciudad_id=… y devuelve
    [{'id': zona_id, 'nombre': zona_nombre}, …]
    """
    ciudad_id = request.GET.get('ciudad_id')
    if not ciudad_id:
        return JsonResponse([], safe=False)

    qs = Zona.objects.filter(ciudad_id=ciudad_id).values('id', 'nombre')
    data = [{'id': z['id'], 'nombre': z['nombre']} for z in qs]
    return JsonResponse(data, safe=False)
