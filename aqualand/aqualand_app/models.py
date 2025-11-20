from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Region(models.Model):
    nombre = models.CharField(max_length=9999999999)
    cobertura_agua = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(99999999999)],
        help_text="Porcentaje de cobertura de agua potable"
    )

    def __str__(self):
        return self.nombre

class Incidencia(models.Model):
    TIPO_CHOICES = [
        ('CORTE', 'Corte de Agua'),
        ('FUGA', 'Fuga de Agua'),
        ('CALIDAD', 'Problema de Calidad'),
        ('OTROS', 'Otros Problemas'),
    ]
    
    ESTADO_CHOICES = [
        ('REPORTADO', 'Reportado'),
        ('EN_PROCESO', 'En Proceso'),
        ('RESUELTO', 'Resuelto'),
        ('CANCELADO', 'Cancelado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='REPORTADO')
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    direccion = models.CharField(max_length=500)
    ubicacion_lat = models.FloatField(null=True, blank=True)
    ubicacion_lng = models.FloatField(null=True, blank=True)
    imagen = models.ImageField(upload_to='incidencias/', null=True, blank=True)
    reportado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incidencias_reportadas')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.titulo}"

class SistemaAPR(models.Model):
    nombre = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    ubicacion_lat = models.FloatField()
    ubicacion_lng = models.FloatField()
    poblacion_atendida = models.IntegerField()
    fecha_registro = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class EstadisticaServicio(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    fecha = models.DateField()
    cobertura_urbana = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    cobertura_rural = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    usuarios_afectados = models.IntegerField(default=0)
    incidencias_mes = models.IntegerField(default=0)

    class Meta:
        unique_together = ['region', 'fecha']

    def __str__(self):
        return f"Estadísticas {self.region} - {self.fecha}"

class RecursoEducativo(models.Model):
    TIPO_CHOICES = [
        ('ARTICULO', 'Artículo'),
        ('VIDEO', 'Video'),
        ('INFOGRAFIA', 'Infografía'),
        ('DOCUMENTO', 'Documento'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='recursos_educativos/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
