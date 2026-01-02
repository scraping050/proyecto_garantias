# Script de configuración de variables de entorno para Windows
# Ejecutar como Administrador en PowerShell

Write-Host "🔐 Configuración de Variables de Entorno - Proyecto Garantias" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Función para solicitar input con validación
function Get-SecureInput {
    param(
        [string]$Prompt,
        [string]$CurrentValue = "",
        [bool]$IsPassword = $false
    )
    
    if ($CurrentValue) {
        Write-Host "$Prompt (actual: $CurrentValue)" -ForegroundColor Yellow
    } else {
        Write-Host "$Prompt" -ForegroundColor Yellow
    }
    
    if ($IsPassword) {
        $secure = Read-Host -AsSecureString
        $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
        $value = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
        return $value
    } else {
        return Read-Host
    }
}

Write-Host "📋 Este script configurará las variables de entorno necesarias" -ForegroundColor Green
Write-Host "   Las variables se guardarán a nivel de USUARIO" -ForegroundColor Green
Write-Host ""

# Configuración de Base de Datos
Write-Host "1️⃣  CONFIGURACIÓN DE BASE DE DATOS" -ForegroundColor Magenta
Write-Host "=================================" -ForegroundColor Magenta

$DB_HOST = Get-SecureInput "Host de MySQL" "localhost"
$DB_USER = Get-SecureInput "Usuario de MySQL" "root"
$DB_PASS = Get-SecureInput "Contraseña de MySQL (NUEVA - mínimo 16 caracteres)" "" $true
$DB_NAME = Get-SecureInput "Nombre de la base de datos" "garantias_seace"

# Validar contraseña
if ($DB_PASS.Length -lt 16) {
    Write-Host "❌ Error: La contraseña debe tener al menos 16 caracteres" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Configuración de Email
Write-Host "2️⃣  CONFIGURACIÓN DE EMAIL" -ForegroundColor Magenta
Write-Host "=========================" -ForegroundColor Magenta

$EMAIL_HOST = Get-SecureInput "Servidor SMTP" "smtp.gmail.com"
$EMAIL_PORT = Get-SecureInput "Puerto SMTP" "587"
$EMAIL_USER = Get-SecureInput "Email de envío"
$EMAIL_PASS = Get-SecureInput "Contraseña de aplicación Gmail (NUEVA)" "" $true
$EMAIL_TO = Get-SecureInput "Email de destino para reportes"

Write-Host ""

# Configuración de IA
Write-Host "3️⃣  CONFIGURACIÓN DE IA" -ForegroundColor Magenta
Write-Host "======================" -ForegroundColor Magenta
Write-Host "   Genera una nueva API key en: https://makersuite.google.com/app/apikey" -ForegroundColor Gray

$GEMINI_API_KEY = Get-SecureInput "Google Gemini API Key (NUEVA)" "" $true

Write-Host ""
Write-Host "💾 Guardando variables de entorno..." -ForegroundColor Cyan

# Guardar variables de entorno
[System.Environment]::SetEnvironmentVariable('GARANTIAS_DB_HOST', $DB_HOST, 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_DB_USER', $DB_USER, 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_DB_PASS', $DB_PASS, 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_DB_NAME', $DB_NAME, 'User')

[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_HOST', $EMAIL_HOST, 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_PORT', $EMAIL_PORT, 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_USER', $EMAIL_USER, 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_PASS', $EMAIL_PASS, 'User')
[System.Environment]::SetEnvironmentVariable('GARANTIAS_EMAIL_TO', $EMAIL_TO, 'User')

[System.Environment]::SetEnvironmentVariable('GARANTIAS_GEMINI_API_KEY', $GEMINI_API_KEY, 'User')

Write-Host "✅ Variables de entorno configuradas correctamente" -ForegroundColor Green
Write-Host ""

# Actualizar contraseña de MySQL
Write-Host "🔄 Actualizando contraseña de MySQL..." -ForegroundColor Cyan
Write-Host "   Ejecuta este comando en MySQL:" -ForegroundColor Yellow
Write-Host "   ALTER USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';" -ForegroundColor White
Write-Host "   FLUSH PRIVILEGES;" -ForegroundColor White
Write-Host ""

# Crear archivo de recordatorio
$reminderContent = @"
# RECORDATORIO DE SEGURIDAD

## Credenciales Rotadas el $(Get-Date -Format "dd/MM/yyyy HH:mm")

### Próximas acciones:

1. ✅ Variables de entorno configuradas
2. ⏳ Actualizar contraseña de MySQL (ver comando arriba)
3. ⏳ Revocar API key antigua de Gemini
4. ⏳ Revocar contraseña de aplicación Gmail antigua
5. ⏳ Eliminar archivo .env del repositorio
6. ⏳ Verificar que todo funciona correctamente

### Para verificar configuración:
```powershell
python config/secrets_manager.py
```

### Para ver variables configuradas:
```powershell
Get-ChildItem Env:GARANTIAS_*
```

### IMPORTANTE:
- NO compartas estas credenciales
- NO las subas a Git
- Rota las credenciales cada 90 días
- Usa contraseñas únicas y fuertes
"@

$reminderContent | Out-File -FilePath "SECURITY_REMINDER.md" -Encoding UTF8

Write-Host "📝 Archivo SECURITY_REMINDER.md creado con instrucciones" -ForegroundColor Green
Write-Host ""

Write-Host "🎉 CONFIGURACIÓN COMPLETADA" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   1. Actualiza la contraseña de MySQL (ver comando arriba)" -ForegroundColor White
Write-Host "   2. Revoca las credenciales antiguas" -ForegroundColor White
Write-Host "   3. Ejecuta: python config/secrets_manager.py" -ForegroundColor White
Write-Host "   4. Elimina el archivo .env" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANTE: Reinicia PowerShell para que las variables tomen efecto" -ForegroundColor Yellow
Write-Host ""

# Preguntar si quiere ver las variables configuradas
$showVars = Read-Host "¿Deseas ver las variables configuradas? (s/n)"
if ($showVars -eq "s") {
    Write-Host ""
    Write-Host "📊 Variables de entorno configuradas:" -ForegroundColor Cyan
    Get-ChildItem Env:GARANTIAS_* | Format-Table Name, Value -AutoSize
}
