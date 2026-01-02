# 🔍 Análisis: Estados "DESCONOCIDO" en el Sistema

**Fecha**: 19 de diciembre de 2024  
**Problema**: 3,575 licitaciones tienen estado "DESCONOCIDO"

---

## 🐛 Causa Raíz

### Origen del Problema:
El estado "DESCONOCIDO" se asigna en el **ETL (cargador.py)** cuando los archivos JSON de SEACE **no contienen** el campo `statusDetails`.

### Código Responsable:

**Archivo**: `1_motor_etl/cargador.py`

#### Líneas 188-201 (Estado de Proceso):
```python
estado = 'DESCONOCIDO'  # Valor por defecto
awards = compiled.get('awards', [])
if awards and len(awards) > 0:
    first_award = awards[0]
    items = first_award.get('items', [])
    if items and len(items) > 0:
        estado_raw = items[0].get('statusDetails')
        if estado_raw:
            estado = safe_str(estado_raw).upper()
# Si no encuentra statusDetails → queda "DESCONOCIDO"
```

#### Líneas 239-248 (Estado de Item):
```python
items = aw.get('items', [])
estado_award = 'DESCONOCIDO'  # Valor por defecto
if items and len(items) > 0:
    estado_award = safe_str(items[0].get('statusDetails'), 50)
    if not estado_award:
        estado_award = 'DESCONOCIDO'
# Si no encuentra statusDetails → queda "DESCONOCIDO"
```

---

## 📊 Datos Actuales

### Distribución de Estados:

| Estado | Cantidad | Porcentaje |
|--------|----------|------------|
| **CONTRATADO** | 4,858 | 48.4% |
| **DESCONOCIDO** | 3,575 | 35.6% |
| **CONSENTIDO** | 967 | 9.6% |
| **ADJUDICADO** | 643 | 6.4% |

**Total**: 10,043 licitaciones

---

## 🔍 ¿Por qué falta `statusDetails`?

### Posibles Razones:

1. **Licitaciones en Proceso**
   - Aún no tienen adjudicación
   - No han llegado a fase de contrato
   - Estado: En convocatoria, evaluación, etc.

2. **Licitaciones Canceladas/Desiertas**
   - No tuvieron ganador
   - Fueron declaradas desiertas
   - Canceladas por la entidad

3. **Datos Incompletos en SEACE**
   - Error en la fuente de datos
   - Campos no actualizados
   - Problemas de sincronización

4. **Licitaciones Antiguas**
   - Datos históricos sin campo `statusDetails`
   - Cambios en estructura del JSON OCDS

---

## ✅ Soluciones Propuestas

### Opción 1: Mapeo Inteligente (Recomendada)

Usar otros campos del JSON para inferir el estado:

```python
def determinar_estado_inteligente(tender, awards):
    """
    Intenta determinar el estado usando múltiples fuentes.
    """
    # 1. Intentar statusDetails (actual)
    if awards and len(awards) > 0:
        first_award = awards[0]
        items = first_award.get('items', [])
        if items and len(items) > 0:
            estado_raw = items[0].get('statusDetails')
            if estado_raw:
                return safe_str(estado_raw).upper()
    
    # 2. Fallback: tender.status
    tender_status = tender.get('status')
    if tender_status:
        # Mapear estados de tender a estados conocidos
        status_map = {
            'active': 'EN_CONVOCATORIA',
            'complete': 'COMPLETADO',
            'cancelled': 'CANCELADO',
            'unsuccessful': 'DESIERTO'
        }
        return status_map.get(tender_status, tender_status.upper())
    
    # 3. Fallback: award.status
    if awards and len(awards) > 0:
        award_status = awards[0].get('status')
        if award_status:
            status_map = {
                'active': 'ADJUDICADO',
                'pending': 'PENDIENTE',
                'cancelled': 'CANCELADO'
            }
            return status_map.get(award_status, award_status.upper())
    
    # 4. Último recurso
    return 'SIN_ESTADO'
```

### Opción 2: Investigar JSON Original

Revisar los archivos JSON para ver qué otros campos tienen:

```bash
# Buscar licitaciones sin statusDetails
grep -l "DESCONOCIDO" 1_database/*.json
```

### Opción 3: Mapeo en Frontend

Cambiar "DESCONOCIDO" por un término más apropiado:

```javascript
// frontend/src/utils/formatters.js
export const formatEstado = (estado) => {
    const estadoMap = {
        'DESCONOCIDO': 'SIN INFORMACIÓN',
        'CONTRATADO': 'Contratado',
        'CONSENTIDO': 'Consentido',
        'ADJUDICADO': 'Adjudicado'
    };
    return estadoMap[estado] || estado;
};
```

### Opción 4: Actualización Manual

Ejecutar un script para actualizar los 3,575 registros:

```sql
-- Opción A: Cambiar a estado más descriptivo
UPDATE licitaciones_cabecera 
SET estado_proceso = 'SIN_INFORMACION' 
WHERE estado_proceso = 'DESCONOCIDO';

-- Opción B: Intentar inferir del estado de adjudicaciones
UPDATE licitaciones_cabecera c
INNER JOIN (
    SELECT id_convocatoria, MAX(estado_item) as estado_inferido
    FROM licitaciones_adjudicaciones
    WHERE estado_item != 'DESCONOCIDO'
    GROUP BY id_convocatoria
) a ON c.id_convocatoria = a.id_convocatoria
SET c.estado_proceso = a.estado_inferido
WHERE c.estado_proceso = 'DESCONOCIDO';
```

---

## 🎯 Recomendación

### Solución Inmediata (Frontend):

Cambiar la visualización de "DESCONOCIDO" a algo más amigable:

**Archivo**: `frontend/src/utils/formatters.js`

```javascript
export const formatEstado = (estado) => {
    if (!estado || estado === 'DESCONOCIDO') {
        return 'Sin Información';
    }
    
    // Capitalizar primera letra
    return estado.charAt(0) + estado.slice(1).toLowerCase();
};
```

**Uso en componentes**:
```javascript
import { formatEstado } from '../utils/formatters';

// En lugar de:
<span>{licitacion.estado_proceso}</span>

// Usar:
<span>{formatEstado(licitacion.estado_proceso)}</span>
```

### Solución a Mediano Plazo (ETL):

1. **Modificar `cargador.py`** para usar mapeo inteligente
2. **Re-ejecutar ETL** para actualizar los 3,575 registros
3. **Validar** que los nuevos estados sean correctos

### Solución a Largo Plazo:

1. **Contactar a SEACE** para reportar datos incompletos
2. **Documentar** qué licitaciones tienen datos faltantes
3. **Crear reporte** de calidad de datos

---

## 📝 Impacto

### Afecta a:
- ✅ Dashboard (gráficos de estado)
- ✅ Estadísticas (distribución por estado)
- ✅ Reportes (análisis por estado)
- ✅ Filtros (filtrar por estado)

### NO Afecta a:
- ✅ Garantías (se calcula por entidad_financiera)
- ✅ Montos (independiente del estado)
- ✅ Ubicaciones (independiente del estado)

---

## 🧪 Investigación Adicional

### Script para Analizar JSON:

```python
import json
import os

def analizar_desconocidos():
    """
    Analiza archivos JSON para entender por qué faltan statusDetails
    """
    carpeta = "1_database"
    sin_status = []
    
    for archivo in os.listdir(carpeta):
        if not archivo.endswith('.json'):
            continue
            
        with open(os.path.join(carpeta, archivo), 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for record in data.get('records', []):
                compiled = record.get('compiledRelease', {})
                awards = compiled.get('awards', [])
                
                if awards:
                    items = awards[0].get('items', [])
                    if items:
                        status = items[0].get('statusDetails')
                        if not status:
                            # Guardar para análisis
                            sin_status.append({
                                'ocid': record.get('ocid'),
                                'tender_status': compiled.get('tender', {}).get('status'),
                                'award_status': awards[0].get('status'),
                                'archivo': archivo
                            })
    
    print(f"Total sin statusDetails: {len(sin_status)}")
    # Analizar patrones
    tender_statuses = {}
    for item in sin_status:
        ts = item['tender_status']
        tender_statuses[ts] = tender_statuses.get(ts, 0) + 1
    
    print("\nDistribución de tender.status:")
    for status, count in sorted(tender_statuses.items(), key=lambda x: x[1], reverse=True):
        print(f"  {status}: {count}")
```

---

## ✅ Acción Recomendada

**Para resolver inmediatamente**:

1. Actualizar `formatters.js` para mostrar "Sin Información" en lugar de "DESCONOCIDO"
2. Aplicar el formateador en todos los componentes
3. Documentar que estos registros requieren investigación

**¿Quieres que implemente la solución de formateo en el frontend?**

---

**Generado automáticamente** - 19/12/2024 22:30
