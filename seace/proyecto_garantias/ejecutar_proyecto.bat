@echo off
REM Script para ejecutar el proyecto con variables de entorno configuradas
REM Establece las variables en la sesión actual y ejecuta el proyecto

echo ========================================
echo   Ejecutando Proyecto Garantias
echo ========================================
echo.

REM Establecer variables de entorno en la sesión actual
set GARANTIAS_DB_HOST=localhost
set GARANTIAS_DB_USER=root
set GARANTIAS_DB_PASS=123456789
set GARANTIAS_DB_NAME=garantias_seace
set GARANTIAS_EMAIL_HOST=smtp.gmail.com
set GARANTIAS_EMAIL_PORT=587
set GARANTIAS_EMAIL_USER=yanfrancochaupincsco@gmail.com
set GARANTIAS_EMAIL_PASS=yixe avpb errk sonp
set GARANTIAS_EMAIL_TO=yanfrancochaupincsco@gmail.com
set GARANTIAS_GEMINI_API_KEY=YOUR_API_KEY_HERE

echo Variables de entorno establecidas en sesion actual
echo.

REM Verificar configuración
echo Verificando configuracion...
python config\secrets_manager.py
if errorlevel 1 (
    echo.
    echo ERROR: La configuracion fallo
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Ejecutando Pipeline ETL
echo ========================================
echo.

REM Ejecutar el proyecto
cd 1_motor_etl
python main_auto.py

echo.
echo ========================================
echo   Ejecucion Completada
echo ========================================
pause
