from django.contrib import admin
from .models import City, Zona

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Zona)               # ← Registra Zona
class ZonaAdmin(admin.ModelAdmin):
    list_display   = ('nombre', 'ciudad')
    list_filter    = ('ciudad',)
    search_fields  = ('nombre',)