@echo off
echo ====================================
echo  DETENIENDO SERVICIOS - CHATBOT AURA
echo ====================================
echo.

REM Detener todos los procesos de uvicorn (Backend)
echo [1/2] Deteniendo Backend (uvicorn)...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq AURA Backend*" 2>nul
if %errorlevel%==0 (
    echo Backend detenido correctamente.
) else (
    echo No se encontraron procesos de Backend activos.
)

REM Detener proceso de Node (Frontend)
echo [2/2] Deteniendo Frontend (npm/node)...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq AURA Frontend*" 2>nul
if %errorlevel%==0 (
    echo Frontend detenido correctamente.
) else (
    echo No se encontraron procesos de Frontend activos.
)

echo.
echo ====================================
echo  SERVICIOS DETENIDOS
echo ====================================
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
