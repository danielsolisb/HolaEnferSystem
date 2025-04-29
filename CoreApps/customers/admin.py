from django.contrib import admin
from .models import CustomerProfile, MedicalHistory

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'cedula', 'nombres', 'apellidos',
        'telefono', 'ciudad', 'zona',
        'ubicacion_mapa',   # ← campo nuevo
        'registrado_por', 'fecha_registro'
    )
    search_fields = (
        'cedula', 'nombres', 'apellidos',
        'telefono', 'email', 'ciudad__nombre',
        'ubicacion_mapa'    # ← incluye en búsqueda
    )
    list_filter = ('ciudad', 'fecha_registro', 'registrado_por')

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'descripcion', 'fecha_registro')
    search_fields = ('customer__cedula', 'customer__nombres')
    list_filter = ('fecha_registro',)
