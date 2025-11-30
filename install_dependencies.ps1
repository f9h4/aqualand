# Script para instalar dependencias del proyecto Aqualand
# Uso: .\install_dependencies.ps1

Write-Host "======================================" -ForegroundColor Green
Write-Host "Instalando dependencias de Aqualand" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Verificar si pip está disponible
try {
    python -m pip --version | Out-Null
}
catch {
    Write-Host "ERROR: pip no está instalado o no está en el PATH" -ForegroundColor Red
    exit 1
}

Write-Host "Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Fallo al actualizar pip" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Instalando dependencias de requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Fallo al instalar dependencias" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Verificando instalación de dj-database-url..." -ForegroundColor Yellow
python -c "import dj_database_url; print('✓ dj-database-url instalado correctamente')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: dj-database-url no se instaló correctamente" -ForegroundColor Red
    Write-Host "Intentando instalar directamente..." -ForegroundColor Yellow
    pip install dj-database-url==2.2.0
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "✓ Dependencias instaladas exitosamente" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
