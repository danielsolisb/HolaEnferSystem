from django.contrib import admin
from .models import CustomerProfile, MedicalHistory

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ( 'nombres', 'apellidos', 'cedula','telefono', 'email', 'registrado_por', 'fecha_registro')
    search_fields = ('nombres', 'apellidos', 'cedula', 'telefono', 'email', 'registrado_por__email')
    list_filter = ('fecha_registro', 'registrado_por')

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'descripcion', 'fecha_registro')
    search_fields = ('customer__cedula', 'customer__nombres')
    list_filter = ('fecha_registro',)
