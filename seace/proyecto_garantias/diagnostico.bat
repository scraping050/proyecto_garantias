@echo off
echo ================================================
echo   Diagnostico del Sistema SEACE Garantias
echo ================================================
echo.

echo [1/5] Verificando MySQL...
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] MySQL esta corriendo
) else (
    echo [ERROR] MySQL NO esta corriendo
    echo        Por favor inicia Laragon
    pause
    exit /b 1
)

echo.
echo [2/5] Verificando archivo .env del backend...
if exist "backend\.env" (
    echo [OK] Archivo .env existe
) else (
    echo [CREANDO] Archivo .env...
    (
        echo DB_HOST=localhost
        echo DB_USER=root
        echo DB_PASSWORD=
        echo DB_NAME=garantias_seace
        echo PORT=5000
        echo NODE_ENV=development
    ) > backend\.env
    echo [OK] Archivo .env creado
)

echo.
echo [3/5] Verificando base de datos...
mysql -u root -e "USE garantias_seace;" 2>NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Base de datos 'garantias_seace' existe
) else (
    echo [ERROR] Base de datos 'garantias_seace' NO existe
    echo        Ejecuta: python crear_bd.py
    pause
    exit /b 1
)

echo.
echo [4/5] Probando conexion al backend...
curl -s http://localhost:5000/health >NUL 2>&1
if "%ERRORLEVEL%"=="0" (
    echo [OK] Backend esta respondiendo en puerto 5000
) else (
    echo [ADVERTENCIA] Backend NO esta respondiendo
    echo              Necesitas iniciar el backend manualmente
)

echo.
echo [5/5] Probando conexion al frontend...
curl -s http://localhost:5173 >NUL 2>&1
if "%ERRORLEVEL%"=="0" (
    echo [OK] Frontend esta respondiendo en puerto 5173
) else (
    echo [ADVERTENCIA] Frontend NO esta respondiendo
    echo              Necesitas iniciar el frontend manualmente
)

echo.
echo ================================================
echo   Diagnostico completado
echo ================================================
echo.
echo Para iniciar los servidores:
echo   1. Abre una terminal y ejecuta: cd backend ^&^& npm run dev
echo   2. Abre otra terminal y ejecuta: cd frontend ^&^& npm run dev
echo.
pause
