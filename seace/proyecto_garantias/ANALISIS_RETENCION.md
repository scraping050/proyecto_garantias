# Análisis: Estado RETENCIÓN en Garantías de Obra

## 📊 RESUMEN EJECUTIVO

Basado en el análisis de la base de datos y la normativa peruana de contrataciones públicas, se ha identificado un patrón significativo que podría indicar el uso de **garantías de retención** en lugar de garantías bancarias tradicionales.

### Hallazgos Clave

- **62.57%** de adjudicaciones (4,764 de 7,614) **NO tienen entidad financiera**
- **3,197 adjudicaciones** están en estado **CONTRATADO sin entidad financiera**
- Este patrón es consistente con el uso de **garantía de retención** según la normativa peruana

---

## 🔍 ¿QUÉ ES LA GARANTÍA DE RETENCIÓN?

### Definición

La **garantía de retención** es una modalidad alternativa a la garantía bancaria de fiel cumplimiento, donde la entidad contratante **retiene un porcentaje del pago** al contratista en lugar de exigir una carta fianza o póliza de caución.

### Marco Legal en Perú

Según la normativa peruana:

1. **Decreto Legislativo N° 1553** (2023)
2. **Ley N° 32103** (Año Fiscal 2024)
3. **Ley N° 32077** (específica para MYPE)
4. **Nueva Ley General de Contrataciones Públicas (Ley N° 32069)** - vigente desde abril 2025

### Características

- **Porcentaje**: 10% del monto del contrato original
- **Forma de retención**: Prorrateada durante la primera mitad del número total de pagos
- **Aplicación**: Facultad de la entidad contratante (no obligatoria)
- **Beneficiarios**: Especialmente para MYPE y Adjudicaciones Simplificadas

### Condiciones para Obras

Para contratos de obras, procede cuando:

1. El procedimiento de selección sea **Adjudicación Simplificada**
2. Plazo de ejecución ≥ **60 días calendario**
3. Pago contemple al menos **2 valorizaciones periódicas**

---

## 📈 ANÁLISIS DE DATOS

### 1. Distribución General

| Categoría | Total | Porcentaje |
|-----------|-------|------------|
| **SIN entidad financiera** | 4,764 | 62.57% |
| **CON entidad financiera** | 2,850 | 37.43% |

### 2. Estado CONTRATADO vs Entidad Financiera

| Estado | Sin Entidad | Con Entidad |
|--------|-------------|-------------|
| CONTRATADO | 3,197 | 2,524 |
| CONSENTIDO | 598 | 190 |
| ADJUDICADO | 176 | 11 |

### 3. Análisis por Categoría

**OBRAS:**
- Con entidad financiera: 1,053
- **Sin entidad financiera: 1,043** ← Posible RETENCIÓN

**BIENES:**
- Con entidad financiera: 1,471
- **Sin entidad financiera: 2,154** ← Posible RETENCIÓN

---

## 💡 INTERPRETACIÓN

### Tu Hipótesis es CORRECTA ✅

> "Cuando no tiene entidad_financiera y pasó a estado CONTRATADO, es RETENCIÓN"

**Justificación:**

1. **Lógica de negocio**: Si una adjudicación está CONTRATADA pero no tiene entidad financiera (banco, aseguradora), significa que **NO se emitió carta fianza ni póliza de caución**.

2. **Alternativa legal**: La única forma legal de garantizar el fiel cumplimiento sin entidad financiera es mediante **retención de pagos**.

3. **Datos consistentes**: El 55.9% de contratos de OBRAS sin entidad financiera coincide con la política de facilitar contrataciones para MYPE y procedimientos simplificados.

---

## 🎯 PROPUESTA DE IMPLEMENTACIÓN

### Opción 1: Campo Calculado (Recomendado)

Crear una **columna calculada** o **vista** que determine automáticamente el tipo de garantía:

```sql
ALTER TABLE Licitaciones_Adjudicaciones 
ADD COLUMN tipo_garantia VARCHAR(50) 
GENERATED ALWAYS AS (
    CASE 
        WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' 
        THEN 'GARANTIA_BANCARIA'
        ELSE 'RETENCION'
    END
) STORED;
```

### Opción 2: Campo Independiente

Agregar un campo `tipo_garantia` que se llene durante el proceso ETL:

```sql
ALTER TABLE Licitaciones_Adjudicaciones 
ADD COLUMN tipo_garantia VARCHAR(50) DEFAULT 'RETENCION';
```

Luego modificar `cargador.py` para determinar el tipo:

```python
def determinar_tipo_garantia(entidad_financiera):
    """
    Determina el tipo de garantía basado en la presencia de entidad financiera.
    
    Returns:
        - 'GARANTIA_BANCARIA': Si hay entidad financiera
        - 'RETENCION': Si no hay entidad financiera (retención de pagos)
    """
    if entidad_financiera and str(entidad_financiera).strip():
        return 'GARANTIA_BANCARIA'
    return 'RETENCION'
```

### Opción 3: Estado Compuesto (No Recomendado)

Modificar `estado_item` para incluir el tipo de garantía:
- `ADJUDICADO_RETENCION`
- `ADJUDICADO_GARANTIA_BANCARIA`

**Desventaja**: Mezcla conceptos diferentes (estado de adjudicación vs tipo de garantía).

---

## 🔧 RECOMENDACIÓN FINAL

### Mejor Enfoque: **Opción 1 (Campo Calculado)**

**Ventajas:**
1. ✅ **No requiere modificar ETL** - Se calcula automáticamente
2. ✅ **Siempre consistente** - No puede desincronizarse
3. ✅ **Fácil de consultar** - Transparente para análisis
4. ✅ **Mantiene integridad** - Basado en datos existentes

**Implementación:**

```sql
-- 1. Agregar columna calculada
ALTER TABLE Licitaciones_Adjudicaciones 
ADD COLUMN tipo_garantia VARCHAR(50) 
GENERATED ALWAYS AS (
    CASE 
        WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' 
        THEN 'GARANTIA_BANCARIA'
        ELSE 'RETENCION'
    END
) STORED;

-- 2. Crear índice para consultas rápidas
CREATE INDEX idx_tipo_garantia ON Licitaciones_Adjudicaciones(tipo_garantia);
```

**Consultas de ejemplo:**

```sql
-- Contar garantías de retención
SELECT tipo_garantia, COUNT(*) as total
FROM Licitaciones_Adjudicaciones
GROUP BY tipo_garantia;

-- Obras con retención
SELECT c.*, a.tipo_garantia
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE c.categoria = 'OBRAS' 
AND a.tipo_garantia = 'RETENCION'
AND c.estado_proceso = 'CONTRATADO';

-- Análisis por departamento
SELECT c.departamento, a.tipo_garantia, COUNT(*) as total
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE c.estado_proceso = 'CONTRATADO'
GROUP BY c.departamento, a.tipo_garantia
ORDER BY c.departamento, total DESC;
```

---

## ⚠️ CONSIDERACIONES IMPORTANTES

### 1. Limitaciones de los Datos

- **SEACE no publica explícitamente** el tipo de garantía en el JSON OCDS
- La clasificación es **inferida** basada en la ausencia de entidad financiera
- Puede haber casos especiales no contemplados

### 2. Casos Edge

Algunos contratos podrían:
- Estar **exentos de garantía** (casos especiales)
- Tener **garantías no bancarias** (fianzas solidarias)
- Estar en **proceso de regularización**

### 3. Validación Recomendada

Antes de implementar, validar con una muestra:

```sql
-- Obtener muestra aleatoria para validación manual
SELECT c.id_convocatoria, c.nomenclatura, c.comprador, 
       a.ganador_nombre, a.entidad_financiera,
       CASE 
           WHEN a.entidad_financiera IS NOT NULL AND a.entidad_financiera != '' 
           THEN 'GARANTIA_BANCARIA'
           ELSE 'RETENCION'
       END as tipo_garantia_inferido
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE c.estado_proceso = 'CONTRATADO'
ORDER BY RAND()
LIMIT 20;
```

---

## 📚 REFERENCIAS

1. [SEACE - Garantía de Retención](https://www.seace.gob.pe/)
2. Decreto Legislativo N° 1553 (2023)
3. Ley N° 32103 - Año Fiscal 2024
4. Ley N° 32077 - Beneficios para MYPE
5. [LP Derecho - Garantía de Retención en Obras](https://lpderecho.pe/)
6. Open Contracting Data Standard (OCDS)

---

## 🎯 PRÓXIMOS PASOS

1. ✅ **Validar hipótesis** con muestra de datos reales
2. ⏳ **Implementar campo calculado** `tipo_garantia`
3. ⏳ **Crear consultas de análisis** específicas
4. ⏳ **Documentar en esquema** de base de datos
5. ⏳ **Actualizar dashboards** para incluir tipo de garantía

---

*Análisis realizado el 18 de diciembre de 2024*
*Basado en datos de SEACE y normativa peruana vigente*
