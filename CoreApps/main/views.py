from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from CoreApps.users.forms import CustomUserCreationForm
from django.contrib.auth import login
from CoreApps.users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from CoreApps.users.models import User
from CoreApps.customers.models import CustomerProfile
# Añadir esta importación para JsonResponse
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    def get_success_url(self):
        return reverse_lazy('dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor verifica tus credenciales e intenta nuevamente.')
        return super().form_invalid(form)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'main/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user_type = User.UserType.CLIENT
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/dashboard/main_dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Otros datos de contexto (título, subtítulo, etc.)
        context['title'] = "Dashboard"
        context['subtitle'] = "Dashboard"
        context['user'] = user
        return context

