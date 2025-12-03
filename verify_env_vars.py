#!/usr/bin/env python
"""
Diagnóstico completo de variables de entorno para Aqualand
Muestra exactamente qué valores se están usando
"""
import os
import sys

print("\n" + "=" * 70)
print("🔍 DIAGNÓSTICO DE VARIABLES DE ENTORNO - AQUALAND")
print("=" * 70 + "\n")

# Variables que Django NECESITA
required_vars = {
    'SECRET_KEY': {
        'used_in': 'settings.py:26',
        'description': 'Clave secreta para Django',
        'critical': True
    },
    'DEBUG': {
        'used_in': 'settings.py:31',
        'description': 'Modo debug (True/False)',
        'critical': True
    },
    'ALLOWED_HOSTS': {
        'used_in': 'settings.py:35',
        'description': 'Hosts que Django acepta',
        'critical': True
    },
    'DATABASE_URL': {
        'used_in': 'settings.py:84',
        'description': 'URL de conexión a PostgreSQL',
        'critical': False  # Tiene fallback a SQLite
    },
    'DJANGO_LOG_LEVEL': {
        'used_in': 'settings.py:225',
        'description': 'Nivel de logging (DEBUG/INFO/WARNING)',
        'critical': False
    },
    'PORT': {
        'used_in': 'Procfile',
        'description': 'Puerto donde escucha la app',
        'critical': False
    }
}

print("VARIABLES DETECTADAS:\n")
print(f"{'VARIABLE':<20} {'VALOR':<50} {'ESTADO':<10}")
print("-" * 80)

critical_missing = []
warnings = []

for var_name, var_info in required_vars.items():
    value = os.environ.get(var_name)
    
    if value is None:
        status = "❌ FALTA"
        if var_info['critical']:
            critical_missing.append(var_name)
    elif value == "":
        status = "⚠️  VACÍA"
        warnings.append(f"  {var_name} está vacía pero debe tener valor")
    elif len(value) > 47:
        status = f"✓ SET"
        display_value = value[:45] + "..."
    else:
        status = "✓ SET"
        display_value = value
    
    display_value = value if value and len(value) <= 47 else (value[:45] + "..." if value else "(vacía)")
    print(f"{var_name:<20} {display_value:<50} {status:<10}")

print("\n" + "=" * 70)
print("📋 REPORTE:\n")

if critical_missing:
    print(f"🚨 CRÍTICO - Faltan {len(critical_missing)} variable(s) OBLIGATORIA(S):")
    for var in critical_missing:
        print(f"   ❌ {var}")
        print(f"      Usada en: {required_vars[var]['used_in']}")
        print(f"      Descripción: {required_vars[var]['description']}\n")
else:
    print("✓ Todas las variables críticas están configuradas\n")

if warnings:
    print(f"⚠️  ADVERTENCIAS ({len(warnings)}):")
    for warning in warnings:
        print(warning)
    print()

print("\n" + "=" * 70)
print("✅ PRÓXIMOS PASOS:")
print("=" * 70 + "\n")

if critical_missing:
    print("""
1. Abre Railway → Tu proyecto "aqualand"
2. Ve a la pestaña "Variables"
3. Agrega estas variables (EXACTAMENTE COMO APARECEN ABAJO):

""")
    for var in critical_missing:
        print(f"   Nombre: {var}")
        print(f"   Descripción: {required_vars[var]['description']}")
        if var == 'SECRET_KEY':
            print(f"   Valor: django-insecure-tu-clave-secreta-aqui-puede-ser-algo-aleatorio")
        elif var == 'DEBUG':
            print(f"   Valor: False")
        elif var == 'ALLOWED_HOSTS':
            print(f"   Valor: *.up.railway.app,*.railway.app,localhost")
        print()
    
    print("\n4. Haz click en 'Restart' en el servicio 'web'")
    print("5. Espera 2-3 minutos para redeploy")
    print("6. Ejecuta este script nuevamente para verificar")
else:
    print("Todas las variables están configuradas. Ahora:")
    print("1. Haz click en 'Restart' en el servicio 'web' de Railway")
    print("2. Espera 2-3 minutos")
    print("3. Prueba accediendo a: https://tu-app.up.railway.app/health/")

print("\n" + "=" * 70 + "\n")
