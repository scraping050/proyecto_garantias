@echo off
title Backend - API SEACE Garantias
cd /d "%~dp0backend"

echo ================================================
echo   Iniciando Backend API
echo ================================================
echo.

REM Verificar si existe .env
if not exist ".env" (
    echo [CREANDO] Archivo .env...
    (
        echo DB_HOST=localhost
        echo DB_USER=root
        echo DB_PASSWORD=
        echo DB_NAME=garantias_seace
        echo PORT=5000
        echo NODE_ENV=development
    ) > .env
    echo [OK] Archivo .env creado
    echo.
)

echo [INFO] Iniciando servidor backend...
echo [INFO] Puerto: 5000
echo [INFO] Presiona Ctrl+C para detener
echo.

npm run dev
