# 🆘 Guía Rápida de Troubleshooting para Railway

## ¿La aplicación se cae?

### Paso 1: Revisar los logs en Railway
1. Ve a tu proyecto en railway.app
2. Haz clic en la pestaña "Logs"
3. Busca mensajes de error rojo

### Paso 2: Verificar variables de entorno
En Railway, asegúrate de tener configuradas:
```
SECRET_KEY=tu-clave-secreta
DEBUG=False
ALLOWED_HOSTS=*.up.railway.app,*.railway.app
```

### Paso 3: Ejecutar diagnóstico local
```bash
cd aqualand
python diagnose_railway.py
```

---

## Problemas Comunes

### ❌ Error: "No module named 'dj_database_url'"
**Solución**: Ya está arreglado con try/except. Si persiste, verifica que todas las dependencias estén en `requirements.txt`

### ❌ Error: "Connection refused" (BD)
**Solución**: Railway proporciona automáticamente `DATABASE_URL`. Si no aparece:
1. Ve a "Services" → "PostgreSQL"
2. Copia la URL de conexión
3. Agrega a variables de entorno como `DATABASE_URL`

### ❌ Error 500: "StaticFiles not found"
**Solución**: Ya se ejecuta `collectstatic` en el release. Si persiste:
```bash
heroku run python manage.py collectstatic --noinput
```

### ❌ Error: "CSRF verification failed"
**Solución**: Verifica que `CSRF_TRUSTED_ORIGINS` esté configurado correctamente en `settings.py`

### ❌ Páginas que cargan lentamente
**Solución**: El problema puede ser la BD. Verifica:
1. Los logs en Railway
2. Que no haya queries N+1 en vistas

### ❌ Errores de permisos en archivos
**Solución**: Railway usa volúmenes efímeros. Para imágenes, usa:
- AWS S3 (recomendado)
- O sube archivos a BD como BLOBs

---

## 🔧 Reparaciones Implementadas

### ✅ Manejo de errores en vistas
- Agregué try/except en `estadisticas()`
- Ahora redirige a home en caso de error

### ✅ Logging mejorado
- Configuré logging a console (Railway muestra esto)
- Nivel INFO por defecto

### ✅ Procfile optimizado
- Agregué `--log-level info` a gunicorn
- Aumenté timeout a 60s

### ✅ Variables de entorno
- ALLOWED_HOSTS acepta wildcards correctamente
- Fallback a SQLite si no hay DATABASE_URL

### ✅ WSGI mejorado
- Ahora loguea errores de inicialización

---

## 📊 Script de Diagnóstico

Localizado en `aqualand/diagnose_railway.py`

Ejecuta:
```bash
cd aqualand
python diagnose_railway.py
```

Verifica:
- ✓ Variables de entorno
- ✓ Conexión a BD
- ✓ Estado de migraciones
- ✓ Archivos estáticos
- ✓ Configuración de seguridad
- ✓ Templates

---

## 🚀 Re-desplegar en Railway

Después de los cambios:

1. **Local**: 
   ```bash
   git push origin main
   ```

2. **En Railway**:
   - Se redeploya automáticamente
   - O: Haz clic en "Redeploy" en el dashboard

3. **Ver logs en vivo**:
   ```bash
   railway logs
   ```
   (con CLI de Railway instalada)

---

## 📱 Monitorear en Tiempo Real

1. Ve a railway.app
2. Proyecto → pestaña "Logs"
3. Selecciona "Real-time"
4. Abre tu app en otra ventana

---

## 🆘 Si nada funciona

1. Ejecuta el diagnóstico local:
   ```bash
   python aqualand/diagnose_railway.py
   ```

2. Revisa los logs completos en Railway

3. Crea un issue en GitHub con:
   - Mensaje de error exacto
   - Output del diagnóstico

---

## 📝 Checklist Pre-Despliegue

- [ ] `SECRET_KEY` configurada en Railway
- [ ] `DEBUG=False` en Railway
- [ ] `DATABASE_URL` configurada o PostgreSQL agregada
- [ ] `ALLOWED_HOSTS` contiene tu dominio
- [ ] Git push hecho
- [ ] Redeploy en Railway completado
- [ ] Logs sin errores rojos

---

**Última actualización**: 2 de diciembre, 2025
**Estado**: Todas las correcciones implementadas ✅
