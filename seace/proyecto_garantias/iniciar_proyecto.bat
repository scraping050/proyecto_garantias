@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 INICIANDO PROYECTO SEACE
echo ========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "free-nextjs-admin-dashboard-main" (
    echo ❌ Error: No se encuentra la carpeta 'frontend'
    pause
    exit /b 1
)

if not exist "backend" (
    echo ❌ Error: No se encuentra la carpeta 'backend'
    pause
    exit /b 1
)

echo 🔍 Verificando instalación de dependencias...
echo.

REM Verificar backend
if not exist "backend\node_modules" (
    echo ⚠️  Backend: Dependencias no instaladas
    echo 📥 Instalando dependencias del backend...
    cd backend
    call npm install
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias del backend
        cd ..
        pause
        exit /b 1
    )
    cd ..
    echo ✅ Dependencias del backend instaladas
) else (
    echo ✅ Backend: Dependencias OK
)

REM Verificar frontend
if not exist "free-nextjs-admin-dashboard-main\node_modules" (
    echo ⚠️  Frontend: Dependencias no instaladas
    echo 📥 Instalando dependencias del frontend...
    cd free-nextjs-admin-dashboard-main
    call npm install
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias del frontend
        cd ..
        pause
        exit /b 1
    )
    cd ..
    echo ✅ Dependencias del frontend instaladas
) else (
    echo ✅ Frontend: Dependencias OK
)

echo.
echo ========================================
echo 🎯 Selecciona el modo de ejecución:
echo ========================================
echo.
echo 1. Modo DESARROLLO (Backend + Frontend con hot-reload)
echo 2. Modo PRODUCCIÓN (Solo Backend, frontend compilado)
echo 3. Solo BACKEND (puerto 5000)
echo 4. Solo FRONTEND (puerto 5173)
echo 5. Salir
echo.
set /p opcion="Ingresa tu opción (1-5): "

if "%opcion%"=="1" goto desarrollo
if "%opcion%"=="2" goto produccion
if "%opcion%"=="3" goto solo_backend
if "%opcion%"=="4" goto solo_frontend
if "%opcion%"=="5" goto fin
echo ❌ Opción inválida
pause
exit /b 1

:desarrollo
echo.
echo 🔥 Iniciando en modo DESARROLLO...
echo.
echo 📌 Backend: http://localhost:5000
echo 📌 Frontend: http://localhost:5173
echo.
echo ⚠️  IMPORTANTE: Se abrirán 2 ventanas de terminal
echo    - NO cierres ninguna ventana mientras trabajes
echo    - Presiona Ctrl+C en cada ventana para detener
echo.
pause
start "SEACE Backend (Dev)" cmd /k "cd /d %~dp0backend && npm run dev"
timeout /t 3 /nobreak >nul
start "SEACE Frontend (Dev)" cmd /k "cd /d %~dp0free-nextjs-admin-dashboard-main && npm run dev"
echo.
echo ✅ Proyecto iniciado en modo desarrollo
echo.
goto fin

:produccion
echo.
echo 🏭 Iniciando en modo PRODUCCIÓN...
echo.
REM Verificar que existe el build
if not exist "free-nextjs-admin-dashboard-main\dist" (
    echo ⚠️  No se encontró el build del frontend
    echo 📦 Compilando frontend...
    cd free-nextjs-admin-dashboard-main
    call npm run build
    if errorlevel 1 (
        echo ❌ Error al compilar el frontend
        cd ..
        pause
        exit /b 1
    )
    cd ..
)
echo.
echo 📌 Backend: http://localhost:5000
echo 📌 Frontend compilado servido desde: free-nextjs-admin-dashboard-main\dist
echo.
start "SEACE Backend (Prod)" cmd /k "cd /d %~dp0backend && npm start"
echo.
echo ✅ Backend iniciado en modo producción
echo.
goto fin

:solo_backend
echo.
echo 🔧 Iniciando solo BACKEND...
echo.
echo 📌 Backend: http://localhost:5000
echo.
start "SEACE Backend" cmd /k "cd /d %~dp0backend && npm run dev"
echo.
echo ✅ Backend iniciado
echo.
goto fin

:solo_frontend
echo.
echo 🎨 Iniciando solo FRONTEND...
echo.
echo 📌 Frontend: http://localhost:5173
echo.
start "SEACE Frontend" cmd /k "cd /d %~dp0free-nextjs-admin-dashboard-main && npm run dev"
echo.
echo ✅ Frontend iniciado
echo.
goto fin

:fin
echo.
echo ========================================
echo 👋 Proceso completado
echo ========================================
pause
