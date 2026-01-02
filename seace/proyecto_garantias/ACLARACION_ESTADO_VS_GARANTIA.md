# ACLARACIÓN IMPORTANTE: Estado vs Tipo de Garantía

## 🚨 NO ESTAMOS CLASIFICANDO EL ESTADO DEL PROCESO

Hay una diferencia **FUNDAMENTAL** entre dos conceptos que se pueden confundir:

---

## 📊 Dos Conceptos Diferentes

### 1️⃣ ESTADO DEL PROCESO (`estado_proceso`)

**¿Qué es?** La etapa en la que se encuentra el **proceso de licitación**

**Ubicación en BD**: Tabla `Licitaciones_Cabecera`, columna `estado_proceso`

**Valores posibles**:
- `CONVOCADO` - En proceso de convocatoria
- `ADJUDICADO` - Ya se adjudicó pero no se firmó contrato
- `CONSENTIDO` - Adjudicación consentida (sin apelaciones)
- `CONTRATADO` - Contrato firmado ✅
- `DESIERTO` - Sin postores válidos
- `NULO` - Proceso anulado
- `CANCELADO` - Proceso cancelado
- `APELADO` - En proceso de apelación

**Fuente**: Campo `tender.status` del JSON de SEACE

---

### 2️⃣ TIPO DE GARANTÍA (`tipo_garantia`) ⭐ **ESTO ES LO QUE IMPLEMENTAMOS**

**¿Qué es?** El **tipo de garantía** que se usa para asegurar el cumplimiento del contrato

**Ubicación en BD**: Tabla `Licitaciones_Adjudicaciones`, columna `tipo_garantia`

**Valores posibles**:
- `GARANTIA_BANCARIA` - Carta fianza o póliza de caución (emitida por banco/aseguradora)
- `RETENCION` - Retención del 10% de los pagos al contratista

**Criterio de clasificación**:
```
SI entidad_financiera tiene valor → GARANTIA_BANCARIA
SI entidad_financiera está vacío → RETENCION
```

---

## 📋 Ejemplo Real: Convocatoria 1001070

```
ID Convocatoria: 1001070
Nomenclatura: LP-SM-2-2024-IN/OGIN-1
Categoría: BIENES
Monto: S/ 4,610,000.00
Ganador: AUTOESPAR S A

┌─────────────────────────────────────────────────────────┐
│ ESTADO DEL PROCESO: CONSENTIDO                          │
│ (Adjudicación consentida, aún no firmado el contrato)   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ TIPO DE GARANTÍA: RETENCION                             │
│ (No tiene entidad financiera, usa retención de pagos)   │
└─────────────────────────────────────────────────────────┘
```

**Interpretación correcta**:
- ✅ El proceso está en estado **CONSENTIDO** (aún no contratado)
- ✅ Cuando se firme el contrato, usará garantía de **RETENCIÓN** (no bancaria)

---

## 🔄 Ciclo de Vida del Proceso

```
CONVOCADO → ADJUDICADO → CONSENTIDO → CONTRATADO
                                          ↓
                                    [TIPO DE GARANTÍA]
                                    ├─ GARANTIA_BANCARIA (con entidad)
                                    └─ RETENCION (sin entidad)
```

---

## ❓ ¿Por Qué Puede Haber Diferencias entre OECE y SEACE?

### Posibles Razones:

1. **Momento de consulta diferente**
   - OECE puede mostrar el estado en tiempo real
   - Nuestra BD tiene datos de cuando se descargó el JSON
   - El estado puede haber cambiado de CONSENTIDO → CONTRATADO

2. **Fuente de datos diferente**
   - OECE: Base de datos en vivo
   - Nuestro proyecto: Archivos JSON descargados mensualmente
   - Puede haber desfase temporal

3. **Actualización de estados**
   - Los estados se actualizan conforme avanza el proceso
   - Un proceso CONSENTIDO eventualmente pasa a CONTRATADO

---

## ✅ Lo Que SÍ Implementamos

**NO** clasificamos el estado del proceso como "RETENCIÓN"

**SÍ** clasificamos el **tipo de garantía** basándonos en:

```sql
tipo_garantia = 
    CASE 
        WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' 
        THEN 'GARANTIA_BANCARIA'
        ELSE 'RETENCION'
    END
```

---

## 📊 Ejemplos de Combinaciones Válidas

| Estado Proceso | Tipo Garantía | Interpretación |
|----------------|---------------|----------------|
| CONSENTIDO | RETENCION | Adjudicado sin apelaciones, usará retención cuando se contrate |
| CONSENTIDO | GARANTIA_BANCARIA | Adjudicado sin apelaciones, usará garantía bancaria cuando se contrate |
| CONTRATADO | RETENCION | Contrato firmado con retención de pagos |
| CONTRATADO | GARANTIA_BANCARIA | Contrato firmado con carta fianza/póliza |
| ADJUDICADO | RETENCION | Adjudicado, usará retención cuando se consienta y contrate |
| DESIERTO | - | No hay adjudicación, no aplica tipo de garantía |

---

## 🎯 Consulta para Verificar

```sql
SELECT 
    c.id_convocatoria,
    c.estado_proceso,           -- Estado del PROCESO
    a.tipo_garantia,            -- Tipo de GARANTÍA
    a.entidad_financiera
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE c.id_convocatoria = '1001070';
```

**Resultado esperado**:
```
id_convocatoria: 1001070
estado_proceso: CONSENTIDO      ← Estado del proceso
tipo_garantia: RETENCION        ← Tipo de garantía
entidad_financiera: NULL        ← Por eso es RETENCION
```

---

## 🔍 Cómo Verificar en SEACE/OECE

1. **Buscar la convocatoria** en SEACE/OECE
2. **Ver el estado**: Puede ser CONSENTIDO, CONTRATADO, etc.
3. **Ver la garantía**: Buscar si tiene entidad financiera
   - Si tiene banco/aseguradora → GARANTIA_BANCARIA
   - Si NO tiene → RETENCION

---

## 📚 Script de Verificación

Usa este script para verificar cualquier convocatoria:

```bash
python buscar_convocatoria.py <id_convocatoria>
```

Ejemplo:
```bash
python buscar_convocatoria.py 1001070
```

---

## ✨ Conclusión

**ESTADO** y **TIPO DE GARANTÍA** son **DOS COSAS COMPLETAMENTE DIFERENTES**:

- **ESTADO** = ¿En qué etapa está el proceso? (CONVOCADO, CONSENTIDO, CONTRATADO, etc.)
- **TIPO DE GARANTÍA** = ¿Qué tipo de garantía usa? (BANCARIA o RETENCIÓN)

**Lo que implementamos**: Clasificación automática del **TIPO DE GARANTÍA**, NO del estado.

---

*Documento de aclaración creado el 18 de diciembre de 2024*
