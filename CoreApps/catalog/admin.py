from django.contrib import admin
from .models import Service, Product

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'cantidad_disponible', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)
