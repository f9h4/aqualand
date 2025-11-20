from rest_framework import serializers
from .models import Incidencia, Region

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'nombre']

class IncidenciaSerializer(serializers.ModelSerializer):
    region_nombre = serializers.CharField(source='region.nombre', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Incidencia
        fields = [
            'id', 'titulo', 'descripcion', 'tipo', 'tipo_display',
            'estado', 'estado_display', 'fecha_reporte',
            'ubicacion_lat', 'ubicacion_lng', 'direccion', 'region', 'region_nombre'
        ]