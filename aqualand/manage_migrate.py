#!/usr/bin/env python
"""
Script personalizado para migrar con MariaDB 10.4
Ignora el error de versión mínima requerida
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')

# Patch para ignorar el error de versión de MariaDB
from django.db.backends.mysql import base
original_check_db_version = base.DatabaseWrapper.check_database_version_supported

def patched_check_db_version(self):
    """Ignora el check de versión para MariaDB 10.4"""
    pass

base.DatabaseWrapper.check_database_version_supported = patched_check_db_version

django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
