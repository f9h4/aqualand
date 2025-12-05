# Generated migration to update superuser passwords

from django.db import migrations
from django.contrib.auth.hashers import make_password


def update_superuser_passwords(apps, schema_editor):
    """Update superuser passwords"""
    User = apps.get_model('auth', 'User')
    
    # Actualizar contraseña de Angel1
    try:
        User.objects.filter(username='Angel1').update(
            password=make_password('juan1234')
        )
    except:
        pass
    
    # Actualizar contraseña de Angel11
    try:
        User.objects.filter(username='Angel11').update(
            password=make_password('juan1234')
        )
    except:
        pass


def reverse_update_passwords(apps, schema_editor):
    """Reverse operation - this is irreversible for security"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('aqualand_app', '0004_add_default_regions'),
    ]

    operations = [
        migrations.RunPython(update_superuser_passwords, reverse_update_passwords),
    ]
