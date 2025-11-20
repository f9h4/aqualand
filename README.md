# Aqualand - Gestor de Reportes de Incidencias de Agua

Una aplicación web basada en Django para gestionar y visualizar reportes de incidencias relacionadas con el servicio de agua potable.

## Características

- 🔐 Autenticación de usuarios
- 📍 Mapa interactivo con ubicaciones de incidencias
- 📋 Formulario para reportar nuevas incidencias
- 🎯 Panel de administración para gestionar reportes
- 📊 Estadísticas de incidencias
- 🖼️ Subida de imágenes
- 🔍 Filtrado de incidencias por tipo y estado
- 📱 Interfaz responsive

## Requisitos Previos

- Python 3.13.7
- pip
- Git

## Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/usuario/aqualand.git
cd aqualand
```

2. **Crear un entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crea un archivo `.env` en la raíz del proyecto:
```
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

5. **Ejecutar migraciones**
```bash
python aqualand/manage.py migrate
```

6. **Crear superusuario**
```bash
python aqualand/manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python aqualand/manage.py runserver
```

Accede a la aplicación en `http://localhost:8000`

## Despliegue en Railway

1. **Preparar el repositorio**
```bash
git add .
git commit -m "Preparar para Railway"
git push origin main
```

2. **Configurar en Railway**
- Crear cuenta en [Railway.app](https://railway.app)
- Conectar tu repositorio de GitHub
- Configurar variables de entorno:
  - `SECRET_KEY`: Tu clave secreta
  - `DEBUG`: False
  - `ALLOWED_HOSTS`: Tu dominio de Railway
  - `DATABASE_URL`: Se configura automáticamente si usas PostgreSQL

3. **Desplegar**
- Railway detectará automáticamente que es una aplicación Django
- Ejecutará las migraciones automáticamente
- La aplicación estará disponible en tu URL de Railway

## Estructura del Proyecto

```
aqualand/
├── aqualand/
│   ├── settings.py       # Configuración principal
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── aqualand_app/
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Vistas
│   ├── forms.py          # Formularios
│   ├── urls.py           # URLs de la app
│   ├── templates/        # Plantillas HTML
│   └── migrations/       # Migraciones de BD
├── manage.py             # Script de Django
├── requirements.txt      # Dependencias
├── Procfile              # Configuración para Railway
└── runtime.txt           # Versión de Python
```

## Tecnologías Utilizadas

- **Backend**: Django 5.2.8
- **API**: Django REST Framework
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Frontend**: Bootstrap 5
- **Mapas**: Leaflet.js con OpenStreetMap
- **Servidor web**: Gunicorn + WhiteNoise

## Uso

### Para Usuarios
1. Registrarse o iniciar sesión
2. Ir a "Reportar Incidencia"
3. Completar el formulario con:
   - Título y descripción
   - Tipo de incidencia
   - Dirección
   - Ubicación en el mapa (hacer clic)
   - Fotografía (opcional)
4. Enviar el reporte

### Para Administradores
1. Acceder al panel de administración (`/admin/`)
2. Ver todos los reportes
3. Editar o eliminar reportes según sea necesario
4. Consultar estadísticas

## API REST

La aplicación incluye una API REST para acceder a los datos:

### Obtener todas las incidencias
```
GET /api/incidencias/
```

### Respuesta
```json
[
  {
    "id": 1,
    "titulo": "Corte de agua",
    "descripcion": "No hay agua desde las 8am",
    "tipo": "CORTE",
    "tipo_display": "Corte de Agua",
    "estado": "REPORTADO",
    "estado_display": "Reportado",
    "fecha_reporte": "2025-11-20T10:30:00Z",
    "ubicacion_lat": -33.4489,
    "ubicacion_lng": -70.6693,
    "direccion": "Calle Principal 123",
    "region": "Santiago",
    "region_nombre": "Metropolitana"
  }
]
```

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte, por favor crea un issue en el repositorio de GitHub.

---

**Hecho con ❤️ para mejorar la gestión del servicio de agua**
