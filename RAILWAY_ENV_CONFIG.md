# 🚨 CONFIGURACIÓN CRÍTICA DE RAILWAY - LECTURA OBLIGATORIA

## El Problema
La aplicación no responde en Railway. Esto es CASI SIEMPRE porque:

1. **Falta `DATABASE_URL`** - La app no puede conectarse a PostgreSQL
2. **Falta `SECRET_KEY`** - Django no puede inicializar
3. **Puerto no está configurado** - La app no escucha en el puerto correcto
4. **ALLOWED_HOSTS no incluye el dominio de Railway** - Rechaza las peticiones

## ✅ SOLUCIÓN: Configura estas Variables en Railway

### Paso 1: Abre tu proyecto en Railway
- Ve a https://railway.app
- Selecciona tu proyecto "aqualand"
- Abre la pestaña "Variables"

### Paso 2: Agregue ESTAS variables de entorno

**Opción A: Usar valores mínimos (RECOMENDADO PARA PRUEBAS)**
```
SECRET_KEY=django-insecure-tu-clave-secreta-aqui-puede-ser-cualquier-cosa
DEBUG=False
ALLOWED_HOSTS=*.up.railway.app,*.railway.app,localhost
PORT=8000
DJANGO_LOG_LEVEL=INFO
```

**Opción B: Valores seguros para producción (DESPUÉS DE PRUEBAS)**
```
# Generar una clave fuerte con: 
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

SECRET_KEY=tu-clave-generada-segura-aqui-[50+ caracteres aleatorios]
DEBUG=False
ALLOWED_HOSTS=tu-app.up.railway.app,tu-dominio-personalizado.com
PORT=8000
DJANGO_LOG_LEVEL=DEBUG
```

### Paso 3: Verifica la Base de Datos
1. En Railway, ve a "Services"
2. Deberías ver un servicio llamado "PostgreSQL" (verde = conectado)
3. Si NO existe PostgreSQL:
   - Click en "+ Add Service"
   - Selecciona "Database" → "PostgreSQL"
   - Espera a que se cree (1-2 minutos)
4. Una vez creado, Railway automáticamente configura `DATABASE_URL`

### Paso 4: Redeploy Manual
1. En Railway, abre tu proyecto "aqualand"
2. Busca el servicio "web"
3. Click en los "..." (tres puntos) → "Restart"
4. Espera 2-3 minutos para que se reinicie

## 🔍 Verificar que funciona

Después de redeploy, prueba ESTOS URLS en orden:

### 1️⃣ Verifica Health Check (sin login)
```
https://tu-app.up.railway.app/health/
```
**Esperas ver:**
```json
{
  "status": "healthy",
  "message": "Aqualand is running"
}
```

**Si ves error/timeout:**
- Railway aún está desplegando (espera 1-2 minutos más)
- O falta DATABASE_URL (ve al Paso 3)

### 2️⃣ Accede al Login
```
https://tu-app.up.railway.app/
```
**Esperas:**
- Página de login (formulario con Usuario/Contraseña)

### 3️⃣ Prueba acceso Admin
```
https://tu-app.up.railway.app/admin/
```
**Login con:**
- Usuario: `admin`
- Contraseña: `admin123`

## 🐛 Diagnóstico si sigue sin funcionar

### A. Ver los logs en Railway
1. Abre tu proyecto en Railway
2. Ve a la pestaña "Logs"
3. Busca mensajes con "ERROR" o "Exception"
4. Comparte los últimos 10-20 líneas conmigo

### B. Comandos para debug local

Puedes ejecutar estos en tu terminal local para ver si hay problemas:

```bash
# Dentro del directorio del proyecto
cd aqualand

# Ver si Django puede inicializar
python manage.py check

# Ver si puede conectar a BD
python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()
>>> print("✓ BD conecta OK")
>>> exit()

# Ver salud de la app
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqualand.settings'); from django.core.wsgi import get_wsgi_application; app = get_wsgi_application(); print('✓ WSGI app carga OK')"
```

## 📋 Lista de Verificación Final

- [ ] Entré a Railway.app y seleccioné el proyecto "aqualand"
- [ ] Fui a "Variables" y agregué SECRET_KEY
- [ ] Agregué ALLOWED_HOSTS
- [ ] Verifiqué que existe PostgreSQL en "Services"
- [ ] Hice click en "Restart" en el servicio web
- [ ] Esperé 2-3 minutos para redeploy
- [ ] Probé `/health/` y vi JSON response
- [ ] Accedí a `/` y vi login
- [ ] Entré a `/admin/` con admin/admin123

## ⚠️ SI NADA DE ESTO FUNCIONA

Ejecuta en tu terminal local:
```bash
cd aqualand
python health_check.py
```

Y comparte el output conmigo exactamente como aparece.

---

**Actualizado: 2025-12-02**
