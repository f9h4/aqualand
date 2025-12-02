#!/usr/bin/env python
"""
Script de diagnóstico para Aqualand en Railway
Ejecuta este script para identificar problemas comunes
"""
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.db import connection
import logging

logger = logging.getLogger(__name__)

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_environment():
    """Verifica variables de entorno críticas"""
    print_header("🔍 VARIABLES DE ENTORNO")
    
    env_vars = {
        'SECRET_KEY': 'Configurada' if os.environ.get('SECRET_KEY') else 'FALTA',
        'DEBUG': os.environ.get('DEBUG', 'False'),
        'ALLOWED_HOSTS': os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,*.up.railway.app'),
        'DATABASE_URL': 'Configurada' if os.environ.get('DATABASE_URL') else 'FALTA (usando SQLite)',
    }
    
    for key, value in env_vars.items():
        status = "✓" if value != 'FALTA' else "✗"
        print(f"{status} {key}: {value}")

def check_database():
    """Verifica conexión a BD"""
    print_header("🗄️  BASE DE DATOS")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✓ Conexión a BD exitosa")
        
        # Verificar tablas críticas
        from django.apps import apps
        for app_config in apps.get_app_configs():
            print(f"  ✓ Aplicación '{app_config.name}' cargada")
        
        return True
    except Exception as e:
        print(f"✗ Error de BD: {str(e)}")
        return False

def check_migrations():
    """Verifica migraciones"""
    print_header("🔄 MIGRACIONES")
    
    try:
        # Verificar migraciones pendientes
        call_command('migrate', '--check', verbosity=0)
        print("✓ Todas las migraciones están aplicadas")
        return True
    except Exception as e:
        print(f"⚠️  Hay migraciones pendientes: {str(e)}")
        return False

def check_static_files():
    """Verifica archivos estáticos"""
    print_header("📁 ARCHIVOS ESTÁTICOS")
    
    static_root = Path(settings.STATIC_ROOT)
    media_root = Path(settings.MEDIA_ROOT)
    
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  {'✓' if static_root.exists() else '✗'} Directorio existe")
    
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"  {'✓' if media_root.exists() else '✗'} Directorio existe")
    
    # Contar archivos
    if static_root.exists():
        static_files = list(static_root.glob('**/*'))
        print(f"  └─ {len([f for f in static_files if f.is_file()])} archivos")

def check_templates():
    """Verifica templates"""
    print_header("📝 TEMPLATES")
    
    for tmpl_config in settings.TEMPLATES:
        dirs = tmpl_config.get('DIRS', [])
        app_dirs = tmpl_config.get('APP_DIRS', False)
        
        print(f"Backend: {tmpl_config.get('BACKEND')}")
        print(f"  APP_DIRS: {app_dirs}")
        
        for dir_path in dirs:
            dir_path = Path(dir_path)
            status = "✓" if dir_path.exists() else "✗"
            print(f"  {status} {dir_path}")

def check_installed_apps():
    """Verifica aplicaciones instaladas"""
    print_header("📦 APLICACIONES INSTALADAS")
    
    for app in settings.INSTALLED_APPS:
        print(f"  ✓ {app}")

def check_middleware():
    """Verifica middleware"""
    print_header("🔧 MIDDLEWARE")
    
    for middleware in settings.MIDDLEWARE:
        print(f"  ✓ {middleware}")

def check_security():
    """Verifica configuración de seguridad"""
    print_header("🔒 CONFIGURACIÓN DE SEGURIDAD")
    
    checks = {
        'DEBUG': (not settings.DEBUG, f"DEBUG = {settings.DEBUG}"),
        'SECRET_KEY segura': (len(settings.SECRET_KEY) > 20, f"Longitud: {len(settings.SECRET_KEY)}"),
        'SECURE_SSL_REDIRECT': (getattr(settings, 'SECURE_SSL_REDIRECT', False), f"= {getattr(settings, 'SECURE_SSL_REDIRECT', False)}"),
        'SESSION_COOKIE_SECURE': (getattr(settings, 'SESSION_COOKIE_SECURE', False), f"= {getattr(settings, 'SESSION_COOKIE_SECURE', False)}"),
        'CSRF_COOKIE_SECURE': (getattr(settings, 'CSRF_COOKIE_SECURE', False), f"= {getattr(settings, 'CSRF_COOKIE_SECURE', False)}"),
    }
    
    for check_name, (result, value) in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check_name}: {value}")

def check_logs():
    """Verifica logging"""
    print_header("📊 LOGGING")
    
    log_config = settings.LOGGING
    print(f"Handlers configurados: {', '.join(log_config.get('handlers', {}).keys())}")
    print(f"Loggers configurados: {', '.join(log_config.get('loggers', {}).keys())}")

def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " DIAGNÓSTICO DE AQUALAND EN RAILWAY ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = []
    results.append(("Variables de Entorno", check_environment()))
    results.append(("Base de Datos", check_database()))
    results.append(("Migraciones", check_migrations()))
    
    check_static_files()
    check_templates()
    check_installed_apps()
    check_middleware()
    check_security()
    check_logs()
    
    print_header("📋 RESUMEN")
    for name, passed in results:
        if passed is not None:
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{status} - {name}")
    
    print("\n")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error durante diagnóstico: {str(e)}", file=sys.stderr)
        logger.exception("Error en diagnóstico")
        sys.exit(1)
