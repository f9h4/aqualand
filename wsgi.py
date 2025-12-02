"""
WSGI config for aqualand project - Root level
"""
import os
import sys
import logging
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings')

logger = logging.getLogger(__name__)

try:
    application = get_wsgi_application()
    logger.info("Django WSGI application initialized successfully")
except Exception as e:
    logger.critical(f"Failed to initialize Django WSGI application: {str(e)}", exc_info=True)
    raise
