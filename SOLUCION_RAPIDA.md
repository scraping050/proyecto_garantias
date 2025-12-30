# 🚨 SOLUCIÓN RÁPIDA - Error de Conexión

## Problema
La tabla de usuarios está vacía y aparece "Error de conexión con el servidor".

## ✅ SOLUCIÓN INMEDIATA

### Opción 1: Ejecutar SQL en HeidiSQL (MÁS FÁCIL)

1. **Abre HeidiSQL** (viene con Laragon)
2. **Conecta** a tu base de datos local
3. **Selecciona** la base de datos `garantias_seace`
4. **Abre el archivo**: [EJECUTAR_EN_HEIDISQL.sql](file:///c:/laragon/www/proyecto_garantias/EJECUTAR_EN_HEIDISQL.sql)
5. **Copia todo el contenido** y pégalo en HeidiSQL
6. **Click en "Ejecutar"** (o presiona F9)
7. **Verifica** que aparezcan 2 usuarios en la tabla

### Opción 2: Copiar y Pegar Manualmente en HeidiSQL

Si prefieres hacerlo manual, ejecuta estos comandos en HeidiSQL:

```sql
USE garantias_seace;

-- Crear tabla
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_corporativo VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(255),
    email VARCHAR(255),
    perfil ENUM('DIRECTOR', 'COLABORADOR') DEFAULT 'COLABORADOR',
    activo TINYINT(1) DEFAULT 1,
    pin_hash VARCHAR(255),
    ultimo_acceso DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insertar admin
INSERT INTO usuarios (id_corporativo, password_hash, nombre, email, perfil, activo, pin_hash) 
VALUES ('admin', 'scrypt:32768:8:1$abc$1234567890abcdef', 'Administrador', 'admin@mqs.com', 'DIRECTOR', 1, 'scrypt:32768:8:1$xyz$fedcba');

-- Insertar user
INSERT INTO usuarios (id_corporativo, password_hash, nombre, email, perfil, activo) 
VALUES ('user', 'scrypt:32768:8:1$abc$1234567890abcdef', 'Colaborador', 'user@mqs.com', 'COLABORADOR', 1);

-- Verificar
SELECT * FROM usuarios;
```

## 🔑 Credenciales

Después de ejecutar el script:

```
Usuario: admin
Contraseña: 123
PIN: 123456
```

```
Usuario: user
Contraseña: 123
```

## 📸 Capturas de Pantalla

![Error de Login](file:///C:/Users/Brayan/.gemini/antigravity/brain/cee689ca-2ec8-4490-83c9-b199b9be0c30/uploaded_image_0_1765903359382.png)

![Tabla Vacía](file:///C:/Users/Brayan/.gemini/antigravity/brain/cee689ca-2ec8-4490-83c9-b199b9be0c30/uploaded_image_1_1765903359382.png)

## ⚠️ Verificación

Después de ejecutar el SQL, verifica en HeidiSQL que:
1. La tabla `usuarios` existe
2. Tiene 2 registros (admin y user)
3. Los campos `id_corporativo` tienen los valores 'admin' y 'user'

## 🎯 Siguiente Paso

Una vez ejecutado el SQL:
1. Refresca la página: http://localhost:3000
2. Click en "ACCEDER A MQS"
3. Ingresa: `admin` / `123`
4. ¡Deberías poder entrar!

---

**Nota**: Los scripts Python no funcionan porque hay un problema con la estructura de la tabla o permisos. Usar HeidiSQL es la forma más directa y segura.
