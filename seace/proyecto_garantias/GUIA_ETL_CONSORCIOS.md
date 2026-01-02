# 🤖 Guía: ETL de Consorcios - Poblar Detalle_Consorcios

## 📊 Estado Actual

- **Total consorcios en BD**: 2,745 adjudicaciones con "CONSORCIO" en el nombre
- **Consorcios procesados**: 0
- **Consorcios pendientes**: 2,106 (con id_contrato válido)
- **Tabla Detalle_Consorcios**: VACÍA

## ✅ Test Exitoso

El test simple (`test_consorcio_simple.py`) confirmó que:
- ✅ Conexión a BD funciona
- ✅ Descarga de metadata SEACE funciona
- ✅ Descarga de PDFs funciona (2.85 MB descargado)
- ✅ Subida a Gemini AI funciona
- ❌ **PROBLEMA**: Cuota de API Gemini excedida (Error 429)

## 🔧 Opciones para Continuar

### Opción 1: Esperar Reset de Cuota Gemini (Recomendado si tienes plan gratuito)

**Cuotas de Gemini 2.0 Flash:**
- Plan gratuito: 15 requests/minuto, 1,500 requests/día
- Verifica tu uso: https://ai.dev/usage?tab=rate-limit

**Comando para ejecutar cuando se resetee:**
```cmd
cd 1_motor_etl
python etl_consorcios_ai.py
```

**Características:**
- Procesa 10 contratos por ciclo
- Pausa de 2 segundos entre contratos
- Pausa de 5 segundos entre ciclos
- Manejo automático de rate limits (espera 30s si detecta 429)

---

### Opción 2: Usar Groq API (Alternativa más rápida)

Groq ofrece API gratuita con límites más generosos:
- **Llama 3.1 70B**: 30 requests/minuto, 14,400 requests/día
- Más rápido que Gemini
- Extrae texto del PDF localmente (pypdf) y lo envía a Groq

**Pasos:**

#### 1. Obtener API Key de Groq
```
1. Ve a: https://console.groq.com/
2. Crea una cuenta (gratis)
3. Genera una API Key
4. Copia la key
```

#### 2. Configurar Variable de Entorno
```cmd
# Ejecutar en CMD (como administrador)
setx GARANTIAS_GROQ_API_KEY "tu_api_key_aqui" /M
```

#### 3. Reiniciar terminal y ejecutar
```cmd
# Cerrar y abrir nueva terminal
cd c:\laragon\www\proyecto_garantias\1_motor_etl
python etl_consorcios_groq.py
```

**Ventajas de Groq:**
- ✅ Más rápido (respuestas en 1-2 segundos)
- ✅ Límites más generosos
- ✅ No requiere subir PDFs completos (extrae texto localmente)
- ✅ Modelo Llama 3.1 70B muy capaz

**Desventajas:**
- ⚠️ Extracción de texto puede fallar en PDFs escaneados (sin OCR)
- ⚠️ Gemini puede ser más preciso con PDFs complejos

---

### Opción 3: Procesamiento Manual Limitado

Si solo quieres poblar algunos registros de prueba:

```cmd
# Editar etl_consorcios_ai.py línea 56
# Cambiar: LIMIT 10
# Por:     LIMIT 3

# Ejecutar
cd 1_motor_etl
python etl_consorcios_ai.py
```

Esto procesará solo 3 contratos por ciclo, reduciendo el uso de API.

---

## 📋 Comparación de APIs

| Característica | Gemini 2.0 Flash | Groq Llama 3.1 70B |
|----------------|------------------|---------------------|
| **Requests/min** | 15 | 30 |
| **Requests/día** | 1,500 | 14,400 |
| **Velocidad** | 5-10s | 1-2s |
| **Precisión PDFs** | Excelente | Buena |
| **PDFs escaneados** | ✅ Sí (OCR) | ❌ No |
| **Costo** | Gratis | Gratis |
| **Setup** | Ya configurado | Requiere API key |

---

## 🎯 Recomendación

### Para 2,106 consorcios:

**Si tienes tiempo (2-3 días):**
- Usa **Gemini** cuando se resetee la cuota
- Mejor precisión con PDFs complejos
- Ya está configurado

**Si quieres terminar hoy:**
- Configura **Groq** (5 minutos)
- Procesará los 2,106 en ~2-3 horas
- Muy buena precisión

**Híbrido (Mejor opción):**
1. Configura Groq y procesa la mayoría
2. Revisa casos fallidos
3. Usa Gemini para casos difíciles

---

## 📊 Estimación de Tiempo

### Con Gemini (cuando se resetee):
- 10 contratos/ciclo × 2s/contrato = 20s/ciclo
- 5s pausa entre ciclos = 25s/ciclo
- 2,106 contratos ÷ 10 = 211 ciclos
- **Tiempo total**: ~88 minutos (1.5 horas)

### Con Groq:
- 10 contratos/ciclo × 1s/contrato = 10s/ciclo
- 3s pausa entre ciclos = 13s/ciclo
- 2,106 contratos ÷ 10 = 211 ciclos
- **Tiempo total**: ~46 minutos

---

## 🔍 Monitoreo del Progreso

Durante la ejecución, puedes monitorear en otra terminal:

```cmd
# Ver cuántos se han procesado
python check_consorcios.py

# Ver últimos registros insertados
python -c "import mysql.connector; from config.secrets_manager import get_db_config; conn = mysql.connector.connect(**get_db_config()); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*), MAX(fecha_registro) FROM Detalle_Consorcios'); print(cursor.fetchone()); conn.close()"
```

---

## ⚠️ Notas Importantes

1. **No interrumpir el proceso**: Los PDFs se descargan y eliminan automáticamente
2. **Espacio en disco**: Cada PDF se descarga temporalmente (~2-5 MB)
3. **Conexión a internet**: Debe ser estable
4. **Rate limits**: Ambos scripts manejan automáticamente los límites

---

## 🆘 Solución de Problemas

### Error 429 (Cuota excedida)
```
✅ Esperar 24 horas para reset
✅ Cambiar a Groq
✅ Reducir LIMIT en la consulta
```

### PDF no descarga
```
⏩ El script salta automáticamente
⏩ No todos los contratos tienen PDF adjunto
```

### Error de parsing JSON
```
⚠️ La IA no pudo extraer datos estructurados
⚠️ El script continúa con el siguiente
```

---

**Creado**: 18 de diciembre de 2024  
**Estado**: Listo para ejecutar (pendiente API key o reset de cuota)
