# Script para iniciar todos los servicios del proyecto (Local Development)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "INICIANDO SERVICIOS DEL PROYECTO (LOCAL)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Iniciar Backend FastAPI
Write-Host "[1/2] Iniciando Backend FastAPI..." -ForegroundColor Yellow
$backendPath = "C:\laragon\www\BRAYAN\proyecto_garantias"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal
Write-Host "OK Backend iniciado en http://localhost:8000" -ForegroundColor Green

# 2. Iniciar Frontend Next.js
Write-Host "[2/2] Iniciando Frontend Next.js..." -ForegroundColor Yellow
$frontendPath = "C:\laragon\www\BRAYAN\proyecto_garantias\seace\proyecto_garantias\free-nextjs-admin-dashboard-main"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev" -WindowStyle Normal
Write-Host "OK Frontend iniciado en http://localhost:3000" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SERVICIOS LANZADOS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend API:   http://localhost:8000/docs" -ForegroundColor White
Write-Host "Frontend:      http://localhost:3000" -ForegroundColor White
