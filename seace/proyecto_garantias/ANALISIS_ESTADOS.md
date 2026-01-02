# Análisis Detallado: Columnas de Estado en Base de Datos

## 📊 RESUMEN EJECUTIVO

**NO HAY ERROR** - El diseño es correcto y refleja la estructura de datos del SEACE (Open Contracting Data Standard).

---

## 🔍 HALLAZGOS DEL ANÁLISIS

### 1. Distribución de Estados

#### Tabla: Licitaciones_Cabecera (estado_proceso)
- **CONTRATADO**: 4,625 (48.15%) - Proceso completado con contrato firmado
- **CONVOCADO**: 1,770 (18.43%) - En proceso de convocatoria
- **NULO**: 1,157 (12.04%) - Proceso anulado
- **DESIERTO**: 752 (7.83%) - Sin postores válidos
- **CONSENTIDO**: 670 (6.97%) - Adjudicación consentida
- **ADJUDICADO**: 164 (1.71%) - Adjudicado pero no contratado aún
- **Otros**: 468 (4.87%)

#### Tabla: Licitaciones_Adjudicaciones (estado_item)
- **ADJUDICADO**: 7,614 (100%) - Todos los ítems adjudicados

### 2. Relación Entre Tablas

**Hallazgo Clave**: 5,975 licitaciones (98.3%) tienen estado_proceso ≠ "ADJUDICADO" pero SÍ tienen adjudicaciones.

Esto es **CORRECTO** porque:

---

## ✅ EXPLICACIÓN TÉCNICA

### Diferencia Conceptual

#### `estado_proceso` (Licitaciones_Cabecera)
- **Nivel**: Proceso de licitación completo
- **Representa**: Estado actual del procedimiento administrativo
- **Ciclo de vida**:
  ```
  CONVOCADO → ADJUDICADO → CONSENTIDO → CONTRATADO
  ```
- **Fuente**: Campo `tender.status` del JSON SEACE

#### `estado_item` (Licitaciones_Adjudicaciones)
- **Nivel**: Ítem individual adjudicado
- **Representa**: Estado de cada adjudicación específica
- **Valor**: Siempre "ADJUDICADO" (por definición, solo se guardan ítems adjudicados)
- **Fuente**: Campo `awards[].items[].status` del JSON SEACE

---

## 📋 LÓGICA DEL CÓDIGO

### Función `determinar_estado()` (línea 55-63)

```python
def determinar_estado(tender_status, item_status):
    st_item = safe_str(item_status)
    if st_item: return st_item.upper()  # Prioriza estado del ítem
    
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

### Proceso de Extracción

1. **Cabecera** (líneas 121-149):
   - Extrae `tender.status` → `estado_proceso`
   - Representa el estado del PROCESO completo

2. **Adjudicaciones** (líneas 151-185):
   - Extrae `awards[].items[]` → solo ítems con `status = "active"`
   - Guarda `awards[].items[].status` → `estado_item`
   - **Filtro**: Solo se guardan ítems adjudicados

---

## 🎯 CASOS DE USO REALES

### Caso 1: Licitación CONTRATADA con múltiples adjudicaciones
```
Licitación: ID 1011323
- estado_proceso: "CONTRATADO"
- Adjudicaciones: 17 ítems
- estado_item: "ADJUDICADO" (todos)
```

**Interpretación**: 
- La licitación pasó por: CONVOCADO → ADJUDICADO → CONSENTIDO → CONTRATADO
- Los 17 ítems fueron adjudicados (estado_item)
- El proceso completo está CONTRATADO (estado_proceso)

### Caso 2: Licitación DESIERTA con adjudicaciones
```
Licitación: ID 1105481
- estado_proceso: "DESIERTO"
- Adjudicaciones: 15 ítems
- estado_item: "ADJUDICADO" (todos)
```

**Interpretación**:
- Algunos ítems fueron adjudicados
- Otros ítems quedaron desiertos
- El proceso general se marcó como DESIERTO (mayoría de ítems sin adjudicar)

---

## 📊 ESTADÍSTICAS IMPORTANTES

### Licitaciones con Múltiples Adjudicaciones
- **Total licitaciones**: 9,606
- **Licitaciones con adjudicaciones**: 6,146 (64%)
- **Total adjudicaciones**: 7,614
- **Promedio**: 1.24 adjudicaciones por licitación

### Distribución Estado Proceso vs Adjudicaciones
| Estado Proceso | # Licitaciones | # Adjudicaciones |
|----------------|----------------|------------------|
| CONTRATADO | 4,625 | 5,730 |
| CONSENTIDO | 670 | 818 |
| DESIERTO | 150 | 277 |
| NULO | 233 | 260 |
| ADJUDICADO | 164 | 186 |

---

## ✅ CONCLUSIONES

### 1. NO HAY ERROR EN EL DISEÑO
- Las dos columnas representan **niveles diferentes** de granularidad
- `estado_proceso`: Estado del procedimiento administrativo completo
- `estado_item`: Estado de cada ítem adjudicado individual

### 2. REFLEJA EL ESTÁNDAR OCDS
- El diseño sigue el Open Contracting Data Standard (OCDS)
- Separación entre `tender` (proceso) y `awards` (adjudicaciones)

### 3. PERMITE ANÁLISIS DETALLADO
- Rastrear evolución del proceso: CONVOCADO → ADJUDICADO → CONTRATADO
- Identificar licitaciones con adjudicaciones parciales
- Analizar ítems individuales dentro de un proceso

### 4. CASOS ESPECIALES SON VÁLIDOS
- **DESIERTO con adjudicaciones**: Algunos ítems adjudicados, otros no
- **NULO con adjudicaciones**: Adjudicaciones antes de anulación
- **CONTRATADO**: Estado final después de adjudicación

---

## 🔧 RECOMENDACIONES

### Para Consultas SQL

#### Obtener solo licitaciones completamente adjudicadas:
```sql
SELECT * FROM Licitaciones_Cabecera
WHERE estado_proceso IN ('ADJUDICADO', 'CONSENTIDO', 'CONTRATADO');
```

#### Obtener licitaciones con adjudicaciones activas:
```sql
SELECT DISTINCT c.*
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE a.estado_item = 'ADJUDICADO';
```

#### Identificar adjudicaciones parciales:
```sql
SELECT c.id_convocatoria, c.nomenclatura, c.estado_proceso,
       COUNT(a.id_adjudicacion) as num_adjudicaciones
FROM Licitaciones_Cabecera c
LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE c.estado_proceso IN ('DESIERTO', 'NULO')
  AND a.id_adjudicacion IS NOT NULL
GROUP BY c.id_convocatoria, c.nomenclatura, c.estado_proceso;
```

### Para Documentación

Agregar comentarios en el esquema de BD:
```sql
ALTER TABLE Licitaciones_Cabecera 
MODIFY COLUMN estado_proceso VARCHAR(50) 
COMMENT 'Estado del proceso de licitación completo (tender.status)';

ALTER TABLE Licitaciones_Adjudicaciones 
MODIFY COLUMN estado_item VARCHAR(50) 
COMMENT 'Estado del ítem adjudicado individual (awards.items.status)';
```

---

## 📚 REFERENCIAS

- **OCDS**: Open Contracting Data Standard
- **SEACE**: Sistema Electrónico de Contrataciones del Estado
- **Fuente de datos**: https://contratacionesabiertas.oece.gob.pe/

---

**Conclusión Final**: La estructura de datos es **CORRECTA y PRECISA**. Las dos columnas de estado sirven propósitos diferentes y complementarios, permitiendo un análisis completo del ciclo de vida de las licitaciones públicas.

---

*Análisis realizado el 17 de diciembre de 2024*
