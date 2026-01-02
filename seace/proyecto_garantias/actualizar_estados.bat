@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo 🔄 ACTUALIZACIÓN DE ESTADOS "DESCONOCIDO"
echo ============================================================
echo.
echo Este script actualizará los 3,575 registros "DESCONOCIDO"
echo a sus estados reales: EN_EVALUACION y CONVOCADO
echo.
echo Presiona Ctrl+C para cancelar, o
pause

echo.
echo 📊 Ejecutando actualización...
echo.

mysql -u root -p garantias_seace -e "UPDATE licitaciones_cabecera SET estado_proceso = 'EN_EVALUACION' WHERE estado_proceso = 'DESCONOCIDO' AND fecha_publicacion < CURDATE() - INTERVAL 7 DAY; UPDATE licitaciones_cabecera SET estado_proceso = 'CONVOCADO' WHERE estado_proceso = 'DESCONOCIDO' AND fecha_publicacion >= CURDATE() - INTERVAL 7 DAY; SELECT '✅ Actualización completada' as mensaje; SELECT estado_proceso, COUNT(*) as total FROM licitaciones_cabecera GROUP BY estado_proceso ORDER BY total DESC;"

echo.
echo ============================================================
echo ✅ PROCESO COMPLETADO
echo ============================================================
echo.
pause
