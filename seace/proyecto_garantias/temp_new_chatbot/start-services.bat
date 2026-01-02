@echo off
echo ====================================
echo  INICIANDO SERVICIOS - CHATBOT AURA
echo ====================================
echo.

REM Iniciar Backend (en nueva ventana)
echo [1/2] Iniciando Backend (FastAPI)...
start "AURA Backend" cmd /k "cd /d %~dp0 && uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul

REM Iniciar Frontend (en nueva ventana)
echo [2/2] Iniciando Frontend (Next.js)...
start "AURA Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ====================================
echo  SERVICIOS INICIADOS
echo ====================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul
