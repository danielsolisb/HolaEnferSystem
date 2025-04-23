from django import forms
from .models import Appointment
from CoreApps.catalog.models import Product
from django.forms.widgets import SelectDateWidget
from .models import Schedule

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'servicio',
            'producto',
            'enfermero',
            'horario',
            'hora',
            'estado',
            'notas',
        ]

        widgets = {
            #'paciente': forms.Select(attrs={'class': 'form-control'}),
            'servicio': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'enfermero': forms.Select(attrs={'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        horario = cleaned.get('horario')
        hora = cleaned.get('hora')

        if horario and hora:
            if hora < horario.hora_inicio or hora > horario.hora_fin:
                self.add_error(
                    'hora',
                    f"La hora seleccionada debe estar entre {horario.hora_inicio} y {horario.hora_fin}."
                )

        return cleaned

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['fecha', 'hora_inicio', 'hora_fin']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }