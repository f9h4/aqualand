#!/usr/bin/env python
"""
Script de inicialización para Railway
Ejecuta migraciones y recolecta estáticos sin fallar si hay problemas
"""
import os
import sys
import django
from pathlib import Path
import logging

# Configure logging before Django setup
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')

try:
    django.setup()
except Exception as e:
    logger.error(f"Error al configurar Django: {str(e)}", exc_info=True)
    print(f"❌ Error al configurar Django: {str(e)}")
    sys.exit(1)

from django.core.management import call_command
from django.conf import settings

def run_migrations():
    """Ejecuta las migraciones"""
    try:
        print("📦 Ejecutando migraciones...")
        # Verificar conexión a BD primero
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            print("✓ Conexión a BD verificada")
        except Exception as db_error:
            print(f"⚠️  No se puede conectar a BD: {str(db_error)}")
            logger.warning(f"Continuando sin BD: {str(db_error)}")
        
        call_command('migrate', '--noinput', verbosity=1)
        print("✓ Migraciones completadas")
        return True
    except Exception as e:
        print(f"⚠️  Error en migraciones: {str(e)}")
        logger.warning(f"Error en migraciones (continuando): {str(e)}", exc_info=True)
        # No retornamos False porque no queremos bloquear la inicialización
        return True

def collect_static():
    """Recolecta archivos estáticos"""
    try:
        print("📁 Recolectando archivos estáticos...")
        call_command('collectstatic', '--noinput', verbosity=0)
        print("✓ Estáticos recolectados")
        return True
    except Exception as e:
        print(f"⚠️  Error recolectando estáticos: {str(e)}")
        logger.warning(f"Error recolectando estáticos (continuando): {str(e)}", exc_info=True)
        # Continuamos incluso si fallan los estáticos
        return True

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
    
    # Check environment first
    print("📋 Verificando configuración de Railway...")
    db_url = os.environ.get('DATABASE_URL')
    secret_key = os.environ.get('SECRET_KEY')
    
    if not db_url:
        print("⚠️  DATABASE_URL no está configurada en Railway")
        print("   La app usará SQLite como fallback")
    else:
        print(f"✓ DATABASE_URL detectada: {db_url[:50]}...")
    
    if not secret_key or secret_key.startswith('django-insecure'):
        print("⚠️  SECRET_KEY no configurada o usando default inseguro")
        print("   Configura una SECRET_KEY segura en Railway")
    else:
        print("✓ SECRET_KEY configurada")
    
    print()
    
    # Ejecutar en orden
    run_migrations()
    collect_static()
    create_superuser()
    
    print("\n" + "=" * 60)
    print("✓ Inicialización completada")
    print("=" * 60 + "\n")
    print("🌐 La aplicación debería estar disponible en:")
    print(f"   - https://tu-app.up.railway.app")
    print(f"   - https://tu-app.up.railway.app/health/ (verificar salud)")
    print()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"Error crítico en inicialización: {str(e)}", exc_info=True)
        print(f"\n❌ Error crítico: {str(e)}\n")
        sys.exit(1)
