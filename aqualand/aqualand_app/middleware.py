"""
Middleware personalizado para Aqualand
"""
import logging
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

class HealthCheckBypassMiddleware:
    """Middleware para permitir health checks y login sin validación estricta"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Normalize host for health checks and forms
        if request.path in ['/health/', '/login/', '/registro/', '/logout/']:
            if hasattr(request, 'META'):
                # Use localhost as fallback host
                host = request.META.get('HTTP_HOST', 'localhost')
                # If it looks like a Railway domain, keep it; otherwise normalize
                if host and ('railway' in host or 'localhost' in host or '127.0.0.1' in host):
                    pass  # Keep the original host
                else:
                    request.META['HTTP_HOST'] = 'localhost'
        
        response = self.get_response(request)
        return response

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

class CSRFFixMiddleware:
    """Middleware para arreglar problemas de CSRF en Railway"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Si viene de un dominio Railway, confiar en el CSRF token
        host = request.META.get('HTTP_HOST', '')
        if 'railway' in host.lower() or 'localhost' in host.lower():
            # Mark request as trusted for CSRF
            request.META['HTTP_X_FORWARDED_PROTO'] = 'https'
        
        response = self.get_response(request)
        return response

class SecurityHeadersMiddleware:
    """Middleware para agregar headers de seguridad"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de seguridad - menos restrictivos para desarrollo
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'  # Cambié de DENY a SAMEORIGIN
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'same-origin'  # Cambié de no-referrer
        
        return response
