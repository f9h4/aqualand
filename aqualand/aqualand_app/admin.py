from django.contrib import admin
from .models import Region, Incidencia, SistemaAPR, EstadisticaServicio, RecursoEducativo

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cobertura_agua')
    search_fields = ('nombre',)
    list_filter = ('cobertura_agua',)

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'estado', 'fecha_reporte', 'region', 'reportado_por')
    list_filter = ('tipo', 'estado', 'region', 'fecha_reporte')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('fecha_reporte', 'fecha_actualizacion')
    date_hierarchy = 'fecha_reporte'

@admin.register(SistemaAPR)
class SistemaAPRAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region', 'poblacion_atendida', 'estado', 'fecha_registro')
    list_filter = ('region', 'estado', 'fecha_registro')
    search_fields = ('nombre',)
    date_hierarchy = 'fecha_registro'

@admin.register(EstadisticaServicio)
class EstadisticaServicioAdmin(admin.ModelAdmin):
    list_display = ('region', 'fecha', 'cobertura_urbana', 'cobertura_rural', 'usuarios_afectados')
    list_filter = ('region', 'fecha')
    date_hierarchy = 'fecha'

@admin.register(RecursoEducativo)
class RecursoEducativoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha_publicacion', 'autor')
    list_filter = ('tipo', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha_publicacion'
