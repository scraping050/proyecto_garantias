@echo off
title Frontend - Dashboard SEACE Garantias
cd /d "%~dp0free-nextjs-admin-dashboard-main"

echo ================================================
echo   Iniciando Frontend Dashboard
echo ================================================
echo.

echo [INFO] Iniciando servidor frontend...
echo [INFO] Puerto: 5173
echo [INFO] URL: http://localhost:5173
echo [INFO] Presiona Ctrl+C para detener
echo.

npm run dev
