# 🏛️ Sistema de Análisis de Garantías SEACE

## 📋 Descripción General

Sistema ETL (Extract, Transform, Load) automatizado para analizar licitaciones públicas del SEACE (Sistema Electrónico de Contrataciones del Estado) de Perú, con enfoque especial en el análisis de garantías de cumplimiento de contratos.

**Objetivo principal**: Procesar datos de licitaciones públicas del estándar OCDS (Open Contracting Data Standard) para identificar y clasificar tipos de garantías (bancarias vs retención) en contratos públicos.

---

## 🎯 Características Principales

### ✅ Pipeline ETL Completo
- **Descarga automática** de datos SEACE en formato JSON (OCDS)
- **Carga optimizada** a base de datos MySQL con validación de integridad
- **Enriquecimiento** con información de entidades financieras
- **Procesamiento IA** para extracción de datos de consorcios (Gemini/Groq)

### 📊 Análisis de Datos
- **10,043 licitaciones** procesadas (100% coincidencia con OECE oficial)
- **7,959 adjudicaciones** registradas
- **6,687 contratos** mapeados
- **Clasificación automática** de tipos de garantía:
  - 62.57% Retención (4,764 casos)
  - 37.43% Garantía Bancaria (2,850 casos)

### 🔒 Seguridad
- Gestión segura de credenciales mediante variables de entorno
- Sin archivos `.env` en código fuente
- Validación automática de configuración
- Documentación completa de seguridad

---

## 🗂️ Estructura del Proyecto

```
proyecto_garantias/
├── 1_motor_etl/              # Motor ETL principal
│   ├── descargador.py        # Descarga archivos JSON de SEACE
│   ├── cargador.py           # Carga datos a MySQL
│   ├── spider_garantias.py   # Enriquecimiento con datos bancarios
│   ├── etl_consorcios_ai.py  # Procesamiento IA (Gemini)
│   ├── etl_consorcios_groq.py # Procesamiento IA (Groq)
│   └── main_auto.py          # Orquestador del pipeline
│
├── 1_database/               # Archivos JSON descargados (24 meses)
│   ├── 2024-01_seace_v3.json
│   ├── 2024-02_seace_v3.json
│   └── ... (hasta 2025-12)
│
├── config/                   # Configuración segura
│   ├── secrets_manager.py    # Gestor de credenciales
│   └── __init__.py
│
├── evidencia_consorcios/     # PDFs de consorcios procesados
│
├── Scripts de análisis/      # Herramientas de auditoría
│   ├── comparar_con_oece.py
│   ├── analisis_completo_bd.py
│   ├── estadisticas_garantias.py
│   └── ... (40+ scripts)
│
└── Documentación/            # Guías y reportes
    ├── QUICKSTART.md
    ├── COMO_EJECUTAR.md
    ├── SECURITY.md
    ├── GUIA_TIPOS_GARANTIA.md
    └── ... (15+ documentos)
```

---

## 🗄️ Esquema de Base de Datos

### Tablas Principales

#### `Licitaciones_Cabecera`
Información principal de cada licitación:
- `id_convocatoria` (PK)
- `ocid` (OCDS ID único)
- `nomenclatura`, `descripcion`
- `comprador`, `categoria`
- `tipo_procedimiento`
- `monto_estimado`, `moneda`
- `fecha_publicacion`, `estado_proceso`
- `departamento`, `provincia`, `distrito`

#### `Licitaciones_Adjudicaciones`
Adjudicaciones y ganadores:
- `id_adjudicacion` (PK)
- `id_convocatoria` (FK)
- `id_contrato`
- `ganador_nombre`, `ganador_ruc`
- `monto_adjudicado`, `fecha_adjudicacion`
- `estado_item`
- `entidad_financiera`
- **`tipo_garantia`** (GENERATED COLUMN):
  - `GARANTIA_BANCARIA`: Si tiene entidad financiera
  - `RETENCION`: Si NO tiene entidad financiera

#### `Contratos`
Contratos firmados:
- `id_contrato` (PK)
- `id_adjudicacion` (FK)
- `id_convocatoria` (FK)
- `fecha_firma`, `estado_contrato`

#### `Detalle_Consorcios`
Miembros de consorcios:
- `id_contrato` (FK)
- `ruc_miembro`, `nombre_miembro`
- `porcentaje_participacion`

#### `control_cargas`
Control de archivos procesados:
- `nombre_archivo` (PK)
- `estado`, `fecha_fin`
- `registros_procesados`

---

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- MySQL 5.7+ (incluido en Laragon)
- Conexión a Internet (para descarga de datos)

### Paso 1: Configurar Variables de Entorno

```cmd
cd c:\laragon\www\proyecto_garantias
setup_env.bat
```

El script solicitará:
- Contraseña MySQL
- API Key de Gemini (https://makersuite.google.com/app/apikey)
- Credenciales de email (opcional, para reportes)

### Paso 2: Crear Base de Datos

```cmd
python crear_bd.py
python crear_esquema.py
```

### Paso 3: Verificar Configuración

```cmd
python config\secrets_manager.py
```

Debe mostrar:
```
✅ Todas las configuraciones están correctas
```

---

## 📖 Uso del Sistema

### Ejecución Completa del Pipeline

```cmd
cd 1_motor_etl
python main_auto.py
```

Esto ejecuta automáticamente:
1. **Descarga** de archivos JSON de SEACE
2. **Carga** a base de datos MySQL
3. **Enriquecimiento** con datos bancarios
4. **Procesamiento IA** de consorcios
5. **Envío de reporte** por email

### Ejecución de Módulos Individuales

#### Solo Descarga
```cmd
cd 1_motor_etl
python descargador.py --years 2024 2025
```

#### Solo Carga
```cmd
cd 1_motor_etl
python cargador.py
```

#### Solo Enriquecimiento
```cmd
cd 1_motor_etl
python spider_garantias.py
```

#### Solo Procesamiento IA
```cmd
cd 1_motor_etl
python etl_consorcios_ai.py
```

---

## 📊 Análisis de Datos

### Consultas SQL Útiles

#### Distribución de Tipos de Garantía
```sql
SELECT tipo_garantia, COUNT(*) as total
FROM Licitaciones_Adjudicaciones
GROUP BY tipo_garantia;
```

#### Obras con Retención por Departamento
```sql
SELECT 
    c.departamento, 
    COUNT(*) as total,
    SUM(a.monto_adjudicado) as monto_total
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a 
    ON c.id_convocatoria = a.id_convocatoria
WHERE c.categoria = 'OBRAS'
AND a.tipo_garantia = 'RETENCION'
AND c.estado_proceso = 'CONTRATADO'
GROUP BY c.departamento
ORDER BY monto_total DESC;
```

#### Top 10 Contratos por Monto
```sql
SELECT 
    c.nomenclatura,
    a.ganador_nombre,
    a.monto_adjudicado,
    a.tipo_garantia,
    c.departamento
FROM Licitaciones_Cabecera c
INNER JOIN Licitaciones_Adjudicaciones a 
    ON c.id_convocatoria = a.id_convocatoria
WHERE c.estado_proceso = 'CONTRATADO'
ORDER BY a.monto_adjudicado DESC
LIMIT 10;
```

### Scripts de Análisis Python

```cmd
# Comparar con datos oficiales OECE
python comparar_con_oece.py

# Estadísticas de garantías
python estadisticas_garantias.py

# Análisis de retención
python analizar_retencion.py

# Auditoría de datos NULL
python auditoria_datos_null.py
```

---

## 🔍 Interpretación de Tipos de Garantía

### GARANTIA_BANCARIA
- **Definición**: Carta fianza o póliza emitida por entidad financiera
- **Características**:
  - Requiere banco/aseguradora regulada
  - Costo adicional (1-3% del monto)
  - Típica en contratos de alto monto
- **Identificación**: Campo `entidad_financiera` tiene valor

**Ejemplos de entidades**:
- BBVA, BCP, Interbank
- CESCE Perú, AVLA Perú (aseguradoras)
- FOGAPI

### RETENCION
- **Definición**: Retención del 10% del pago al contratista
- **Características**:
  - NO requiere entidad financiera
  - Facilita acceso a MYPE
  - Reduce costos (sin comisiones)
  - Prorrateada en primera mitad de pagos
- **Identificación**: Campo `entidad_financiera` es NULL o vacío

**Marco Legal**:
- Decreto Legislativo N° 1553 (2023)
- Ley N° 32103 (Año Fiscal 2024)
- Ley N° 32077 (específica para MYPE)

---

## 📈 Estadísticas Actuales

### Distribución General
| Tipo | Cantidad | % | Monto Total |
|------|----------|---|-------------|
| RETENCION | 4,764 | 62.57% | S/ 24.6B |
| GARANTIA_BANCARIA | 2,850 | 37.43% | S/ 16.3B |

### Por Categoría
| Categoría | Retención | Bancaria |
|-----------|-----------|----------|
| BIENES | 59.4% | 40.6% |
| OBRAS | 49.7% | 50.3% |
| SERVICIOS | 65.2% | 34.8% |

### Por Región (Top 5)
| Departamento | Total | Retención | Bancaria |
|--------------|-------|-----------|----------|
| LIMA | 2,891 | 1,277 (44%) | 1,614 (56%) |
| CUSCO | 421 | 287 (68%) | 134 (32%) |
| AREQUIPA | 398 | 245 (62%) | 153 (38%) |
| PIURA | 356 | 234 (66%) | 122 (34%) |
| LA LIBERTAD | 312 | 198 (63%) | 114 (37%) |

---

## 🛠️ Mantenimiento

### Actualización de Datos

Para actualizar con nuevos datos mensuales:

```cmd
cd 1_motor_etl
python descargador.py --years 2025 --force
python cargador.py
```

### Limpieza de Datos

```cmd
# Limpiar control de cargas
python limpiar_control_cargas.py

# Eliminar duplicados
python eliminar_duplicados_2025.py

# Eliminar huérfanos (registros sin JSON)
python eliminar_huerfanos_100.py
```

### Verificación de Integridad

```cmd
# Verificar estado de BD
python verificar_bd.py

# Comparar con OECE oficial
python comparar_con_oece.py

# Auditoría de NULLs
python auditoria_datos_null.py
```

---

## 📚 Documentación Adicional

- [QUICKSTART.md](QUICKSTART.md) - Guía de inicio rápido
- [COMO_EJECUTAR.md](COMO_EJECUTAR.md) - Instrucciones de ejecución
- [SECURITY.md](SECURITY.md) - Guía de seguridad
- [GUIA_TIPOS_GARANTIA.md](GUIA_TIPOS_GARANTIA.md) - Interpretación de garantías
- [ANALISIS_RETENCION.md](ANALISIS_RETENCION.md) - Análisis normativo
- [REPORTE_AUDITORIA_NULL.md](REPORTE_AUDITORIA_NULL.md) - Auditoría de datos
- [RESUMEN_IMPLEMENTACION.md](RESUMEN_IMPLEMENTACION.md) - Historial de cambios

---

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **MySQL 5.7+**: Base de datos
- **Selenium**: Web scraping
- **ijson**: Procesamiento streaming de JSON
- **Google Gemini AI**: Extracción de datos de PDFs
- **Groq API**: Alternativa de IA
- **mysql-connector-python**: Conexión a BD
- **requests**: HTTP requests

### Dependencias Python
```
mysql-connector-python
selenium
webdriver-manager
requests
ijson
google-generativeai
groq
pypdf
```

---

## 🎓 Casos de Uso

### 1. Análisis de Políticas Públicas
- Identificar tendencias en uso de retención vs garantías bancarias
- Evaluar impacto de políticas de inclusión MYPE
- Analizar distribución regional de contratos

### 2. Investigación Académica
- Estudios sobre contratación pública
- Análisis de acceso a mercados públicos
- Evaluación de costos de transacción

### 3. Transparencia y Auditoría
- Verificación de cumplimiento normativo
- Detección de patrones inusuales
- Monitoreo de contratos públicos

### 4. Análisis Financiero
- Evaluación de mercado de garantías
- Identificación de oportunidades para entidades financieras
- Análisis de riesgo crediticio

---

## ⚠️ Limitaciones Conocidas

1. **Tabla Detalle_Consorcios vacía**: Requiere ejecución manual del ETL de IA
2. **Algunos ganador_ruc NULL**: Limitación de datos fuente (3.90%)
3. **Monto estimado NULL**: Normal en SEACE (15.14%)
4. **Procesamiento IA lento**: Depende de APIs externas (Gemini/Groq)

---

## 🔄 Historial de Versiones

### Versión Actual: 2.0 (Diciembre 2024)

**Mejoras implementadas**:
- ✅ Migración a variables de entorno (seguridad)
- ✅ 100% coincidencia con datos OECE oficiales
- ✅ Tabla Contratos implementada (relación 1:N)
- ✅ Campo tipo_garantia como columna generada
- ✅ Limpieza de registros huérfanos
- ✅ Estados originales del SEACE (sin traducciones)
- ✅ Documentación completa

**Calificación del proyecto**: 8.0/10

---

## 🤝 Contribuciones

Este es un proyecto de análisis de datos públicos. Para contribuir:

1. Reportar bugs o inconsistencias
2. Sugerir mejoras en análisis
3. Proponer nuevas métricas o visualizaciones
4. Mejorar documentación

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisar documentación en carpeta raíz
2. Ejecutar scripts de diagnóstico
3. Verificar logs en `1_motor_etl/bot_execution.log`

---

## 📄 Licencia

Proyecto de análisis de datos públicos del Estado Peruano.
Datos fuente: SEACE (https://www.seace.gob.pe/)
Estándar: OCDS (https://standard.open-contracting.org/)

---

## 🎯 Próximos Pasos

### Corto Plazo
- [ ] Ejecutar ETL de consorcios para poblar tabla
- [ ] Implementar dashboard de visualización
- [ ] Automatizar ejecución mensual

### Mediano Plazo
- [ ] Testing automatizado (pytest)
- [ ] CI/CD con GitHub Actions
- [ ] API REST para consultas

### Largo Plazo
- [ ] Machine Learning para predicción de garantías
- [ ] Análisis de redes de contratistas
- [ ] Integración con otros sistemas del Estado

---

**Última actualización**: 18 de diciembre de 2024
**Autor**: Sistema automatizado de análisis SEACE
**Versión**: 2.0
