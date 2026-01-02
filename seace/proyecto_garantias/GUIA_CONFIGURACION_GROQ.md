# Guía: Configuración de Groq API para ETL de Consorcios

## ⚠️ Requisito

El ETL de consorcios (`etl_consorcios_groq.py`) requiere una API key de Groq para funcionar.

---

## 🔑 Obtener API Key de Groq

### Paso 1: Crear Cuenta

1. Visitar: https://console.groq.com
2. Crear cuenta gratuita (con Google/GitHub)
3. Verificar email

### Paso 2: Generar API Key

1. Ir a: https://console.groq.com/keys
2. Click en "Create API Key"
3. Copiar la key (empieza con `gsk_...`)

**⚠️ IMPORTANTE**: Guardar la key en lugar seguro, solo se muestra una vez

---

## ⚙️ Configurar en el Proyecto

### Opción 1: Variable de Entorno (Recomendado)

**Windows (PowerShell)**:
```powershell
[System.Environment]::SetEnvironmentVariable('GARANTIAS_GROQ_API_KEY', 'gsk_tu_api_key_aqui', 'User')
```

**Windows (CMD)**:
```cmd
setx GARANTIAS_GROQ_API_KEY "gsk_tu_api_key_aqui"
```

**Reiniciar terminal** después de configurar

### Opción 2: Archivo .env

Editar archivo `.env` en la raíz del proyecto:

```
GARANTIAS_GROQ_API_KEY=gsk_tu_api_key_aqui
```

---

## ✅ Verificar Configuración

```bash
# Windows PowerShell
$env:GARANTIAS_GROQ_API_KEY

# Windows CMD
echo %GARANTIAS_GROQ_API_KEY%
```

Debería mostrar tu API key

---

## 🚀 Ejecutar ETL de Consorcios

Una vez configurada la API key:

```bash
python 1_motor_etl\etl_consorcios_groq.py
```

O usar el script batch:

```bash
ejecutar_ia_consorcios.bat
```

---

## 📊 ¿Qué Hace el ETL?

1. **Busca** contratos con "CONSORCIO" en el nombre del ganador
2. **Descarga** el PDF del contrato desde SEACE
3. **Extrae** texto del PDF (primeras 15 páginas)
4. **Analiza** con IA (Groq Llama 3.1 70B) para identificar miembros
5. **Guarda** en tabla `Detalle_Consorcios`:
   - RUC del miembro
   - Nombre del miembro
   - Porcentaje de participación

---

## 💰 Costos

**Groq es GRATUITO** para uso normal:
- 30 requests/minuto
- 14,400 tokens/minuto
- Suficiente para procesar cientos de contratos

---

## ⚠️ Limitaciones

- Requiere conexión a internet
- Depende de disponibilidad de PDFs en SEACE
- IA puede no extraer el 100% correctamente (pero es muy precisa)

---

## 🔧 Troubleshooting

### Error: "Variable de entorno no encontrada"
- Verificar que la variable esté configurada
- Reiniciar terminal/IDE
- Verificar nombre exacto: `GARANTIAS_GROQ_API_KEY`

### Error: "Rate limit (429)"
- Esperar 1 minuto
- El script automáticamente reintenta

### Error: "No se pudo descargar PDF"
- Normal - no todos los contratos tienen PDF público
- El script continúa con el siguiente

---

*Guía creada el 18 de diciembre de 2024*
