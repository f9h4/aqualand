from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets
from .models import Incidencia, Region, EstadisticaServicio, RecursoEducativo
from .forms import IncidenciaForm, CambiarEstadoIncidenciaForm
from .serializers import IncidenciaSerializer, RegionSerializer
from .services import NewsAPIService
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_http_methods

def is_admin(user):
    return user.is_staff

@require_http_methods(["GET", "HEAD"])
def health_check(request):
    """Endpoint para verificar que la aplicación está en línea"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({
            'status': 'healthy',
            'message': 'Aqualand is running'
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'message': str(e)
        }, status=503)

def home(request):
    """Página principal - accesible para todos"""
    if request.user.is_authenticated:
        incidencias = Incidencia.objects.all().order_by('-fecha_reporte')[:5]
        return render(request, 'aqualand_app/home.html', {
            'incidencias': incidencias
        })
    else:
        return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {username}!')
                if user.is_staff:
                    return redirect('admin_dashboard')
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'aqualand_app/login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('user_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'aqualand_app/registro.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, '¡Has cerrado sesión exitosamente!')
    return redirect('home')

@login_required
def user_dashboard(request):
    user_incidencias = Incidencia.objects.filter(reportado_por=request.user).order_by('-fecha_reporte')
    return render(request, 'aqualand_app/user_dashboard.html', {
        'incidencias': user_incidencias
    })

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_incidencias = Incidencia.objects.count()
    incidencias_pendientes = Incidencia.objects.filter(estado='REPORTADO').count()
    incidencias_proceso = Incidencia.objects.filter(estado='EN_PROCESO').count()
    incidencias_resueltas = Incidencia.objects.filter(estado='RESUELTO').count()
    
    ultimas_incidencias = Incidencia.objects.all().order_by('-fecha_reporte')[:10]
    
    return render(request, 'aqualand_app/admin_dashboard.html', {
        'total_incidencias': total_incidencias,
        'incidencias_pendientes': incidencias_pendientes,
        'incidencias_proceso': incidencias_proceso,
        'incidencias_resueltas': incidencias_resueltas,
        'ultimas_incidencias': ultimas_incidencias
    })

@login_required
def reportar_incidencia(request):
    if request.method == 'POST':
        form = IncidenciaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                incidencia = form.save(commit=False)
                incidencia.reportado_por = request.user
                
                # Validar coordenadas
                if not incidencia.ubicacion_lat or not incidencia.ubicacion_lng:
                    messages.error(request, 'Por favor, selecciona una ubicación en el mapa.')
                    return render(request, 'aqualand_app/reportar_incidencia.html', {'form': form})
                
                incidencia.save()
                messages.success(request, '¡Incidencia reportada exitosamente!')
                return redirect('detalle_incidencia', incidencia_id=incidencia.id)
            except Exception as e:
                messages.error(request, f'Error al guardar la incidencia: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = IncidenciaForm()
    
    return render(request, 'aqualand_app/reportar_incidencia.html', {'form': form})

def lista_incidencias(request):
    incidencias = Incidencia.objects.all().order_by('-fecha_reporte')
    return render(request, 'aqualand_app/lista_incidencias.html', {
        'incidencias': incidencias
    })

def detalle_incidencia(request, incidencia_id):
    incidencia = get_object_or_404(Incidencia, pk=incidencia_id)
    return render(request, 'aqualand_app/detalle_incidencia.html', {
        'incidencia': incidencia
    })

def mapa_incidencias(request):
    return render(request, 'aqualand_app/mapa_incidencias.html')

def recursos_educativos(request):
    recursos = RecursoEducativo.objects.all().order_by('-fecha_publicacion')
    return render(request, 'aqualand_app/recursos_educativos.html', {
        'recursos': recursos
    })

def estadisticas(request):
    try:
        # Obtener todas las regiones
        regiones = Region.objects.all()
        
        # Datos para el gráfico de cobertura por región
        cobertura_data = {
            'labels': [region.nombre for region in regiones] if regiones.exists() else ['Sin datos'],
            'datasets': [{
                'label': 'Cobertura de Agua Potable (%)',
                'data': [region.cobertura_agua for region in regiones] if regiones.exists() else [0],
                'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }]
        }
        
        # Crear diccionario de tipos para búsqueda rápida
        tipos_dict = dict(Incidencia.TIPO_CHOICES)
        
        # Estadísticas de incidencias por tipo
        tipos_incidencias = Incidencia.objects.values('tipo').annotate(
            total=Count('id')
        ).order_by('tipo')
        
        tipos_labels = [tipos_dict.get(tipo['tipo'], tipo['tipo']) for tipo in tipos_incidencias]
        tipos_data_values = [tipo['total'] for tipo in tipos_incidencias]
        
        tipos_data = {
            'labels': tipos_labels if tipos_labels else ['Sin incidencias'],
            'datasets': [{
                'data': tipos_data_values if tipos_data_values else [0],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)'
                ]
            }]
        }
    
        # Estadísticas de últimos 30 días
        fecha_inicio = timezone.now() - timedelta(days=30)
        incidencias_mes = Incidencia.objects.filter(
            fecha_reporte__gte=fecha_inicio
        ).values('fecha_reporte__date').annotate(
            total=Count('id')
        ).order_by('fecha_reporte__date')
        
        tendencia_data = {
            'labels': [str(item['fecha_reporte__date']) for item in incidencias_mes] if incidencias_mes.exists() else ['Sin datos'],
            'datasets': [{
                'label': 'Incidencias Reportadas',
                'data': [item['total'] for item in incidencias_mes] if incidencias_mes.exists() else [0],
                'borderColor': 'rgba(75, 192, 192, 1)',
                'fill': False
            }]
        }
        
        # Resumen de estadísticas
        total_incidencias = Incidencia.objects.count()
        incidencias_activas = Incidencia.objects.filter(
            estado__in=['REPORTADO', 'EN_PROCESO']
        ).count()
        incidencias_resueltas = Incidencia.objects.filter(
            estado='RESUELTO'
        ).count()
        
        context = {
            'cobertura_data': cobertura_data,
            'tipos_data': tipos_data,
            'tendencia_data': tendencia_data,
            'total_incidencias': total_incidencias,
            'incidencias_activas': incidencias_activas,
            'incidencias_resueltas': incidencias_resueltas,
            'porcentaje_resueltas': (incidencias_resueltas / total_incidencias * 100) if total_incidencias > 0 else 0
        }
        
        return render(request, 'aqualand_app/estadisticas.html', context)
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en vista de estadísticas: {str(e)}", exc_info=True)
        messages.error(request, 'Error al cargar las estadísticas. Por favor, intenta más tarde.')
        return redirect('home')

class IncidenciaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Incidencia.objects.all().order_by('-fecha_reporte')
    serializer_class = IncidenciaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

@login_required
@user_passes_test(is_admin)
def editar_incidencia(request, incidencia_id):
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    
    if request.method == 'POST':
        form = IncidenciaForm(request.POST, request.FILES, instance=incidencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Incidencia actualizada exitosamente.')
            return redirect('admin_dashboard')
    else:
        form = IncidenciaForm(instance=incidencia)
    
    return render(request, 'aqualand_app/editar_incidencia.html', {
        'form': form,
        'incidencia': incidencia
    })

@login_required
@user_passes_test(is_admin)
def cambiar_estado_incidencia(request, incidencia_id):
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    
    if request.method == 'POST':
        form = CambiarEstadoIncidenciaForm(request.POST, instance=incidencia)
        if form.is_valid():
            nuevo_estado = form.cleaned_data.get('estado')
            estado_display = dict(Incidencia.ESTADO_CHOICES).get(nuevo_estado)
            incidencia = form.save()
            messages.success(request, f'Estado de la incidencia actualizado a: {estado_display}')
            return redirect('detalle_incidencia', incidencia_id=incidencia.id)
    else:
        form = CambiarEstadoIncidenciaForm(instance=incidencia)
    
    return render(request, 'aqualand_app/cambiar_estado_incidencia.html', {
        'form': form,
        'incidencia': incidencia
    })

@login_required
@user_passes_test(is_admin)
def eliminar_incidencia(request, incidencia_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
        
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    
    if request.method == 'POST':
        incidencia.delete()
        messages.success(request, 'Incidencia eliminada exitosamente.')
        return redirect('admin_dashboard')
    
    return render(request, 'aqualand_app/confirmar_eliminar_incidencia.html', {
        'incidencia': incidencia
    })

@require_http_methods(["GET"])
def api_noticias_agua(request):
    """API endpoint para obtener noticias sobre agua"""
    try:
        service = NewsAPIService()
        noticias = service.get_water_news(page_size=20)
        return JsonResponse(noticias, safe=False)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'articles': []
        }, status=500)

@require_http_methods(["GET"])
def api_buscar_noticias(request):
    """API endpoint para buscar noticias con palabras clave"""
    query = request.GET.get('q', '')
    
    if not query:
        return JsonResponse({
            'status': 'error',
            'message': 'Parámetro "q" requerido para búsqueda',
            'articles': []
        }, status=400)
    
    try:
        service = NewsAPIService()
        page_size = int(request.GET.get('pageSize', 20))
        sort_by = request.GET.get('sortBy', 'publishedAt')
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        
        noticias = service.search_everything(
            query=query,
            sort_by=sort_by,
            page_size=page_size,
            from_date=from_date,
            to_date=to_date
        )
        return JsonResponse(noticias, safe=False)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'articles': []
        }, status=500)

@require_http_methods(["GET"])
def api_titulares(request):
    """API endpoint para obtener titulares principales"""
    try:
        service = NewsAPIService()
        query = request.GET.get('q')
        category = request.GET.get('category')
        country = request.GET.get('country')
        page_size = int(request.GET.get('pageSize', 20))
        
        titulares = service.get_top_headlines(
            query=query,
            category=category,
            country=country,
            page_size=page_size
        )
        return JsonResponse(titulares, safe=False)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'articles': []
        }, status=500)
