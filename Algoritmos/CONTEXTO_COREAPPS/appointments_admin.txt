from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AppointmentStatus, Schedule, Appointment

@admin.register(AppointmentStatus)
class AppointmentStatusAdmin(admin.ModelAdmin):
    list_display    = ('nombre', 'descripcion')
    search_fields   = ('nombre',)
    ordering        = ('nombre',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display    = ('enfermero', 'fecha', 'hora_inicio', 'hora_fin', 'disponible')
    list_filter     = ('enfermero', 'fecha', 'disponible')
    search_fields   = ('enfermero__nombres',)
    date_hierarchy  = 'fecha'
    raw_id_fields   = ('enfermero',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'paciente',
        'servicio',
        'enfermero',
        'horario',
        'hora',
        'estado',
        'tipo_ubicacion',  # Nuevo campo en admin
        'ubicacion',
        'mapa_ubicacion', 
        'doctor_name',
        'diagnosis', # Añadido aquí también
        'asignado_por',
        'fecha_creacion',
    )
    list_filter     = (
        'estado',
        'enfermero',  # ← nuevo campo aquí
        'horario__fecha',
        'horario__enfermero',
        'asignado_por',
    )
    search_fields   = (
        'paciente__nombres',
        'servicio__nombre',
        'asignado_por__email',
        'enfermero__email',  # ← puedes buscar por email del enfermero
    )
    date_hierarchy  = 'horario__fecha'
    raw_id_fields   = (
        'paciente',
        'servicio',
        'producto',
        'horario',
        'estado',
        'asignado_por',
        'enfermero',  # ← nuevo campo aquí
    )
    #filter_horizontal = ('producto',)  # ← Esto activa un widget útil para seleccionar productos M2M
    fieldsets = (
    (None, {
        'fields': (
                'paciente',
                'enfermero',
                'servicio',
                'producto',
                'tipo_ubicacion',
                'ubicacion',
                'mapa_ubicacion',  # Añadido aquí también
                'horario',
                'hora',
                'estado',
                'asignado_por',
                'notas',
                'doctor_name',
                'diagnosis',
            )
        }),
        (_('Tiempos'), {
            'fields': ('fecha_creacion', 'fecha_modifica'),
        }),
    )
    readonly_fields = ('fecha_creacion', 'fecha_modifica')
