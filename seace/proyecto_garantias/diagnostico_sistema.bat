@echo off
echo ========================================
echo   DIAGNOSTICO - Sistema Garantias SEACE
echo ========================================
echo.

echo [1/5] Verificando Node.js...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js no esta instalado
    pause
    exit /b 1
)
echo OK - Node.js instalado
echo.

echo [2/5] Verificando proceso Node corriendo...
tasklist /FI "IMAGENAME eq node.exe" 2>NUL | find /I /N "node.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo OK - Proceso Node.js detectado
) else (
    echo ADVERTENCIA: No se detecta proceso Node.js corriendo
)
echo.

echo [3/5] Verificando puertos...
netstat -ano | findstr :5000
if %errorlevel% equ 0 (
    echo OK - Puerto 5000 en uso (Backend)
) else (
    echo ADVERTENCIA: Puerto 5000 NO en uso - Backend no esta corriendo
)

netstat -ano | findstr :5173
if %errorlevel% equ 0 (
    echo OK - Puerto 5173 en uso (Frontend)
) else (
    echo ADVERTENCIA: Puerto 5173 NO en uso - Frontend no esta corriendo
)
echo.

echo [4/5] Verificando archivos de configuracion...
if exist "backend\.env" (
    echo OK - backend\.env existe
) else (
    echo ERROR: backend\.env NO existe
    echo Crear archivo backend\.env con:
    echo DB_HOST=localhost
    echo DB_USER=root
    echo DB_PASSWORD=123456789
    echo DB_NAME=garantias_seace
    echo PORT=5000
)

if exist "backend\node_modules" (
    echo OK - backend\node_modules existe
) else (
    echo ADVERTENCIA: backend\node_modules NO existe - Ejecutar: cd backend ^&^& npm install
)

if exist "frontend\node_modules" (
    echo OK - frontend\node_modules existe
) else (
    echo ADVERTENCIA: frontend\node_modules NO existe - Ejecutar: cd frontend ^&^& npm install
)
echo.

echo [5/5] Probando conexion a MySQL...
echo Intentando conectar a garantias_seace...
python -c "import mysql.connector; conn = mysql.connector.connect(host='localhost', user='root', password='123456789', database='garantias_seace'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM Licitaciones_Cabecera'); total = cursor.fetchone()[0]; print(f'OK - Base de datos conectada. Total registros: {total}'); conn.close()" 2>NUL
if %errorlevel% neq 0 (
    echo ERROR: No se pudo conectar a MySQL
    echo Verificar que Laragon este corriendo y MySQL activo
)
echo.

echo ========================================
echo   DIAGNOSTICO COMPLETADO
echo ========================================
echo.
echo SIGUIENTE PASO:
echo 1. Si backend NO esta corriendo: cd backend ^&^& npm run dev
echo 2. Si frontend NO esta corriendo: cd frontend ^&^& npm run dev
echo 3. Abrir navegador en: http://localhost:5173
echo.
pause
