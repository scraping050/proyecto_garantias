# Script temporal para configurar variables de entorno con credenciales actuales
# IMPORTANTE: Estas son las credenciales ANTIGUAS que deben ser rotadas después

Write-Host "🔧 Configurando variables de entorno temporalmente..." -ForegroundColor Cyan
Write-Host "⚠️  IMPORTANTE: Estas son credenciales temporales que deben ser rotadas" -ForegroundColor Yellow
Write-Host ""

# Configuración de Base de Datos (desde .env actual)
[System.Environment]::SetEnvironmentVariable('GARANTIAS_DB_HOST', 'localhost', 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_DB_USER', 'root', 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_DB_PASS', '123456789', 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_DB_NAME', 'garantias_seace', 'User')

# Configuración de Email (desde .env actual)
[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_HOST', 'smtp.gmail.com', 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_PORT', '587', 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_USER', 'yanfrancochaupincsco@gmail.com', 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_PASS', 'yixe avpb errk sonp', 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_TO', 'yanfrancochaupincsco@gmail.com', 'User')

# Configuración de IA (desde .env actual)
[System.Environment]::SetEnvironmentVariable('GARANTIAS_GEMINI_API_KEY', 'YOUR_API_KEY_HERE', 'User')

Write-Host "✅ Variables de entorno configuradas" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Variables configuradas:" -ForegroundColor Cyan
Get-ChildItem Env:GARANTIAS_* | Format-Table Name, Value -AutoSize
Write-Host ""
Write-Host "⚠️  RECORDATORIO IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   1. Estas son las credenciales ANTIGUAS del archivo .env" -ForegroundColor Red
Write-Host "   2. DEBES rotarlas lo antes posible por seguridad" -ForegroundColor Red
Write-Host "   3. Ejecuta setup_env.bat para configurar credenciales nuevas" -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 Ahora puedes ejecutar el proyecto:" -ForegroundColor Green
Write-Host "   cd 1_motor_etl" -ForegroundColor White
Write-Host "   python main_auto.py" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANTE: Cierra y vuelve a abrir PowerShell para que las variables tomen efecto" -ForegroundColor Yellow
