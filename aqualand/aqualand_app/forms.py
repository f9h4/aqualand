from django import forms
from .models import Incidencia

class IncidenciaForm(forms.ModelForm):
    imagen = forms.ImageField(
        required=False,
        help_text='Puedes adjuntar una fotografía (máx. 5MB)',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    class Meta:
        model = Incidencia
        fields = ['titulo', 'descripcion', 'tipo', 'direccion', 'ubicacion_lat', 'ubicacion_lng', 'imagen', 'region']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Calle Principal 123'}),
            'ubicacion_lat': forms.HiddenInput(),
            'ubicacion_lng': forms.HiddenInput(),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resumen breve de la incidencia'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el problema detalladamente'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
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
        }
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            if imagen.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('La imagen no debe superar 5MB.')
        return imagen


class CambiarEstadoIncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'estado': 'Cambiar Estado',
        }