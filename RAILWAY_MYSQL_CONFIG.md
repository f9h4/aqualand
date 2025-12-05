# Configuración de Railway MySQL para Aqualand

## Variables de Entorno Requeridas en Railway

Debes configurar las siguientes variables de entorno en tu proyecto de Railway:

### Opción 1: Usar DATABASE_URL (Recomendado)
```
DATABASE_URL=mysql://usuario:contraseña@mysql.railway.internal:3306/nombre_bd
```

### Opción 2: Variables Individuales
```
DB_ENGINE=django.db.backends.mysql
DB_NAME=aqualand_db
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=mysql.railway.internal
DB_PORT=3306
```

## Pasos para Configurar en Railway

1. **Ve al Dashboard de Railway**
   - Accede a https://railway.app/dashboard

2. **Selecciona tu Proyecto Aqualand**

3. **Ve a la pestaña "Variables"**

4. **Agregar la variable DATABASE_URL**
   - Click en "New Variable"
   - Nombre: `DATABASE_URL`
   - Valor: `mysql://usuario:contraseña@mysql.railway.internal:3306/aqualand_db`

## Credenciales de MySQL en Railway

Reemplaza en la CONNECTION STRING:
- `usuario`: Tu usuario de MySQL en Railway
- `contraseña`: Tu contraseña de MySQL en Railway
- `mysql.railway.internal`: Host (ya proporcionado)
- `3306`: Puerto (por defecto)
- `aqualand_db`: Nombre de la base de datos

## Ejemplo Completo

Si tus credenciales son:
- Usuario: `root`
- Contraseña: `miContraseña123`
- Base de datos: `aqualand_db`

La CONNECTION STRING sería:
```
DATABASE_URL=mysql://root:miContraseña123@mysql.railway.internal:3306/aqualand_db
```

## Después de Configurar

1. **Redeploy la aplicación**
   - Railway ejecutará automáticamente las migraciones
   - El superusuario admin se creará automáticamente

2. **Verificar la conexión**
   - Accede a `/admin/` con usuario: `admin`, contraseña: `admin`

3. **Las regiones de Chile se crearán automáticamente**
   - Durante el deployment, se ejecutará la migración que crea las 16 regiones

## Archivos Configurados

- `settings.py`: Detecta automáticamente `DATABASE_URL`
- `requirements.txt`: Contiene `dj-database-url` y `mysqlclient`
- Migraciones: Crean automáticamente tablas, superusuario y regiones

## Soporte

Si tienes problemas, verifica:
1. La CONNECTION STRING es correcta
2. MySQL está habilitado en Railway
3. Los credenciales son válidos
4. El host `mysql.railway.internal` es accesible
