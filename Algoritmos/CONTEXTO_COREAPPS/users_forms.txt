from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para crear nuevos usuarios con nuestro modelo personalizado.
    """
    class Meta:
        model = User
        #fields = ('email', 'cedula', 'nombres', 'telefono', 'rol')
        fields = (
            'email','cedula','nombres','telefono',
            'rol','ciudad','zonas'
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['cedula'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cédula'})
        self.fields['nombres'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombres completos'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Número de teléfono'})
        self.fields['rol'].widget.attrs.update({'class': 'form-select'})
        self.fields['ciudad'].widget.attrs.update({'class':'form-select'})
        self.fields['zonas'].widget.attrs.update({'class':'form-select'})

class CustomUserChangeForm(UserChangeForm):
    """
    Formulario para actualizar usuarios con nuestro modelo personalizado.
    """
    class Meta:
        model = User
        #fields = ('email', 'cedula', 'nombres', 'telefono', 'rol')
        fields = (
            'email','cedula','nombres','telefono',
            'rol','ciudad','zonas'
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['cedula'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombres'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['rol'].widget.attrs.update({'class': 'form-select'})
        self.fields['ciudad'].widget.attrs.update({'class':'form-select'})
        self.fields['zonas'].widget.attrs.update({'class':'form-select'})