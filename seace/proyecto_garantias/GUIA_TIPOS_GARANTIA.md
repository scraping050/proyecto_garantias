# Guía de Interpretación: Tipos de Garantía en SEACE

## 📚 Introducción

Este documento explica cómo interpretar y utilizar la clasificación de tipos de garantía implementada en la base de datos del proyecto.

---

## 🎯 Tipos de Garantía

### 1. GARANTIA_BANCARIA

**Definición**: Garantía emitida por una entidad financiera (banco, aseguradora, cooperativa) que respalda el cumplimiento del contrato.

**Características**:
- Requiere emisión de carta fianza o póliza de caución
- Emitida por entidad financiera regulada
- Costo adicional para el contratista (comisión bancaria)
- Típica en contratos de alto monto

**Identificación en BD**: Campo `entidad_financiera` tiene valor (no NULL, no vacío)

**Ejemplos de entidades**:
- BBVA
- BCP (Banco de Crédito del Perú)
- Interbank
- CESCE Perú (Aseguradora)
- AVLA Perú (Aseguradora)
- FOGAPI

### 2. RETENCION

**Definición**: Garantía mediante retención de un porcentaje del pago al contratista durante la ejecución del contrato.

**Características**:
- NO requiere entidad financiera
- Retención del 10% del monto del contrato
- Prorrateada en la primera mitad de pagos
- Facilita acceso a MYPE y pequeños contratistas
- Reduce costos para el contratista (no hay comisiones bancarias)

**Identificación en BD**: Campo `entidad_financiera` es NULL o vacío

**Marco Legal**:
- Decreto Legislativo N° 1553 (2023)
- Ley N° 32103 (Año Fiscal 2024)
- Ley N° 32077 (específica para MYPE)
- Ley N° 32069 (Nueva Ley General de Contrataciones)

---

## 📊 Estadísticas Actuales

Según análisis de la base de datos:

| Tipo | Cantidad | Porcentaje | Monto Total |
|------|----------|------------|-------------|
| **RETENCION** | 4,764 | 62.57% | S/ 24.6B |
| **GARANTIA_BANCARIA** | 2,850 | 37.43% | S/ 16.3B |

**Observación**: Aunque las retenciones son más frecuentes (62.57%), representan un monto total mayor debido a que incluyen contratos de obras de gran envergadura.

---

## 🔍 Consultas SQL Útiles

### Listar adjudicaciones por tipo de garantía

```sql
SELECT tipo_garantia, COUNT(*) as total
FROM Licitaciones_Adjudicaciones
GROUP BY tipo_garantia;
```

### Obras con retención (CONTRATADAS)

```sql
SELECT c.id_convocatoria, c.nomenclatura, a.monto_adjudicado, c.departamento
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE c.categoria = 'OBRAS'
AND a.tipo_garantia = 'RETENCION'
AND c.estado_proceso = 'CONTRATADO'
ORDER BY a.monto_adjudicado DESC;
```

### Distribución por departamento

```sql
SELECT c.departamento, a.tipo_garantia, COUNT(*) as total
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE c.estado_proceso = 'CONTRATADO'
GROUP BY c.departamento, a.tipo_garantia
ORDER BY c.departamento, total DESC;
```

### Análisis de montos promedio

```sql
SELECT 
    a.tipo_garantia,
    c.categoria,
    COUNT(*) as cantidad,
    ROUND(AVG(a.monto_adjudicado), 2) as monto_promedio,
    ROUND(SUM(a.monto_adjudicado), 2) as monto_total
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE c.estado_proceso = 'CONTRATADO'
AND a.monto_adjudicado > 0
GROUP BY a.tipo_garantia, c.categoria
ORDER BY c.categoria, monto_total DESC;
```

### Identificar casos especiales (SIN_GARANTIA)

```sql
SELECT c.id_convocatoria, c.nomenclatura, a.entidad_financiera, a.tipo_garantia
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
WHERE a.entidad_financiera LIKE '%SIN_GARANTIA%'
LIMIT 20;
```

---

## ⚠️ Casos Especiales

### "SIN_GARANTIA" como Entidad Financiera

Algunos registros tienen el valor `SIN_GARANTIA` en el campo `entidad_financiera`. Estos se clasifican como **GARANTIA_BANCARIA** porque el campo no está vacío.

**Interpretación**: Podría indicar:
1. Contratos exentos de garantía por normativa especial
2. Garantías no bancarias (fianzas solidarias)
3. Datos en proceso de regularización

**Recomendación**: Revisar manualmente estos casos para determinar si deberían ser RETENCION.

### Obras de Alto Monto con Retención

Se han identificado obras con retención por montos superiores a S/ 600M. Esto es válido según la normativa, aunque poco común.

**Ejemplo**: ID 1084610 - S/ 678,197,013.61 (LIMA)

---

## 🎓 Interpretación para Análisis

### ¿Cuándo usar cada tipo?

**Para análisis de acceso a contrataciones públicas**:
- RETENCION indica facilidades para MYPE y pequeños contratistas
- GARANTIA_BANCARIA indica contratos que requieren mayor capacidad financiera

**Para análisis de costos**:
- RETENCION reduce costos de transacción (no hay comisiones bancarias)
- GARANTIA_BANCARIA implica costos adicionales (1-3% del monto)

**Para análisis regional**:
- Departamentos con alta proporción de RETENCION pueden indicar políticas de inclusión
- Lima tiene el mayor número de retenciones (1,277) pero también muchas garantías bancarias

---

## 📈 Tendencias Observadas

1. **BIENES**: Mayor uso de retención (59.4%)
2. **OBRAS**: Distribución equilibrada (50.3% bancaria, 49.7% retención)
3. **LIMA**: Concentra el 40% de todas las retenciones del país
4. **Monto promedio**: Retenciones tienen monto promedio mayor (S/ 7.7M vs S/ 6.5M)

---

## 🔧 Scripts de Análisis

El proyecto incluye scripts Python para análisis:

1. **`validar_tipo_garantia.py`**: Muestra aleatoria para validación manual
2. **`estadisticas_garantias.py`**: Estadísticas completas por categoría, departamento, etc.
3. **`analizar_retencion.py`**: Análisis específico de patrones de retención

**Ejecutar**:
```bash
python validar_tipo_garantia.py
python estadisticas_garantias.py
```

---

## 📚 Referencias

- [ANALISIS_RETENCION.md](file:///c:/laragon/www/proyecto_garantias/ANALISIS_RETENCION.md) - Análisis completo y normativa
- [Decreto Legislativo N° 1553](https://www.seace.gob.pe/)
- [Ley N° 32103 - Año Fiscal 2024](https://www.seace.gob.pe/)
- [Open Contracting Data Standard (OCDS)](https://standard.open-contracting.org/)

---

*Guía creada el 18 de diciembre de 2024*
*Versión 1.0*
