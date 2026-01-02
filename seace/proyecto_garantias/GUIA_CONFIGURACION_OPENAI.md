# Guía de Configuración: API Key de OpenAI

## Paso 1: Configurar la API Key

Ejecuta el siguiente comando en PowerShell (como Administrador):

```powershell
[System.Environment]::SetEnvironmentVariable('GARANTIAS_OPENAI_API_KEY', 'tu-api-key-aqui', 'User')
```

**Reemplaza `'tu-api-key-aqui'` con tu API Key real de OpenAI.**

## Paso 2: Reiniciar la Terminal

Cierra y vuelve a abrir PowerShell para que cargue la nueva variable de entorno.

## Paso 3: Verificar la Configuración

```bash
cd c:\laragon\www\proyecto_garantias
python config\secrets_manager.py
```

Deberías ver:
```
✓ OpenAI API Key: ********************...abcd
```

## Paso 4: Ejecutar el ETL de Prueba

```bash
cd 1_motor_etl
python etl_consorcios_openai.py
```

El script procesará solo **5 contratos** en modo prueba y mostrará:
- Tokens consumidos
- Costo en USD
- Datos extraídos

## Configuración Manual (Alternativa)

Si prefieres, edita el archivo `.env` en la raíz del proyecto:

```env
GARANTIAS_OPENAI_API_KEY=sk-proj-...tu-api-key...
```

Luego ejecuta:
```bash
setup_env.bat
```

---

## Notas Importantes

- El script está en **MODO PRUEBA** (solo 5 PDFs)
- Usa el modelo **GPT-4o** (el más preciso)
- Calcula el costo automáticamente
- Para producción: Cambiar `TEST_MODE = False` en el código

## Estimación de Costos

- **Modo prueba (5 PDFs):** ~$0.02 USD
- **100 PDFs:** ~$0.40 USD  
- **1,000 PDFs:** ~$4.00 USD
