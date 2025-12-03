# ⚠️ CONFIGURAR VARIABLES EN RAILWAY - PASO A PASO

## El Problema
La app no puede iniciar porque **falta decirle a Django dónde está PostgreSQL y qué clave secreta usar**.

## ✅ SOLUCIÓN EN 3 PASOS

### PASO 1: Abre Railway y tu proyecto
1. Ve a https://railway.app
2. Abre tu proyecto "aqualand"
3. En la parte superior, busca y **abre "Variables"** (o "Environment Variables")

### PASO 2: Agrega EXACTAMENTE estas 3 variables

Te mostraré dónde encontrar cada una y qué valor poner.

#### Variable #1: SECRET_KEY
```
Nombre:   SECRET_KEY
Valor:    django-insecure-clave-super-secreta-puede-ser-cualquier-cosa-aleatoria-12345
```
*(Este es solo un ejemplo. Puede ser cualquier texto largo y aleatorio)*

#### Variable #2: DEBUG  
```
Nombre:   DEBUG
Valor:    False
```
*(IMPORTANTE: Escribir así, con mayúscula)*

#### Variable #3: ALLOWED_HOSTS
```
Nombre:   ALLOWED_HOSTS
Valor:    *.up.railway.app,*.railway.app,localhost,127.0.0.1
```
*(IMPORTANTE: Sin espacios después de las comas)*

### PASO 3: Verifica que PostgreSQL existe

1. Mientras estés en Railway, abre la pestaña **"Services"**
2. Deberías ver:
   - ✓ Un servicio "web" (verde/azul - tu app Django)
   - ✓ Un servicio "PostgreSQL" (rojo/rosa - base de datos)
3. **SI NO VES PostgreSQL:**
   - Click en "+ Add Service"
   - Selecciona "Database" → "PostgreSQL"
   - Espera 2-3 minutos a que se cree

### PASO 4: Reinicia la app

1. En Railway, ve a **"Services"**
2. Abre el servicio **"web"**
3. Busca el botón "..." (tres puntos) en la parte superior derecha
4. Selecciona **"Restart"** o **"Redeploy"**
5. Espera 2-3 minutos

### PASO 5: Verifica que funciona

Abre en tu navegador (reemplaza `tu-app` con tu ID de Railway):
```
https://tu-app.up.railway.app/health/
```

**Deberías ver:**
```json
{
  "status": "healthy",
  "message": "Aqualand is running"
}
```

---

## 🐛 Si sigue sin funcionar

### Opción A: Ver los logs
1. En Railway, ve a la pestaña **"Logs"**
2. Busca líneas con "ERROR" o "Exception"
3. **Copia las últimas 10-20 líneas y envíamelas**

### Opción B: Ejecuta el verificador local
En tu terminal:
```bash
cd aqualand
python ../verify_env_vars.py
```

---

## 📌 CHECKLISTA FINAL

- [ ] Fui a Railway.app y abrí mi proyecto
- [ ] Fui a "Variables" y agregué SECRET_KEY
- [ ] Agregué DEBUG = False
- [ ] Agregué ALLOWED_HOSTS = *.up.railway.app,*.railway.app,localhost
- [ ] Verifiqué que PostgreSQL existe en "Services"
- [ ] Hice click en "Restart" en el servicio "web"
- [ ] Esperé 2-3 minutos
- [ ] Probé https://tu-app.up.railway.app/health/ en el navegador
- [ ] Vi la respuesta JSON con "status": "healthy"

---

**Si no sabes tu URL de Railway:**
- En Railway, abre el servicio "web"
- Busca "Domain" o URL en la parte superior
- Se verá algo como: `aqualand-production-XXXX.up.railway.app`

Eso es tu URL. Usa ese dominio en lugar de `tu-app.up.railway.app`
