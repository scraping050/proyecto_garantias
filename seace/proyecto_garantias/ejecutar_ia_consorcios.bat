@echo off
REM Script para ejecutar solo el módulo de IA de consorcios
REM Establece las variables de entorno y ejecuta etl_consorcios_ai.py

echo ========================================
echo   Ejecutando Extraccion de Consorcios con IA
echo ========================================
echo.

REM Establecer variables de entorno en la sesión actual
set GARANTIAS_DB_HOST=localhost
set GARANTIAS_DB_USER=root
set GARANTIAS_DB_PASS=123456789
set GARANTIAS_DB_NAME=garantias_seace
set GARANTIAS_GEMINI_API_KEY=YOUR_API_KEY_HERE
set GARANTIAS_GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE

echo Variables de entorno configuradas
echo.
echo IMPORTANTE: Este proceso puede tardar varios minutos
echo debido a que debe:
echo   1. Descargar PDFs de contratos
echo   2. Analizar cada PDF con Google Gemini AI
echo   3. Extraer informacion de miembros de consorcios
echo.
echo Procesando 1,991 consorcios pendientes...
echo.

REM Ejecutar el módulo de IA (Gemini puede procesar PDFs escaneados)
cd 1_motor_etl
python etl_consorcios_ai.py

echo.
echo ========================================
echo   Proceso Completado
echo ========================================
pause
