# Guía de Inicio Rápido - Implementación de Seguridad

## 🚀 Paso a Paso

### Paso 1: Configurar Variables de Entorno

**Opción A: Usando CMD (Recomendado para Windows)**
```cmd
setup_env.bat
```

**Opción B: Usando PowerShell**
```powershell
# Cambiar política de ejecución temporalmente
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\setup_env.ps1
```

### Paso 2: Generar Nuevas Credenciales

Antes de ejecutar el script, genera:

1. **Nueva contraseña MySQL** (mínimo 16 caracteres):
   - Usa un generador de contraseñas
   - Ejemplo: `MyS3cur3P@ssw0rd2024!`

2. **Nueva API Key de Gemini**:
   - Ve a: https://makersuite.google.com/app/apikey
   - Revoca la key antigua: `AIzaSyBW_tjkzoXXlX61iy-HKMPgEd37MwpQKxQ`
   - Genera una nueva

3. **Nueva contraseña de aplicación Gmail**:
   - Ve a: https://myaccount.google.com/apppasswords
   - Revoca la antigua: `yixe avpb errk sonp`
   - Genera una nueva

### Paso 3: Ejecutar Script de Configuración

```cmd
cd c:\laragon\www\proyecto_garantias
setup_env.bat
```

Ingresa los valores cuando se soliciten.

### Paso 4: Actualizar Contraseña de MySQL

```sql
-- Conectar a MySQL
mysql -u root -p

-- Cambiar contraseña (usa la que configuraste)
ALTER USER 'root'@'localhost' IDENTIFIED BY 'tu_nueva_contraseña';
FLUSH PRIVILEGES;
EXIT;
```

### Paso 5: Verificar Configuración

```cmd
python config\secrets_manager.py
```

**Resultado esperado**:
```
✅ Todas las configuraciones están correctas
📊 Base de Datos:
  Host: localhost
  User: root
  ...
```

### Paso 6: Actualizar Módulos Python

Ahora actualizaré los 5 módulos para usar el nuevo sistema de configuración.

---

## ⚠️ Importante

- **NO cierres la ventana** hasta completar todos los pasos
- **Guarda las credenciales** en un gestor de contraseñas seguro
- **Revoca las credenciales antiguas** después de verificar que todo funciona

---

**¿Listo para continuar?** Responde cuando hayas completado los pasos 1-5.
