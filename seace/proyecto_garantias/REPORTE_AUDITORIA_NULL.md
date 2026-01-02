# Reporte de Auditoría: Datos NULL en Base de Datos

## 📊 RESUMEN EJECUTIVO

Se realizó una auditoría completa de la base de datos para identificar campos NULL o vacíos que deberían contener información.

**Fecha**: 18 de diciembre de 2024  
**Estado**: Auditoría completada - Problemas identificados

---

## 🔍 HALLAZGOS PRINCIPALES

### 1. ❌ CRÍTICO: id_contrato NULL (23.97%)

**Total afectado**: 1,825 de 7,614 adjudicaciones (23.97%)

**Distribución por estado**:
| Estado | Sin id_contrato | Análisis |
|--------|-----------------|----------|
| CONSENTIDO | 552 | ✅ CORRECTO - No tienen contrato aún |
| **CONTRATADO** | **429** | ❌ **BUG - Deberían tener contrato** |
| NULO | 229 | ✅ CORRECTO - Proceso anulado |
| RETROTRAIDO | 206 | ✅ CORRECTO - Proceso retrotraído |
| ADJUDICADO | 176 | ✅ CORRECTO - No tienen contrato aún |
| DESIERTO | 117 | ✅ CORRECTO - Proceso desierto |
| Otros | 116 | ✅ CORRECTO - Estados sin contrato |

**Problema identificado**:
- ❌ **429 adjudicaciones CONTRATADAS sin id_contrato**
- Investigación en JSON reveló que **SÍ existen contratos en la fuente**
- Ejemplo: Convocatoria 1001603 tiene 6 contratos en JSON pero NO se cargan

**Causa raíz**:
- El mapeo de contratos en `cargador.py` (líneas 143-148) funciona correctamente
- **PERO**: Algunos awards tienen múltiples contratos asociados
- El código actual solo mapea 1 contrato por award
- Cuando hay múltiples contratos para el mismo award, solo se guarda el último

---

### 2. ⚠️ MODERADO: ganador_ruc NULL (3.90%)

**Total afectado**: 297 de 7,614 adjudicaciones (3.90%)

**Análisis**:
- Investigación en JSON mostró que algunos suppliers tienen ID en formato `PE-RUC-XXXXXXXXXX`
- El código extrae correctamente: `sups[0].get('id')`
- **Posible causa**: Algunos suppliers no tienen campo `id` en el JSON

**Impacto**: Moderado - Dificulta identificación del ganador

---

### 3. ⚠️ MODERADO: monto_estimado NULL (15.14%)

**Total afectado**: 1,454 de 9,606 licitaciones (15.14%)

**Análisis**:
- Algunos procesos no tienen monto estimado en el JSON original
- Esto es **normal** en SEACE - no todos los procesos publican monto estimado

**Impacto**: Bajo - Es una limitación de la fuente de datos

---

### 4. ❌ CRÍTICO: Tabla Detalle_Consorcios VACÍA

**Total registros**: 0

**Análisis**:
- La tabla existe pero está completamente vacía
- **Causa**: El proceso ETL de consorcios NO se ha ejecutado
- Existe script `etl_consorcios_groq.py` pero no se ha corrido

**Impacto**: Alto - No hay información de consorcios

---

## 📋 DATOS CORRECTOS (Sin problemas)

✅ **fecha_publicacion**: 0 NULL (100% completo)  
✅ **fecha_adjudicacion**: 1 NULL (99.99% completo)  
✅ **departamento**: 0 NULL (100% completo)  
✅ **provincia**: 0 NULL (100% completo)  
✅ **distrito**: 0 NULL (100% completo)  
✅ **monto_adjudicado**: 0 NULL/0 (100% completo)  

---

## 🔧 PLAN DE CORRECCIÓN

### Prioridad 1: Corregir mapeo de id_contrato

**Problema**: Awards con múltiples contratos solo guardan el último

**Solución propuesta**:

```python
# En cargador.py, línea 143-148
# ACTUAL (INCORRECTO):
mapa_contratos = {}
for c in compiled.get('contracts', []):
    aw_id = c.get('awardID')
    c_id = c.get('id')
    if aw_id and c_id:
        mapa_contratos[str(aw_id)] = safe_str(c_id, 100)  # Solo guarda el último

# PROPUESTO (CORRECTO):
mapa_contratos = {}
for c in compiled.get('contracts', []):
    aw_id = c.get('awardID')
    c_id = c.get('id')
    if aw_id and c_id:
        # Guardar múltiples contratos separados por coma
        if str(aw_id) in mapa_contratos:
            mapa_contratos[str(aw_id)] += ',' + safe_str(c_id, 100)
        else:
            mapa_contratos[str(aw_id)] = safe_str(c_id, 100)
```

**Alternativa**: Crear tabla `Contratos` separada con relación 1:N con adjudicaciones

---

### Prioridad 2: Ejecutar ETL de Consorcios

**Acción**: Ejecutar `etl_consorcios_groq.py` para poblar `Detalle_Consorcios`

**Comando**:
```bash
python 1_motor_etl\etl_consorcios_groq.py
```

---

### Prioridad 3: Investigar ganador_ruc NULL

**Acción**: Analizar casos específicos donde `suppliers[0].id` es NULL en JSON

**Script de análisis**:
```python
# Buscar awards sin supplier ID
for aw in awards:
    sups = aw.get('suppliers', [])
    if sups and not sups[0].get('id'):
        print(f"Award sin supplier ID: {aw.get('id')}")
```

---

## 📊 ESTADÍSTICAS DETALLADAS

### Tabla: Licitaciones_Cabecera

| Campo | NULL/Vacío | % | Estado |
|-------|------------|---|--------|
| monto_estimado | 1,454 | 15.14% | ⚠️ Normal (limitación de fuente) |
| Otros campos | 0 | 0% | ✅ Completo |

### Tabla: Licitaciones_Adjudicaciones

| Campo | NULL/Vacío | % | Estado |
|-------|------------|---|--------|
| id_contrato | 1,825 | 23.97% | ❌ **429 son BUG** |
| ganador_ruc | 297 | 3.90% | ⚠️ Investigar |
| entidad_financiera | 4,764 | 62.57% | ✅ Correcto (RETENCIÓN) |
| fecha_adjudicacion | 1 | 0.01% | ✅ Casi completo |

### Tabla: Detalle_Consorcios

| Estado | Registros |
|--------|-----------|
| Total | 0 |
| **Acción** | **Ejecutar ETL de consorcios** |

---

## ✅ PRÓXIMOS PASOS

1. **Corregir código** de mapeo de contratos en `cargador.py`
2. **Re-ejecutar ETL** para actualizar id_contrato
3. **Ejecutar ETL de consorcios** para poblar Detalle_Consorcios
4. **Validar** que los 429 casos CONTRATADOS ahora tengan id_contrato
5. **Investigar** casos de ganador_ruc NULL

---

## 📚 ARCHIVOS DE AUDITORÍA

- `auditoria_datos_null.py` - Script de auditoría completa
- `investigar_json_null.py` - Investigación en JSON original
- `analizar_mapeo_contratos.py` - Análisis del mapeo de contratos

---

*Reporte generado el 18 de diciembre de 2024*
