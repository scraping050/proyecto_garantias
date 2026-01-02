@echo off
chcp 65001 >nul
echo ========================================
echo 🏗️  COMPILACIÓN DEL PROYECTO SEACE
echo ========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "frontend" (
    echo ❌ Error: No se encuentra la carpeta 'frontend'
    echo    Asegúrate de ejecutar este script desde la raíz del proyecto
    pause
    exit /b 1
)

if not exist "backend" (
    echo ❌ Error: No se encuentra la carpeta 'backend'
    echo    Asegúrate de ejecutar este script desde la raíz del proyecto
    pause
    exit /b 1
)

echo 📦 Paso 1: Instalando dependencias del BACKEND...
echo ----------------------------------------
cd backend
if not exist "node_modules" (
    echo 📥 Instalando dependencias por primera vez...
    call npm install
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias del backend
        cd ..
        pause
        exit /b 1
    )
) else (
    echo ✅ Dependencias del backend ya instaladas
)
cd ..
echo.

echo 📦 Paso 2: Instalando dependencias del FRONTEND...
echo ----------------------------------------
cd frontend
if not exist "node_modules" (
    echo 📥 Instalando dependencias por primera vez...
    call npm install
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias del frontend
        cd ..
        pause
        exit /b 1
    )
) else (
    echo ✅ Dependencias del frontend ya instaladas
)
echo.

echo 🔨 Paso 3: Compilando FRONTEND (Vite Build)...
echo ----------------------------------------
call npm run build
if errorlevel 1 (
    echo ❌ Error al compilar el frontend
    cd ..
    pause
    exit /b 1
)
echo ✅ Frontend compilado exitosamente
cd ..
echo.

echo ========================================
echo ✅ COMPILACIÓN COMPLETADA
echo ========================================
echo.
echo 📁 Archivos compilados en: frontend\dist
echo.
echo 🚀 Próximos pasos:
echo    1. Iniciar el backend: cd backend ^&^& npm start
echo    2. El frontend compilado está en frontend\dist
echo.
echo 💡 Para desarrollo (sin compilar):
echo    - Backend: cd backend ^&^& npm run dev
echo    - Frontend: cd frontend ^&^& npm run dev
echo.
pause
