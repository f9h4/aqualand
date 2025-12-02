#!/usr/bin/env python
"""
Pre-flight health check before WSGI app starts
Verifies critical environment and configuration
"""
import os
import sys
import django

# Set Django settings before anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')

print("\n" + "=" * 60)
print("🔍 PRE-FLIGHT HEALTH CHECK")
print("=" * 60 + "\n")

# Check 1: Environment Variables
print("1️⃣  Checking environment variables...")
required_vars = {
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'DEBUG': os.environ.get('DEBUG', 'False'),
    'ALLOWED_HOSTS': os.environ.get('ALLOWED_HOSTS'),
    'DATABASE_URL': os.environ.get('DATABASE_URL'),
    'PORT': os.environ.get('PORT', '8000'),
}

for var, value in required_vars.items():
    status = '✓' if value else '⚠️'
    print(f"   {status} {var}: {str(value)[:50]}..." if value and len(str(value)) > 50 else f"   {status} {var}: {value}")

# Check 2: Django Setup
print("\n2️⃣  Setting up Django...")
try:
    django.setup()
    print("   ✓ Django configured successfully")
except Exception as e:
    print(f"   ❌ Django setup failed: {str(e)}")
    sys.exit(1)

# Check 3: Database Connection
print("\n3️⃣  Checking database connection...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("   ✓ Database connection successful")
except Exception as e:
    print(f"   ⚠️  Database connection failed: {str(e)}")
    print("   (App will try to continue with fallback)")

# Check 4: Installed Apps
print("\n4️⃣  Checking installed apps...")
try:
    from django.apps import apps
    app_count = len(apps.get_app_configs())
    print(f"   ✓ {app_count} apps loaded successfully")
except Exception as e:
    print(f"   ❌ Error loading apps: {str(e)}")
    sys.exit(1)

# Check 5: URL Configuration
print("\n5️⃣  Checking URL configuration...")
try:
    from django.urls import reverse
    health_url = reverse('health_check')
    print(f"   ✓ Health check endpoint: /health/")
except Exception as e:
    print(f"   ⚠️  Error checking URLs: {str(e)}")

print("\n" + "=" * 60)
print("✓ PRE-FLIGHT CHECK COMPLETE")
print("=" * 60 + "\n")
