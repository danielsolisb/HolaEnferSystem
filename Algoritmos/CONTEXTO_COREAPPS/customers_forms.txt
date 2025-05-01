from django import forms
from .models import CustomerProfile, MedicalHistory

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        #fields = ['nombres', 'apellidos', 'cedula', 'telefono', 'email', 'direccion', 'ciudad', 'fecha_nacimiento']
        fields = [
            'nombres','apellidos','cedula','telefono','email','ciudad','zona',
            'direccion','ubicacion_mapa','fecha_nacimiento'
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(attrs={'class':'form-control'}),
            'zona':   forms.Select(attrs={'class':'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ubicacion_mapa': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://maps.google.com/…'
            }),
            #'ciudad': forms.Select(attrs={'class': 'form-control'}),  # Corrección aquí
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
