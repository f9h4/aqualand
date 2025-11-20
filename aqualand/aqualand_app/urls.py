from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('incidencias/reportar/', views.reportar_incidencia, name='reportar_incidencia'),
    path('incidencias/', views.lista_incidencias, name='lista_incidencias'),
    path('incidencias/<int:incidencia_id>/', views.detalle_incidencia, name='detalle_incidencia'),
    path('mapa/', views.mapa_incidencias, name='mapa_incidencias'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('recursos-educativos/', views.recursos_educativos, name='recursos_educativos'),
    path('api/incidencias/', views.IncidenciaViewSet.as_view({'get': 'list'}), name='api_incidencias'),
    path('incidencias/<int:incidencia_id>/editar/', views.editar_incidencia, name='editar_incidencia'),
    path('incidencias/<int:incidencia_id>/eliminar/', views.eliminar_incidencia, name='eliminar_incidencia'),
]
