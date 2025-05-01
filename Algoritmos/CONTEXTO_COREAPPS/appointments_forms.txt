from django import forms
from .models import Appointment
from CoreApps.catalog.models import Product
from django.forms.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from .models import Schedule

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        #fields = [
        #    'paciente',
        #    'servicio',
        #    'producto',
        #    'enfermero',
        #    'fecha',
        #    'hora',
        #    'estado',
        #    'notas',
        #]
        fields = [
            'paciente', 'servicio', 'producto',
            'tipo_ubicacion', 'ubicacion', 'mapa_ubicacion',  # Añade aquí
            'enfermero', 'fecha', 'hora', 'estado', 'notas',
        ]

        widgets = {
            #'paciente': forms.Select(attrs={'class': 'form-control'}),
            'servicio': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'tipo_ubicacion': forms.RadioSelect(),
            'ubicacion': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Dirección de la cita'
            }),
            'mapa_ubicacion': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enlace al mapa de Google'
            }),
            'doctor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del doctor'
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Diagnóstico médico'
            }),
            'enfermero': forms.Select(attrs={'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    def clean(self):
        cleaned_data = super().clean()
        enfermero = cleaned_data.get('enfermero')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        paciente  = cleaned_data.get('paciente')
        tipo_ubi  = cleaned_data.get('tipo_ubicacion')
        ubi       = cleaned_data.get('ubicacion')

        if enfermero and fecha and hora:
            try:
                horario = Schedule.objects.get(
                    enfermero=enfermero,
                    fecha=fecha,
                    hora_inicio__lte=hora,
                    hora_fin__gte=hora,
                    disponible=True
                )
                self.instance.horario = horario  # ← AQUÍ ASIGNAMOS ANTES DE VALIDAR EL MODELO
            except Schedule.DoesNotExist:
                raise forms.ValidationError("No se encontró un horario disponible para esta fecha y hora seleccionada.")

        if tipo_ubi == 'domicilio':
            if paciente and paciente.direccion and paciente.ubicacion_mapa:
                cleaned_data['ubicacion'] = paciente.direccion
                cleaned_data['mapa_ubicacion'] = paciente.ubicacion_mapa
                self.instance.ubicacion = paciente.direccion
                self.instance.mapa_ubicacion = paciente.ubicacion_mapa
            else:
                raise ValidationError("El cliente no tiene dirección o mapa registrados.")
        else:  # 'otro'
            if not ubi or not cleaned_data.get('mapa_ubicacion'):
                raise ValidationError("Debe indicar la ubicación y el enlace del mapa para la cita.")
            self.instance.ubicacion = ubi
            self.instance.mapa_ubicacion = cleaned_data['mapa_ubicacion']

        return cleaned_data

        

    #def clean(self):
    #    cleaned = super().clean()
    #    enfermero = cleaned.get('enfermero')
    #    fecha = cleaned.get('fecha')
    #    hora = cleaned.get('hora')
#
    #    if enfermero and fecha and hora:
    #        conflicto = Appointment.objects.filter(
    #            enfermero=enfermero,
    #            fecha=fecha,
    #            hora=hora
    #        )
    #        if self.instance.pk:
    #            conflicto = conflicto.exclude(pk=self.instance.pk)
#
    #        if conflicto.exists():
    #            raise ValidationError(
    #                f"Ya existe una cita asignada al enfermero {enfermero} el {fecha} a las {hora}.",
    #                code='duplicate_appointment'
    #            )
#
    #    return cleaned

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['fecha', 'hora_inicio', 'hora_fin']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }