from django import forms
from .models import Service, Product

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nombre', 'descripcion', 'precio', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nombre', 'descripcion', 'precio', 'cantidad_disponible', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
