# Instrucciones para Ejecutar el Proyecto

## ⚠️ IMPORTANTE: Variables de Entorno Configuradas

Las variables de entorno han sido configuradas exitosamente, pero **necesitas cerrar y volver a abrir PowerShell/CMD** para que tomen efecto.

## 🚀 Pasos para Ejecutar

### 1. Cierra la terminal actual

Cierra completamente PowerShell o CMD.

### 2. Abre una nueva terminal

Abre una nueva ventana de PowerShell o CMD.

### 3. Navega al proyecto

```cmd
cd c:\laragon\www\proyecto_garantias
```

### 4. Verifica la configuración

```cmd
python config\secrets_manager.py
```

**Resultado esperado**:
```
Validando configuracion...
OK - Todas las configuraciones estan correctas

Base de Datos:
  Host: localhost
  User: root
  Database: garantias_seace
  Password: *********

Email:
  Host: smtp.gmail.com:587
  User: yanfrancochaupincsco@gmail.com
  Password: *******************

IA:
  Gemini API Key: ********************KxQ
```

### 5. Ejecuta el proyecto

```cmd
cd 1_motor_etl
python main_auto.py
```

## ✅ Variables Configuradas

Las siguientes variables de entorno están configuradas:

- `GARANTIAS_DB_HOST` = localhost
- `GARANTIAS_DB_USER` = root
- `GARANTIAS_DB_PASS` = 123456789
- `GARANTIAS_DB_NAME` = garantias_seace
- `GARANTIAS_EMAIL_HOST` = smtp.gmail.com
- `GARANTIAS_EMAIL_PORT` = 587
- `GARANTIAS_EMAIL_USER` = yanfrancochaupincsco@gmail.com
- `GARANTIAS_EMAIL_PASS` = yixe avpb errk sonp
- `GARANTIAS_EMAIL_TO` = yanfrancochaupincsco@gmail.com
- `GARANTIAS_GEMINI_API_KEY` = AIzaSyBW_tjkzoXXlX61iy-HKMPgEd37MwpQKxQ

## ⚠️ RECORDATORIO DE SEGURIDAD

**ESTAS SON LAS CREDENCIALES ANTIGUAS DEL ARCHIVO .env**

Por seguridad, debes rotarlas lo antes posible:

1. **MySQL**: Cambiar contraseña "123456789" por una segura
2. **Gemini API**: Revocar y generar nueva key
3. **Gmail**: Revocar y generar nueva contraseña de aplicación

Ejecuta `setup_env.bat` cuando estés listo para configurar credenciales nuevas.

---

**Fecha**: 17 de diciembre de 2024
