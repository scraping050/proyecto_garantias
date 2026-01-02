@echo off
echo ===================================================
echo   INICIANDO SISTEMA DE GARANTIAS SEACE (AURA)
echo ===================================================

echo [1/2] Iniciando Backend Server (Puerto 5000)...
start "BACKEND - API Garantias" /D "c:\laragon\www\proyecto_garantias\backend" npm run dev

echo [2/2] Iniciando Frontend Dashboard (Next.js)...
start "FRONTEND - Dashboard" /D "c:\laragon\www\proyecto_garantias\free-nextjs-admin-dashboard-main" npm run dev

echo ===================================================
echo   SERVICIOS INICIADOS
echo   - Backend: http://localhost:5000
echo   - Frontend: http://localhost:3000 (o similar)
echo ===================================================
echo.
echo Por favor no cierres las ventanas negras que aparecieron.
echo Si el backend muestra error de API Key, revisa tu archivo .env
echo.
pause
