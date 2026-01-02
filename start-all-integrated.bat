@echo off
echo ===================================================
echo   INICIANDO SISTEMA COMPLETO MCQS + SEACE
echo ===================================================

echo 1. Iniciando Backend Principal (Puerto 8000)...
start "Main Backend" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo 2. Iniciando Frontend Principal (Puerto 3000)...
start "Main Frontend" cmd /k "cd frontend && npm run dev"

echo 3. Iniciando Backend SEACE (Puerto 5000)...
start "SEACE Backend" cmd /k "cd seace\proyecto_garantias\backend && npm start"

echo 4. Iniciando Frontend SEACE (Puerto 3001)...
start "SEACE Frontend" cmd /k "cd seace\proyecto_garantias\free-nextjs-admin-dashboard-main && npm run dev -- -p 3001"

echo ===================================================
echo   TODOS LOS SERVICIOS INICIADOS
echo ===================================================
echo - Portal Principal: http://localhost:3000
echo - Dashboard SEACE:  http://localhost:3001
pause
