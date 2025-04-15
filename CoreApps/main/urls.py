from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView, SignUpView, DashboardView,
)

# Elimina esta línea redundante
# from django.urls import path
# from . import view

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    
    
]