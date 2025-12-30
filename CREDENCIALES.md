# 🔐 Credenciales de Acceso al Sistema MQS Garantías

## Usuarios Configurados

Según los scripts de configuración en el proyecto, estos son los usuarios disponibles:

### 👨‍💼 Usuario Administrador (DIRECTOR)

```
Usuario: admin
Contraseña: 123
PIN: 123456
```

**Permisos**: Acceso completo a todos los módulos (MQS Operations, Admin Financial, SEACE Analytics)

---

### 👤 Usuario Colaborador

```
Usuario: user
Contraseña: 123
```

**Permisos**: Acceso limitado según perfil de colaborador

---

## 📍 URLs de Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

---

## 🚀 Cómo Iniciar Sesión

1. Abrir navegador en `http://localhost:3000`
2. Click en **"ACCEDER A MQS"**
3. Ingresar credenciales:
   - **Usuario**: `admin`
   - **Contraseña**: `123`
4. Seleccionar módulo deseado:
   - **MQS Operations** - Gestión de operaciones
   - **Admin Financial** - Administración financiera
   - **SEACE Analytics** - Análisis de licitaciones
5. Si seleccionas un perfil de Director/Admin, se solicitará el PIN: `123456`

---

## 🔧 Crear/Resetear Usuarios

Si necesitas recrear los usuarios en la base de datos, ejecuta:

```bash
cd c:\laragon\www\proyecto_garantias
.\venv\Scripts\Activate.ps1
python setup_users.py
```

Este script:
- ✅ Elimina usuarios existentes
- ✅ Crea usuario `admin` con contraseña `123` y PIN `123456`
- ✅ Crea usuario `user` con contraseña `123`
- ✅ Verifica la creación exitosa

---

## 📊 Estructura de la Base de Datos

**Base de datos**: `garantias_seace`

**Tabla de usuarios**: `users`

Campos principales:
- `id_corporativo` - Username para login
- `password_hash` - Contraseña hasheada
- `nombre` - Nombre completo
- `email` - Correo electrónico
- `perfil` - DIRECTOR / COLABORADOR
- `activo` - Estado del usuario
- `pin_hash` - PIN para acceso administrativo (solo DIRECTOR)

---

## ⚠️ Notas Importantes

1. **Base de datos**: Asegúrate de que MySQL esté corriendo y la base de datos `garantias_seace` exista
2. **Servidores**: Ambos servidores (backend y frontend) deben estar corriendo
3. **Contraseñas**: Las contraseñas están hasheadas con `werkzeug.security`
4. **Primer uso**: Si es la primera vez, ejecuta `python setup_users.py` para crear los usuarios

---

## 🔍 Verificar Usuarios en la Base de Datos

Para ver los usuarios directamente en MySQL:

```sql
USE garantias_seace;
SELECT id_corporativo, nombre, email, perfil, activo FROM users;
```

---

## 📝 Archivos de Configuración

- [setup_users.py](file:///c:/laragon/www/proyecto_garantias/setup_users.py) - Script principal de creación de usuarios
- [create_test_users.py](file:///c:/laragon/www/proyecto_garantias/create_test_users.py) - Script alternativo
- [app/routers/auth.py](file:///c:/laragon/www/proyecto_garantias/app/routers/auth.py) - Lógica de autenticación
- [.env](file:///c:/laragon/www/proyecto_garantias/.env) - Configuración de base de datos
