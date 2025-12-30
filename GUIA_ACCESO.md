# 🔐 Guía de Acceso - Sistema MQS Garantías

## ✅ Credenciales de Acceso

### 👨‍💼 Usuario Administrador
```
Usuario: admin
Contraseña: 123
PIN (Director): 123456
```

### 👤 Usuario Colaborador
```
Usuario: user
Contraseña: 123
```

---

## 🚀 Cómo Iniciar Sesión

1. Abrir: **http://localhost:3000**
2. Click en **"ACCEDER A MQS"**
3. Ingresar credenciales: `admin` / `123`
4. Seleccionar módulo deseado
5. Si pide PIN: `123456`

---

## ✨ Mejoras Implementadas en el Login

### 1. Ver/Ocultar Contraseña
- Click en el ícono del ojo 👁️ para mostrar/ocultar la contraseña
- Facilita verificar que escribiste correctamente

### 2. Recuperar Contraseña
- Link "¿Olvidaste tu contraseña?" debajo del formulario
- Muestra modal con:
  - Contacto del administrador
  - **Credenciales de prueba visibles** (admin/123)
  - Información de ayuda

### 3. Recordar Sesión
- Checkbox para mantener la sesión activa
- Mejora la experiencia de usuario

---

## 🔧 Scripts para Crear Usuarios

### Opción 1: Script Python (Recomendado)
```bash
cd c:\laragon\www\proyecto_garantias
.\venv\Scripts\Activate.ps1
python crear_usuarios.py
```

### Opción 2: Script SQL
Ejecutar en MySQL Workbench o línea de comandos:
```bash
mysql -u root -p123456789 garantias_seace < create_users.sql
```

---

## ⚠️ Solución de Problemas

### Si no puedes iniciar sesión:

1. **Verificar que MySQL esté corriendo**
   - Laragon debe estar activo
   - Base de datos `garantias_seace` debe existir

2. **Crear usuarios manualmente**
   ```bash
   python crear_usuarios.py
   ```

3. **Verificar conexión del backend**
   - Backend debe estar en: http://localhost:8000
   - Probar: http://localhost:8000/docs

4. **Ver credenciales en el modal**
   - Click en "¿Olvidaste tu contraseña?"
   - Las credenciales de prueba están visibles ahí

---

## 📁 Archivos Creados

- [crear_usuarios.py](file:///c:/laragon/www/proyecto_garantias/crear_usuarios.py) - Script Python para crear usuarios
- [create_users.sql](file:///c:/laragon/www/proyecto_garantias/create_users.sql) - Script SQL alternativo
- [CREDENCIALES.md](file:///c:/laragon/www/proyecto_garantias/CREDENCIALES.md) - Documentación completa

---

## 🎯 Próximos Pasos

1. Ejecutar `python crear_usuarios.py` para asegurar que los usuarios existan
2. Acceder a http://localhost:3000
3. Usar credenciales: `admin` / `123`
4. Si olvidas la contraseña, click en el link de recuperación

---

**¡El sistema está listo para usar!** 🎉
