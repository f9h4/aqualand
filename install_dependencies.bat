@echo off
REM Script para instalar dependencias del proyecto Aqualand
REM Uso: install_dependencies.bat

echo ======================================
echo Instalando dependencias de Aqualand
echo ======================================
echo.

REM Verificar si pip está disponible
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip no está instalado o no está en el PATH
    exit /b 1
)

echo Actualizando pip...
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo ERROR: Fallo al actualizar pip
    exit /b 1
)

echo.
echo Instalando dependencias de requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Fallo al instalar dependencias
    exit /b 1
)

echo.
echo Verificando instalación de dj-database-url...
python -c "import dj_database_url; print('✓ dj-database-url instalado correctamente')"
if %errorlevel% neq 0 (
    echo ERROR: dj-database-url no se instaló correctamente
    echo Intentando instalar directamente...
    pip install dj-database-url==2.2.0
)

echo.
echo ======================================
echo ✓ Dependencias instaladas exitosamente
echo ======================================
