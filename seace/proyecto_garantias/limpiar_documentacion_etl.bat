@echo off
echo ========================================
echo LIMPIEZA DE ARCHIVOS DE DOCUMENTACION
echo ========================================
echo.

echo Eliminando archivos de documentacion...

del /F /Q "GUIA_ETL_CONSORCIOS_2_PASADAS.md" 2>nul && echo [OK] GUIA_ETL_CONSORCIOS_2_PASADAS.md || echo [--] No encontrado
del /F /Q "PROTECCIONES_ETL_CONSORCIOS.md" 2>nul && echo [OK] PROTECCIONES_ETL_CONSORCIOS.md || echo [--] No encontrado
del /F /Q "REVISION_CODIGO_ETL.md" 2>nul && echo [OK] REVISION_CODIGO_ETL.md || echo [--] No encontrado
del /F /Q "VERIFICACION_EXHAUSTIVA_CODIGO.md" 2>nul && echo [OK] VERIFICACION_EXHAUSTIVA_CODIGO.md || echo [--] No encontrado
del /F /Q "EJECUTAR_ETL_PRODUCCION.md" 2>nul && echo [OK] EJECUTAR_ETL_PRODUCCION.md || echo [--] No encontrado
del /F /Q "VERIFICACION_PRE_PRODUCCION.md" 2>nul && echo [OK] VERIFICACION_PRE_PRODUCCION.md || echo [--] No encontrado
del /F /Q "PROBLEMA_RESUELTO.md" 2>nul && echo [OK] PROBLEMA_RESUELTO.md || echo [--] No encontrado

echo.
echo ========================================
echo LIMPIEZA COMPLETADA
echo ========================================
echo.
echo Archivos esenciales mantenidos:
echo  - 1_motor_etl\etl_consorcios_openai.py
echo  - 1_motor_etl\etl_consorcios_openai_retry.py
echo  - setup_auditoria_consorcios.py
echo  - generar_reporte_visual.py
echo.
pause
