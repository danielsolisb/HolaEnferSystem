from django import forms
from .models import Report, ConsentOrPrescription

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['appointment', 'ubicacion_gps', 'notas_novedades', 'valoracion']
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion_gps': forms.URLInput(attrs={'class': 'form-control'}),
            'notas_novedades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valoracion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }

class ConsentOrPrescriptionForm(forms.ModelForm):
    class Meta:
        model = ConsentOrPrescription
        fields = ['report', 'tipo', 'imagen_receta', 'firma_digital']
        widgets = {
            'report': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'imagen_receta': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'firma_digital': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
