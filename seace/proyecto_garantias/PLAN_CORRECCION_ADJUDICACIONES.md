# PLAN DE CORRECCIÓN: Problemas en Licitaciones_Adjudicaciones

## PROBLEMAS DETECTADOS

### Problema 1: estado_item HARDCODEADO ❌
- **Ubicación**: `cargador.py` línea 223
- **Impacto**: 7,959 registros con estado incorrecto
- **Estado actual**: Todos tienen "ADJUDICADO"
- **Estado real**: Varía según el award en el JSON

### Problema 2: SIN_GARANTIA mal clasificado ❌
- **Ubicación**: Columna generada `tipo_garantia`
- **Impacto**: 2,684 registros mal clasificados
- **Clasificación actual**: GARANTIA_BANCARIA
- **Clasificación correcta**: RETENCION

---

## SOLUCIONES

### Solución 1: Capturar estado_item real del JSON

**Archivo**: `1_motor_etl/cargador.py`  
**Línea**: 220-224

**ANTES**:
```python
adjudicaciones.append((
    id_adj, id_contrato, ocid, id_conv, ganador, ruc, m_adj, f_adj, 'ADJUDICADO'  # ← HARDCODEADO
))
```

**DESPUÉS**:
```python
# Capturar estado real del award
estado_award = safe_str(aw.get('status'), 50)
if not estado_award:
    estado_award = 'DESCONOCIDO'

adjudicaciones.append((
    id_adj, id_contrato, ocid, id_conv, ganador, ruc, m_adj, f_adj, estado_award  # ← DINÁMICO
))
```

---

### Solución 2: Corregir lógica de tipo_garantia

**Opción A: Modificar columna generada (Recomendado)**

```sql
-- 1. Eliminar columna generada actual
ALTER TABLE Licitaciones_Adjudicaciones DROP COLUMN tipo_garantia;

-- 2. Crear nueva columna con lógica corregida
ALTER TABLE Licitaciones_Adjudicaciones ADD COLUMN tipo_garantia VARCHAR(50) 
GENERATED ALWAYS AS (
    CASE 
        WHEN entidad_financiera IS NULL OR entidad_financiera = '' 
            OR entidad_financiera = 'SIN_GARANTIA'
            OR entidad_financiera = 'NO_INFO'
            OR entidad_financiera = 'ERROR_CONEXION'
            OR entidad_financiera = 'CONTRATO_NO_ENCONTRADO_API'
        THEN 'RETENCION'
        ELSE 'GARANTIA_BANCARIA'
    END
) STORED;

-- 3. Recrear índice
CREATE INDEX idx_tipo_garantia ON Licitaciones_Adjudicaciones(tipo_garantia);
```

**Opción B: Actualizar spider para no guardar SIN_GARANTIA**

Modificar `spider_garantias.py` línea 134:
```python
# ANTES:
if emisores: res_banco = " | ".join(sorted(emisores))
else: res_banco = "SIN_GARANTIA"

# DESPUÉS:
if emisores: res_banco = " | ".join(sorted(emisores))
else: res_banco = None  # NULL = RETENCION
```

---

## IMPLEMENTACIÓN PASO A PASO

### Paso 1: Corregir cargador.py

```python
# Editar líneas 220-224
estado_award = safe_str(aw.get('status'), 50)
if not estado_award:
    estado_award = 'DESCONOCIDO'

adjudicaciones.append((
    id_adj, id_contrato, ocid, id_conv, ganador, ruc, m_adj, f_adj, estado_award
))
```

### Paso 2: Corregir columna tipo_garantia

Ejecutar SQL:
```sql
ALTER TABLE Licitaciones_Adjudicaciones DROP COLUMN tipo_garantia;

ALTER TABLE Licitaciones_Adjudicaciones ADD COLUMN tipo_garantia VARCHAR(50) 
GENERATED ALWAYS AS (
    CASE 
        WHEN entidad_financiera IS NULL 
            OR entidad_financiera = '' 
            OR entidad_financiera = 'SIN_GARANTIA'
            OR entidad_financiera = 'NO_INFO'
            OR entidad_financiera LIKE 'ERROR%'
            OR entidad_financiera LIKE 'CONTRATO_NO%'
        THEN 'RETENCION'
        ELSE 'GARANTIA_BANCARIA'
    END
) STORED;

CREATE INDEX idx_tipo_garantia ON Licitaciones_Adjudicaciones(tipo_garantia);
```

### Paso 3: Re-ejecutar cargador.py

```cmd
# Limpiar control de cargas para forzar re-procesamiento
python limpiar_control_cargas.py

# Re-ejecutar cargador
cd 1_motor_etl
python cargador.py
```

### Paso 4: Verificar resultados

```cmd
python investigar_problemas_adjudicaciones.py
```

Debe mostrar:
- ✅ Múltiples estados en estado_item (no solo ADJUDICADO)
- ✅ SIN_GARANTIA clasificado como RETENCION

---

## IMPACTO ESPERADO

### Antes de la corrección:

| Métrica | Valor | Estado |
|---------|-------|--------|
| estado_item = "ADJUDICADO" | 7,959 (100%) | ❌ Incorrecto |
| SIN_GARANTIA → GARANTIA_BANCARIA | 2,684 | ❌ Incorrecto |
| RETENCION | 5,109 | ⚠️ Incluye incorrectos |
| GARANTIA_BANCARIA | 2,850 | ⚠️ Incluye incorrectos |

### Después de la corrección:

| Métrica | Valor Esperado | Estado |
|---------|----------------|--------|
| Estados variados en estado_item | Múltiples | ✅ Correcto |
| SIN_GARANTIA → RETENCION | 2,684 | ✅ Correcto |
| RETENCION | ~7,793 | ✅ Correcto |
| GARANTIA_BANCARIA | ~166 | ✅ Correcto |

**Nota**: Los valores finales dependerán de los datos reales después de re-procesar.

---

## ARCHIVOS A MODIFICAR

1. ✅ `1_motor_etl/cargador.py` - Líneas 220-224
2. ✅ Base de datos - Columna `tipo_garantia`
3. ⚠️ `1_motor_etl/spider_garantias.py` - Opcional (línea 134)

---

## TIEMPO ESTIMADO

- Modificar código: 5 minutos
- Modificar BD: 1 minuto
- Re-ejecutar cargador: 2-3 minutos
- Verificar: 1 minuto
- **Total**: ~10 minutos

---

**Creado**: 18 de diciembre de 2024  
**Prioridad**: CRÍTICA  
**Estado**: Listo para implementar
