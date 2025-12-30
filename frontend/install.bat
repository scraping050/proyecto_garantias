@echo off
echo ========================================
echo SEACE Monitor - Frontend Installation
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Verificando Node.js...
node --version
if errorlevel 1 (
    echo ERROR: Node.js no esta instalado
    echo Por favor instala Node.js desde https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo [2/4] Instalando dependencias principales...
call npm install

echo.
echo [3/4] Instalando dependencias adicionales...
call npm install tailwindcss-animate next-themes

echo.
echo [4/4] Verificando instalacion...
call npm list --depth=0

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Para ejecutar el servidor de desarrollo:
echo   npm run dev
echo.
echo El frontend estara disponible en:
echo   http://localhost:3000
echo.
pause
