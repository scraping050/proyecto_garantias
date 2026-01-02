# Propuesta: Clasificación de Estados por Defecto (Sin Traducciones)

## RESUMEN EJECUTIVO

**Solicitud del Usuario**: Guardar estados EXACTAMENTE como vienen en el JSON del SEACE, sin traducciones.

**Problema Actual**: La función `determinar_estado()` traduce estados de inglés a español, causando inconsistencias.

**Solución Propuesta**: Eliminar traducciones y guardar valores originales en mayúsculas.

---

## ANÁLISIS COMPARATIVO

### Función ACTUAL (Con Traducciones)

```python
def determinar_estado(tender_status, item_status):
    st_item = safe_str(item_status)
    if st_item: return st_item.upper()
    
    st = safe_str(tender_status).lower()
    if not st: return "DESCONOCIDO"

    mapping = {
        'active': 'CONVOCADO', 
        'complete': 'CONTRATADO', 
        'cancelled': 'CANCELADO', 
        'unsuccessful': 'DESIERTO', 
        'withdrawn': 'NULO', 
        'planned': 'PROGRAMADO', 
        'awarded': 'ADJUDICADO'
    }
    return mapping.get(st, st.upper())
```

### Resultados ACTUALES

| JSON (tender.status) | BD (estado_proceso) | Comentario |
|----------------------|---------------------|------------|
| active | CONVOCADO | ✗ Traducido |
| complete | CONTRATADO | ✗ Traducido |
| awarded | ADJUDICADO | ✗ Traducido |
| ADJUDICADO | ADJUDICADO | ✓ Original |
| CONSENTIDO | CONSENTIDO | ✓ Original |
| RETROTRAID_POR_RESOLUCION | RETROTRAID_POR_RESOLUCION | ✓ Original |

**Problema**: Mezcla de estados traducidos (inglés→español) y originales (español).

---

## SOLUCIÓN PROPUESTA

### Función NUEVA (Sin Traducciones)

```python
def determinar_estado(tender_status, item_status):
    """
    Retorna el estado ORIGINAL del JSON sin traducciones.
    Normaliza a MAYUSCULAS para consistencia.
    """
    # Priorizar estado del item si existe
    st_item = safe_str(item_status)
    if st_item: 
        return st_item.upper()
    
    # Si no hay estado de item, usar estado del tender
    st = safe_str(tender_status)
    if not st: 
        return "DESCONOCIDO"
    
    # Retornar valor ORIGINAL en mayúsculas
    return st.upper()
```

### Resultados PROPUESTOS

| JSON (tender.status) | BD (estado_proceso) | Comentario |
|----------------------|---------------------|------------|
| active | ACTIVE | ✓ Original |
| complete | COMPLETE | ✓ Original |
| awarded | AWARDED | ✓ Original |
| ADJUDICADO | ADJUDICADO | ✓ Original |
| CONSENTIDO | CONSENTIDO | ✓ Original |
| RETROTRAID_POR_RESOLUCION | RETROTRAID_POR_RESOLUCION | ✓ Original |

**Ventaja**: TODOS los estados son originales, sin traducciones.

---

## VENTAJAS DE LA SOLUCIÓN

### 1. CONSISTENCIA TOTAL
- Todos los estados exactamente como vienen del SEACE
- No hay mezcla de formatos
- Fácil validación contra JSON original

### 2. TRAZABILIDAD
- Comparación directa: BD ↔ JSON
- Auditoría simplificada
- Debug más fácil

### 3. MANTENIBILIDAD
- Código más simple (sin diccionario)
- No requiere actualizar traducciones
- Menos puntos de fallo

### 4. ACTUALIZACIONES AUTOMÁTICAS
- Si SEACE agrega nuevos estados, se reflejan automáticamente
- No requiere modificar código

### 5. COMPATIBILIDAD
- Funciona con estados en inglés Y español
- No asume formato específico

---

## DESVENTAJAS Y SOLUCIONES

### Desventaja 1: Estados en Inglés

**Problema**: Algunos estados estarán en inglés (ACTIVE, COMPLETE, etc.)

**Solución 1 - Vista SQL**:
```sql
CREATE VIEW Licitaciones_Cabecera_Traducido AS
SELECT 
    *,
    CASE estado_proceso
        WHEN 'ACTIVE' THEN 'CONVOCADO'
        WHEN 'COMPLETE' THEN 'CONTRATADO'
        WHEN 'AWARDED' THEN 'ADJUDICADO'
        WHEN 'CANCELLED' THEN 'CANCELADO'
        WHEN 'UNSUCCESSFUL' THEN 'DESIERTO'
        WHEN 'WITHDRAWN' THEN 'NULO'
        WHEN 'PLANNED' THEN 'PROGRAMADO'
        ELSE estado_proceso
    END AS estado_proceso_es
FROM Licitaciones_Cabecera;
```

**Solución 2 - Función SQL**:
```sql
DELIMITER //
CREATE FUNCTION traducir_estado(estado VARCHAR(50)) 
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    RETURN CASE estado
        WHEN 'ACTIVE' THEN 'CONVOCADO'
        WHEN 'COMPLETE' THEN 'CONTRATADO'
        WHEN 'AWARDED' THEN 'ADJUDICADO'
        WHEN 'CANCELLED' THEN 'CANCELADO'
        WHEN 'UNSUCCESSFUL' THEN 'DESIERTO'
        WHEN 'WITHDRAWN' THEN 'NULO'
        WHEN 'PLANNED' THEN 'PROGRAMADO'
        ELSE estado
    END;
END //
DELIMITER ;

-- Uso:
SELECT id_convocatoria, traducir_estado(estado_proceso) as estado
FROM Licitaciones_Cabecera;
```

---

## IMPLEMENTACIÓN

### Paso 1: Modificar cargador.py

**Archivo**: `1_motor_etl/cargador.py`  
**Líneas**: 60-68

**Código Actual**:
```python
def determinar_estado(tender_status, item_status):
    st_item = safe_str(item_status)
    if st_item: return st_item.upper()
    
    st = safe_str(tender_status).lower()
    if not st: return "DESCONOCIDO"

    mapping = {'active': 'CONVOCADO', 'complete': 'CONTRATADO', 'cancelled': 'CANCELADO', 'unsuccessful': 'DESIERTO', 'withdrawn': 'NULO', 'planned': 'PROGRAMADO', 'awarded': 'ADJUDICADO'}
    return mapping.get(st, st.upper())
```

**Código NUEVO**:
```python
def determinar_estado(tender_status, item_status):
    """
    Retorna el estado ORIGINAL del JSON sin traducciones.
    Normaliza a MAYUSCULAS para consistencia.
    """
    # Priorizar estado del item si existe
    st_item = safe_str(item_status)
    if st_item: 
        return st_item.upper()
    
    # Si no hay estado de item, usar estado del tender
    st = safe_str(tender_status)
    if not st: 
        return "DESCONOCIDO"
    
    # Retornar valor ORIGINAL en mayúsculas
    return st.upper()
```

### Paso 2: Limpiar y Recargar Datos

```sql
-- Limpiar datos actuales
DELETE FROM Licitaciones_Adjudicaciones;
DELETE FROM Licitaciones_Cabecera;
DELETE FROM control_cargas;
```

```cmd
-- Recargar con nuevo código
.\ejecutar_proyecto.bat
```

### Paso 3: Crear Vista SQL (Opcional)

```sql
CREATE VIEW Licitaciones_Cabecera_ES AS
SELECT 
    id_convocatoria,
    ocid,
    nomenclatura,
    descripcion,
    comprador,
    categoria,
    tipo_procedimiento,
    monto_estimado,
    moneda,
    fecha_publicacion,
    CASE estado_proceso
        WHEN 'ACTIVE' THEN 'CONVOCADO'
        WHEN 'COMPLETE' THEN 'CONTRATADO'
        WHEN 'AWARDED' THEN 'ADJUDICADO'
        WHEN 'CANCELLED' THEN 'CANCELADO'
        WHEN 'UNSUCCESSFUL' THEN 'DESIERTO'
        WHEN 'WITHDRAWN' THEN 'NULO'
        WHEN 'PLANNED' THEN 'PROGRAMADO'
        ELSE estado_proceso
    END AS estado_proceso_es,
    estado_proceso as estado_proceso_original,
    ubicacion_completa,
    departamento,
    provincia,
    distrito,
    archivo_origen,
    fecha_carga,
    last_update
FROM Licitaciones_Cabecera;
```

---

## VERIFICACIÓN

### Consulta 1: Ver Distribución de Estados

```sql
SELECT estado_proceso, COUNT(*) as cantidad
FROM Licitaciones_Cabecera
GROUP BY estado_proceso
ORDER BY cantidad DESC;
```

**Resultado Esperado**:
```
COMPLETE         4,625
ACTIVE           1,770
WITHDRAWN        1,157
UNSUCCESSFUL       752
CONSENTIDO         670
...
```

### Consulta 2: Comparar Original vs Traducido

```sql
SELECT 
    estado_proceso as original,
    CASE estado_proceso
        WHEN 'ACTIVE' THEN 'CONVOCADO'
        WHEN 'COMPLETE' THEN 'CONTRATADO'
        ELSE estado_proceso
    END as traducido,
    COUNT(*) as cantidad
FROM Licitaciones_Cabecera
GROUP BY estado_proceso
ORDER BY cantidad DESC
LIMIT 10;
```

---

## RECOMENDACIÓN FINAL

**OPCIÓN RECOMENDADA**: Implementar Solución Propuesta

### Razones:
1. ✓ Cumple 100% con requisito del usuario
2. ✓ Mayor consistencia y trazabilidad
3. ✓ Código más simple y mantenible
4. ✓ Preparado para futuros cambios del SEACE
5. ✓ Vista SQL opcional para traducción cuando sea necesario

### Próximos Pasos:
1. Aprobar propuesta
2. Modificar `cargador.py`
3. Limpiar y recargar datos
4. Crear vista SQL para traducciones (opcional)
5. Actualizar documentación

---

**¿Proceder con la implementación?**

---

*Propuesta creada el 17 de diciembre de 2024*
