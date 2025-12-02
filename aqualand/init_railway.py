#!/usr/bin/env python
"""
Script de inicialización para Railway
Ejecuta migraciones y recolecta estáticos sin fallar si hay problemas
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def run_migrations():
    """Ejecuta las migraciones"""
    try:
        print("📦 Ejecutando migraciones...")
        call_command('migrate', '--noinput', verbosity=1)
        print("✓ Migraciones completadas")
        return True
    except Exception as e:
        print(f"⚠️  Error en migraciones: {str(e)}")
        logger.error(f"Error en migraciones: {str(e)}", exc_info=True)
        return False

def collect_static():
    """Recolecta archivos estáticos"""
    try:
        print("📁 Recolectando archivos estáticos...")
        call_command('collectstatic', '--noinput', verbosity=0)
        print("✓ Estáticos recolectados")
        return True
    except Exception as e:
        print(f"⚠️  Error recolectando estáticos: {str(e)}")
        logger.error(f"Error recolectando estáticos: {str(e)}", exc_info=True)
        return False

def create_superuser():
    """Crea un superusuario si no existe"""
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            print("👤 Creando superusuario admin...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✓ Superusuario admin creado")
            print("  Usuario: admin")
            print("  Contraseña: admin123")
            print("  (Cambia esto inmediatamente en producción)")
        else:
            print("✓ Superusuario admin ya existe")
        return True
    except Exception as e:
        print(f"⚠️  Error creando superusuario: {str(e)}")
        logger.error(f"Error creando superusuario: {str(e)}", exc_info=True)
        return False

def main():
    print("\n" + "=" * 60)
    print("🚀 Inicializando Aqualand en Railway")
    print("=" * 60 + "\n")
    
    # Ejecutar en orden
    run_migrations()
    collect_static()
    create_superuser()
    
    print("\n" + "=" * 60)
    print("✓ Inicialización completada")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"Error crítico en inicialización: {str(e)}", exc_info=True)
        sys.exit(1)
