from django import forms
from .models import Incidencia

class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ['titulo', 'descripcion', 'tipo', 'direccion', 'ubicacion_lat', 'ubicacion_lng', 'imagen', 'region']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion_lat': forms.HiddenInput(),
            'ubicacion_lng': forms.HiddenInput(),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título de la Incidencia',
            'descripcion': 'Descripción detallada',
            'tipo': 'Tipo de Incidencia',
            'direccion': 'Dirección',
            'region': 'Región',
            'imagen': 'Fotografía (opcional)',
        }
        help_texts = {
            'descripcion': 'Describe el problema con el mayor detalle posible.',
            'direccion': 'Ingresa la dirección completa donde ocurre la incidencia.',
            'imagen': 'Puedes adjuntar una fotografía de la incidencia.',
        }