from django.contrib import admin
from .models import Report, ConsentOrPrescription

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'enfermero', 'fecha_hora_reporte', 'valoracion')
    search_fields = ('appointment__paciente__nombres', 'appointment__servicio__nombre', 'enfermero__nombres')
    list_filter = ('valoracion', 'fecha_hora_reporte')
    date_hierarchy = 'fecha_hora_reporte'
    raw_id_fields = ('appointment', 'enfermero')

@admin.register(ConsentOrPrescription)
class ConsentOrPrescriptionAdmin(admin.ModelAdmin):
    list_display = ('report', 'tipo', 'fecha_hora_creacion')
    search_fields = ('report__appointment__paciente__nombres', 'tipo')
    list_filter = ('tipo', 'fecha_hora_creacion')
    date_hierarchy = 'fecha_hora_creacion'
    raw_id_fields = ('report',)
