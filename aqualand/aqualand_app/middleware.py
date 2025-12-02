"""
Middleware personalizado para Aqualand
"""
import logging
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware:
    """Middleware para manejar errores no capturados"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.exception(f"Error no manejado: {str(e)}")
            return JsonResponse(
                {
                    'error': 'Error interno del servidor',
                    'message': str(e) if logger.root.level == logging.DEBUG else 'Error no identificado'
                },
                status=500
            )

class SecurityHeadersMiddleware:
    """Middleware para agregar headers de seguridad"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'no-referrer'
        
        return response
