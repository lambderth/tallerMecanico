from django import forms
from .models import HistorialReparacion, Vehiculo

class HistorialReparacionForm(forms.ModelForm):
    class Meta:
        model = HistorialReparacion
        fields = ['tipo_reparacion', 'descripcion_trabajo', 'costo_piezas', 'costo_mano_obra']
        widgets = {
            'tipo_reparacion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_trabajo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'costo_piezas': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_mano_obra': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ["nombre_cliente", "telefono_cliente", "email_cliente",
                  "marca", "modelo", "anio", "placa"]
        widgets = {
            "nombre_cliente": forms.TextInput(attrs={"class": "form-control"}),
            "telefono_cliente": forms.TextInput(attrs={"class": "form-control"}),
            "email_cliente": forms.EmailInput(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "modelo": forms.TextInput(attrs={"class": "form-control"}),
            "anio": forms.NumberInput(attrs={"class": "form-control", "min": 1900, "max": 2100}),
            "placa": forms.TextInput(attrs={"class": "form-control"}),
        }