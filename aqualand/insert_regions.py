#!/usr/bin/env python
"""
Script para insertar regiones predeterminadas de Chile en MySQL
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')
django.setup()

from aqualand_app.models import Region

# Crear regiones de Chile
regiones_data = [
    {'nombre': 'Arica y Parinacota', 'cobertura_agua': 88.5},
    {'nombre': 'Tarapacá', 'cobertura_agua': 82.3},
    {'nombre': 'Antofagasta', 'cobertura_agua': 85.7},
    {'nombre': 'Atacama', 'cobertura_agua': 80.2},
    {'nombre': 'Coquimbo', 'cobertura_agua': 78.9},
    {'nombre': 'Valparaíso', 'cobertura_agua': 86.4},
    {'nombre': 'Metropolitana', 'cobertura_agua': 91.2},
    {'nombre': 'Libertador General Bernardo O\'Higgins', 'cobertura_agua': 79.8},
    {'nombre': 'Maule', 'cobertura_agua': 77.5},
    {'nombre': 'Ñuble', 'cobertura_agua': 76.3},
    {'nombre': 'Biobío', 'cobertura_agua': 80.6},
    {'nombre': 'La Araucanía', 'cobertura_agua': 74.1},
    {'nombre': 'Los Ríos', 'cobertura_agua': 72.8},
    {'nombre': 'Los Lagos', 'cobertura_agua': 75.9},
    {'nombre': 'Aysén del General Carlos Ibáñez del Campo', 'cobertura_agua': 68.4},
    {'nombre': 'Magallanes y de la Antártica Chilena', 'cobertura_agua': 70.2},
]

print("Insertando regiones de Chile en MySQL...")
for region_data in regiones_data:
    region, created = Region.objects.get_or_create(**region_data)
    if created:
        print(f'✓ Región creada: {region.nombre}')
    else:
        print(f'- Región ya existe: {region.nombre}')

total = Region.objects.count()
print(f'\n✓ Total de regiones: {total}')
print("\n✓ Regiones guardadas exitosamente en MySQL")
