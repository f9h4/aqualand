# Generated migration to create default superuser

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_default_superuser(apps, schema_editor):
    """Create default superuser if it doesn't exist"""
    User = apps.get_model('auth', 'User')
    
    # Create superuser admin if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            email='admin@aqualand.com',
            password=make_password('admin'),
            is_superuser=True,
            is_staff=True,
            is_active=True
        )


def reverse_operation(apps, schema_editor):
    """Reverse operation - optional"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('aqualand_app', '0006_alter_region_cobertura_agua_alter_region_nombre'),
    ]

    operations = [
        migrations.RunPython(create_default_superuser, reverse_operation),
    ]
