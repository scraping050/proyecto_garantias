@echo off
REM Script para limpiar datos y recargar con estados originales

echo ========================================
echo   Limpiando y Recargando Datos
echo   Estados Originales (Sin Traducciones)
echo ========================================
echo.

REM Establecer variables de entorno
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

echo 1. Limpiando datos actuales...
python -c "import mysql.connector; conn = mysql.connector.connect(host='localhost', user='root', password='123456789', database='garantias_seace'); cursor = conn.cursor(); cursor.execute('DELETE FROM Licitaciones_Adjudicaciones'); cursor.execute('DELETE FROM Licitaciones_Cabecera'); cursor.execute('DELETE FROM control_cargas'); conn.commit(); print('OK - Datos limpiados'); conn.close()"

if errorlevel 1 (
    echo ERROR: No se pudieron limpiar los datos
    pause
    exit /b 1
)

echo.
echo 2. Recargando datos con estados originales...
echo    (Esto puede tardar 1-2 minutos)
echo.

cd 1_motor_etl
python main_auto.py

echo.
echo ========================================
echo   Proceso Completado
echo ========================================
echo.
echo Verificando resultados...
cd ..
python -c "import mysql.connector; conn = mysql.connector.connect(host='localhost', user='root', password='123456789', database='garantias_seace'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM Licitaciones_Cabecera'); print(f'Licitaciones: {cursor.fetchone()[0]:,}'); cursor.execute('SELECT COUNT(*) FROM Licitaciones_Adjudicaciones'); print(f'Adjudicaciones: {cursor.fetchone()[0]:,}'); conn.close()"

echo.
pause
