@echo off
REM Script de configuración de variables de entorno - Versión CMD
REM Ejecutar como Administrador

echo ============================================================
echo  Configuracion de Variables de Entorno - Proyecto Garantias
echo ============================================================
echo.

echo Este script configurara las variables de entorno necesarias
echo Las variables se guardaran a nivel de USUARIO
echo.

REM Configuración de Base de Datos
echo 1. CONFIGURACION DE BASE DE DATOS
echo =================================
set /p DB_HOST="Host de MySQL [localhost]: "
if "%DB_HOST%"=="" set DB_HOST=localhost

set /p DB_USER="Usuario de MySQL [root]: "
if "%DB_USER%"=="" set DB_USER=root

set /p DB_PASS="Contraseña de MySQL (NUEVA - minimo 16 caracteres): "

set /p DB_NAME="Nombre de la base de datos [garantias_seace]: "
if "%DB_NAME%"=="" set DB_NAME=garantias_seace

echo.

REM Configuración de Email
echo 2. CONFIGURACION DE EMAIL
echo =========================
set /p EMAIL_HOST="Servidor SMTP [smtp.gmail.com]: "
if "%EMAIL_HOST%"=="" set EMAIL_HOST=smtp.gmail.com

set /p EMAIL_PORT="Puerto SMTP [587]: "
if "%EMAIL_PORT%"=="" set EMAIL_PORT=587

set /p EMAIL_USER="Email de envio: "
set /p EMAIL_PASS="Contraseña de aplicacion Gmail (NUEVA): "
set /p EMAIL_TO="Email de destino para reportes: "

echo.

REM Configuración de IA
echo 3. CONFIGURACION DE IA
echo ======================
echo    Genera una nueva API key en: https://makersuite.google.com/app/apikey
set /p GEMINI_API_KEY="Google Gemini API Key (NUEVA): "

echo.
echo Guardando variables de entorno...

REM Guardar variables de entorno
setx GARANTIAS_DB_HOST "%DB_HOST%"
setx GARANTIAS_DB_USER "%DB_USER%"
setx GARANTIAS_DB_PASS "%DB_PASS%"
setx GARANTIAS_DB_NAME "%DB_NAME%"

setx GARANTIAS_EMAIL_HOST "%EMAIL_HOST%"
setx GARANTIAS_EMAIL_PORT "%EMAIL_PORT%"
setx GARANTIAS_EMAIL_USER "%EMAIL_USER%"
setx GARANTIAS_EMAIL_PASS "%EMAIL_PASS%"
setx GARANTIAS_EMAIL_TO "%EMAIL_TO%"

setx GARANTIAS_GEMINI_API_KEY "%GEMINI_API_KEY%"

echo.
echo ============================================================
echo  Variables de entorno configuradas correctamente
echo ============================================================
echo.

echo PROXIMOS PASOS:
echo.
echo 1. Actualiza la contraseña de MySQL:
echo    mysql -u %DB_USER% -p
echo    ALTER USER '%DB_USER%'@'localhost' IDENTIFIED BY '%DB_PASS%';
echo    FLUSH PRIVILEGES;
echo.
echo 2. Verifica la configuracion:
echo    python config\secrets_manager.py
echo.
echo 3. IMPORTANTE: Cierra y vuelve a abrir PowerShell/CMD
echo    para que las variables tomen efecto
echo.

pause
