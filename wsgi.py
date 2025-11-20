"""
WSGI config for aqualand project - Root level
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')

application = get_wsgi_application()
