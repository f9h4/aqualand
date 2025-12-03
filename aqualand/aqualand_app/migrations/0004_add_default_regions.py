# Generated migration to add default regions

from django.db import migrations


def add_default_regions(apps, schema_editor):
    """Add default regions to the database"""
    Region = apps.get_model('aqualand_app', 'Region')
    
    default_regions = [
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
    
    for region_data in default_regions:
        Region.objects.get_or_create(**region_data)


def remove_default_regions(apps, schema_editor):
    """Remove default regions if migration is reversed"""
    Region = apps.get_model('aqualand_app', 'Region')
    default_region_names = [
        'Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama',
        'Coquimbo', 'Valparaíso', 'Metropolitana', 
        'Libertador General Bernardo O\'Higgins', 'Maule', 'Ñuble',
        'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos',
        'Aysén del General Carlos Ibáñez del Campo', 
        'Magallanes y de la Antártica Chilena'
    ]
    Region.objects.filter(nombre__in=default_region_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('aqualand_app', '0003_incidencia_direccion_alter_incidencia_ubicacion_lat_and_more'),
    ]

    operations = [
        migrations.RunPython(add_default_regions, remove_default_regions),
    ]
