#!/usr/bin/env python
"""
Script de validación para el proyecto Django - Aqualand
Verifica que todo esté correctamente configurado para Railway
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User

def check_requirements():
    """Verifica que todas las dependencias estén instaladas"""
    print("✓ Verificando dependencias...")
    required_packages = [
        'django',
        'rest_framework',
        'gunicorn',
        'whitenoise',
        'psycopg2',
        'dj_database_url',
        'Pillow'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - FALTA INSTALAR")
            return False
    return True

def check_database():
    """Verifica la conexión con la base de datos"""
    print("\n✓ Verificando base de datos...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("  ✓ Conexión a BD exitosa")
        return True
    except Exception as e:
        print(f"  ✗ Error en BD: {str(e)}")
        return False

def check_migrations():
    """Verifica que todas las migraciones estén aplicadas"""
    print("\n✓ Verificando migraciones...")
    try:
        call_command('migrate', '--check', verbosity=0)
        print("  ✓ Todas las migraciones están aplicadas")
        return True
    except Exception as e:
        print(f"  ✗ Migraciones pendientes: {str(e)}")
        return False

def check_settings():
    """Verifica configuraciones importantes"""
    print("\n✓ Verificando configuración...")
    checks = [
        ('SECRET_KEY', settings.SECRET_KEY != 'django-insecure-x7d3)*6q5i&*_w#_j02y=@&tl%i0h&pnc7^#t_v0stfqcr4i97'),
        ('DEBUG en producción', not settings.DEBUG),
        ('STATIC_ROOT', hasattr(settings, 'STATIC_ROOT')),
        ('MEDIA_ROOT', hasattr(settings, 'MEDIA_ROOT')),
        ('WhiteNoise instalado', 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE),
    ]
    
    all_good = True
    for check_name, result in checks:
        if result:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name}")
            all_good = False
    
    return all_good

def main():
    print("=" * 50)
    print("Validación del Proyecto Aqualand para Railway")
    print("=" * 50)
    
    results = []
    results.append(("Dependencias", check_requirements()))
    results.append(("Base de Datos", check_database()))
    results.append(("Migraciones", check_migrations()))
    results.append(("Configuración", check_settings()))
    
    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ Todo está listo para Railway")
        return 0
    else:
        print("\n✗ Hay problemas a resolver")
        return 1

if __name__ == '__main__':
    sys.exit(main())
