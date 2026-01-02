# Guía de Seguridad - Proyecto Garantias

## 🔐 Gestión de Credenciales

### Configuración Inicial

1. **Ejecutar script de configuración**:
   ```powershell
   .\setup_env.ps1
   ```

2. **Generar nuevas credenciales**:
   - **MySQL**: Contraseña de mínimo 16 caracteres
   - **Gemini API**: Nueva key desde https://makersuite.google.com/app/apikey
   - **Gmail**: Nueva contraseña de aplicación desde https://myaccount.google.com/apppasswords

3. **Verificar configuración**:
   ```powershell
   python config/secrets_manager.py
   ```

### Variables de Entorno Requeridas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `GARANTIAS_DB_HOST` | Host de MySQL | `localhost` |
| `GARANTIAS_DB_USER` | Usuario de MySQL | `root` |
| `GARANTIAS_DB_PASS` | Contraseña de MySQL | `contraseña_segura_16+` |
| `GARANTIAS_DB_NAME` | Nombre de BD | `garantias_seace` |
| `GARANTIAS_EMAIL_HOST` | Servidor SMTP | `smtp.gmail.com` |
| `GARANTIAS_EMAIL_PORT` | Puerto SMTP | `587` |
| `GARANTIAS_EMAIL_USER` | Email de envío | `tu@email.com` |
| `GARANTIAS_EMAIL_PASS` | Contraseña de app Gmail | `xxxx xxxx xxxx xxxx` |
| `GARANTIAS_EMAIL_TO` | Email de destino | `destino@email.com` |
| `GARANTIAS_GEMINI_API_KEY` | API key de Gemini | `AIza...` |

### Rotación de Credenciales

**Frecuencia recomendada**: Cada 90 días

**Proceso**:
1. Generar nuevas credenciales
2. Ejecutar `setup_env.ps1` con nuevos valores
3. Actualizar contraseña de MySQL:
   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_contraseña';
   FLUSH PRIVILEGES;
   ```
4. Revocar credenciales antiguas
5. Verificar que todo funciona

## 🛡️ Mejores Prácticas

### ✅ Hacer

- Usar contraseñas únicas de 16+ caracteres
- Rotar credenciales cada 90 días
- Mantener `.env` fuera del repositorio
- Usar variables de entorno del sistema
- Verificar configuración antes de desplegar

### ❌ No Hacer

- NO subir credenciales a Git
- NO compartir credenciales por email/chat
- NO usar contraseñas débiles
- NO hardcodear credenciales en código
- NO reutilizar contraseñas

## 🔍 Auditoría de Seguridad

### Verificar Credenciales Expuestas

```powershell
# Buscar posibles credenciales en código
git grep -i "password\|api_key\|secret" -- "*.py"

# Verificar que .env no esté en Git
git ls-files | Select-String ".env"
```

### Escaneo de Seguridad

```powershell
# Instalar git-secrets
# https://github.com/awslabs/git-secrets

# Escanear repositorio
git secrets --scan
```

## 📞 Contacto de Seguridad

Si detectas una vulnerabilidad de seguridad:
- Email: yanfrancochaupincsco@gmail.com
- Asunto: [SEGURIDAD] Vulnerabilidad en proyecto_garantias

---

**Última actualización**: 17 de diciembre de 2024
