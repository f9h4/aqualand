#!/usr/bin/env python
"""
Script para crear un superusuario (admin) en Aqualand
Uso: python create_admin.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    """Crea o verifica el usuario admin"""
    username = 'admin'
    email = 'admin@aqualand.com'
    password = 'admin123'  # CAMBIAR ESTO EN PRODUCCIÓN
    
    print("\n" + "=" * 60)
    print("👤 CREADOR DE USUARIO ADMIN - AQUALAND")
    print("=" * 60 + "\n")
    
    # Verificar si ya existe
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"✓ Usuario '{username}' ya existe")
        print(f"  - Email: {user.email}")
        print(f"  - Admin: {user.is_staff}")
        print(f"  - Superusuario: {user.is_superuser}")
        
        # Preguntar si cambiar contraseña
        response = input("\n¿Deseas cambiar la contraseña? (s/n): ").lower().strip()
        if response == 's':
            user.set_password(password)
            user.save()
            print(f"✓ Contraseña actualizada a: {password}")
    else:
        # Crear nuevo usuario
        print(f"Creando nuevo usuario...\n")
        try:
            user = User.objects.create_superuser(username, email, password)
            print(f"✅ Superusuario '{username}' creado exitosamente")
            print(f"\n📋 CREDENCIALES:")
            print(f"   Usuario: {username}")
            print(f"   Contraseña: {password}")
            print(f"   Email: {email}")
            print(f"\n⚠️  IMPORTANTE:")
            print(f"   1. Cambia la contraseña en la primera oportunidad")
            print(f"   2. En producción, usa una contraseña más segura")
            print(f"   3. Accede a: https://tu-app.up.railway.app/admin/")
        except Exception as e:
            print(f"❌ Error creando superusuario: {str(e)}")
            return False
    
    print("\n" + "=" * 60)
    print("✓ LISTO")
    print("=" * 60 + "\n")
    print("Acceso al admin:")
    print("  URL: https://tu-app.up.railway.app/admin/")
    print(f"  Usuario: {username}")
    print(f"  Contraseña: {password}\n")
    
    return True

if __name__ == '__main__':
    try:
        create_admin()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
