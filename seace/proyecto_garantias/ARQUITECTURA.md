# 🏗️ Arquitectura del Sistema - Proyecto Garantías SEACE

## 📐 Diagrama de Arquitectura General

```mermaid
graph TB
    subgraph "Fuente de Datos"
        SEACE[SEACE API<br/>datos.gob.pe]
        OECE[OECE Oficial<br/>10,043 licitaciones]
    end
    
    subgraph "1. ETL Pipeline"
        DESC[Descargador<br/>descargador.py]
        CARG[Cargador<br/>cargador.py]
        SPID[Spider Garantías<br/>spider_garantias.py]
        CONS[ETL Consorcios IA<br/>etl_consorcios_ai.py]
        MAIN[Orquestador<br/>main_auto.py]
    end
    
    subgraph "2. Almacenamiento"
        JSON[Archivos JSON<br/>24 meses<br/>1_database/]
        DB[(MySQL Database<br/>garantias_seace)]
    end
    
    subgraph "3. Tablas BD"
        LICIT[Licitaciones_Cabecera<br/>10,043 registros]
        ADJUD[Licitaciones_Adjudicaciones<br/>7,959 registros]
        CONTR[Contratos<br/>6,687 registros]
        DETCO[Detalle_Consorcios<br/>0 registros]
    end
    
    subgraph "4. Análisis"
        COMP[Comparador OECE<br/>comparar_con_oece.py]
        ESTAT[Estadísticas<br/>estadisticas_garantias.py]
        AUDIT[Auditoría<br/>auditoria_datos_null.py]
        RESUMEN[Resumen Ejecutivo<br/>resumen_ejecutivo.py]
    end
    
    subgraph "5. Configuración"
        ENV[Variables Entorno<br/>GARANTIAS_*]
        SEC[Secrets Manager<br/>config/secrets_manager.py]
    end
    
    SEACE -->|Descarga JSON| DESC
    DESC -->|Guarda| JSON
    JSON -->|Lee| CARG
    CARG -->|Inserta| DB
    DB --> LICIT
    DB --> ADJUD
    DB --> CONTR
    DB --> DETCO
    
    LICIT -->|FK| ADJUD
    ADJUD -->|FK| CONTR
    CONTR -->|FK| DETCO
    
    SPID -->|Enriquece| ADJUD
    CONS -->|Procesa PDFs| DETCO
    
    MAIN -->|Orquesta| DESC
    MAIN -->|Orquesta| CARG
    MAIN -->|Orquesta| SPID
    MAIN -->|Orquesta| CONS
    
    DB -->|Consulta| COMP
    DB -->|Consulta| ESTAT
    DB -->|Consulta| AUDIT
    DB -->|Consulta| RESUMEN
    
    OECE -.->|Valida| COMP
    
    ENV -->|Provee| SEC
    SEC -->|Configura| MAIN
    SEC -->|Configura| CARG
    SEC -->|Configura| SPID
    SEC -->|Configura| CONS
    
    style SEACE fill:#e1f5ff
    style OECE fill:#e1f5ff
    style DB fill:#fff4e1
    style LICIT fill:#e8f5e9
    style ADJUD fill:#e8f5e9
    style CONTR fill:#e8f5e9
    style DETCO fill:#ffebee
    style MAIN fill:#f3e5f5
```

## 🔄 Flujo de Datos Detallado

```mermaid
sequenceDiagram
    participant U as Usuario
    participant M as main_auto.py
    participant D as descargador.py
    participant C as cargador.py
    participant S as spider_garantias.py
    participant I as etl_consorcios_ai.py
    participant DB as MySQL
    participant E as Email
    
    U->>M: Ejecutar Pipeline
    
    Note over M: Etapa 1: Descarga
    M->>D: Iniciar descarga
    D->>D: Scraping SEACE
    D->>D: Descargar JSONs
    D->>D: Validar SHA256
    D-->>M: Completado (24 archivos)
    
    Note over M: Etapa 2: Carga
    M->>C: Iniciar carga
    C->>C: Leer JSONs (ijson streaming)
    C->>C: Filtrar Licitación Pública
    C->>DB: INSERT/UPDATE Cabecera
    C->>DB: INSERT/UPDATE Adjudicaciones
    C->>DB: INSERT/UPDATE Contratos
    C->>DB: Limpiar huérfanos
    C-->>M: Completado (10,043 licitaciones)
    
    Note over M: Etapa 3: Enriquecimiento
    M->>S: Iniciar spider
    S->>DB: SELECT pendientes
    S->>S: Scraping SEACE (garantías)
    S->>DB: UPDATE entidad_financiera
    S-->>M: Completado
    
    Note over M: Etapa 4: IA
    M->>I: Iniciar procesamiento IA
    I->>DB: SELECT contratos con PDF
    I->>I: Descargar PDFs
    I->>I: Gemini AI (extracción)
    I->>DB: INSERT Detalle_Consorcios
    I-->>M: Completado
    
    Note over M: Reporte Final
    M->>E: Enviar reporte HTML
    M-->>U: Pipeline completado
```

## 🗄️ Modelo de Datos

```mermaid
erDiagram
    Licitaciones_Cabecera ||--o{ Licitaciones_Adjudicaciones : "tiene"
    Licitaciones_Adjudicaciones ||--o{ Contratos : "genera"
    Contratos ||--o{ Detalle_Consorcios : "incluye"
    
    Licitaciones_Cabecera {
        varchar id_convocatoria PK
        varchar ocid UK
        text nomenclatura
        text descripcion
        varchar comprador
        varchar categoria
        varchar tipo_procedimiento
        decimal monto_estimado
        date fecha_publicacion
        varchar estado_proceso
        varchar departamento
        varchar provincia
        varchar distrito
    }
    
    Licitaciones_Adjudicaciones {
        varchar id_adjudicacion PK
        varchar id_convocatoria FK
        varchar id_contrato
        varchar ganador_nombre
        varchar ganador_ruc
        decimal monto_adjudicado
        date fecha_adjudicacion
        varchar estado_item
        varchar entidad_financiera
        varchar tipo_garantia "GENERATED"
    }
    
    Contratos {
        varchar id_contrato PK
        varchar id_adjudicacion FK
        varchar id_convocatoria FK
        date fecha_firma
        varchar estado_contrato
    }
    
    Detalle_Consorcios {
        int id PK
        varchar id_contrato FK
        varchar ruc_miembro
        varchar nombre_miembro
        decimal porcentaje_participacion
    }
```

## 🎯 Clasificación de Tipos de Garantía

```mermaid
flowchart TD
    START[Adjudicación]
    CHECK{entidad_financiera<br/>tiene valor?}
    BANCARIA[GARANTIA_BANCARIA<br/>35.81%<br/>2,850 casos]
    RETENCION[RETENCION<br/>64.19%<br/>5,109 casos]
    
    START --> CHECK
    CHECK -->|Sí| BANCARIA
    CHECK -->|No/NULL| RETENCION
    
    BANCARIA --> EJEMPLOS1[Ejemplos:<br/>BBVA, BCP, Interbank<br/>CESCE, AVLA]
    RETENCION --> EJEMPLOS2[Características:<br/>10% del monto<br/>Sin costo bancario<br/>Facilita MYPE]
    
    style BANCARIA fill:#e3f2fd
    style RETENCION fill:#f1f8e9
    style START fill:#fff3e0
```

## 📊 Distribución de Datos

```mermaid
pie title Distribución por Tipo de Garantía
    "RETENCION (64.19%)" : 5109
    "GARANTIA_BANCARIA (35.81%)" : 2850
```

```mermaid
pie title Distribución por Categoría
    "BIENES (65.84%)" : 5239
    "OBRAS (35.86%)" : 2854
```

```mermaid
pie title Estados de Proceso (Top 5)
    "CONTRATADO (48.9%)" : 4910
    "CONVOCADO (17.9%)" : 1798
    "NULO (12.0%)" : 1204
    "DESIERTO (7.8%)" : 788
    "CONSENTIDO (6.7%)" : 670
    "OTROS (6.7%)" : 673
```

## 🔐 Arquitectura de Seguridad

```mermaid
graph LR
    subgraph "Sistema Operativo"
        ENVVARS[Variables de Entorno<br/>GARANTIAS_DB_USER<br/>GARANTIAS_DB_PASS<br/>GARANTIAS_GEMINI_API_KEY<br/>etc.]
    end
    
    subgraph "Aplicación"
        SEC[secrets_manager.py<br/>Validación y acceso]
        MOD1[descargador.py]
        MOD2[cargador.py]
        MOD3[spider_garantias.py]
        MOD4[etl_consorcios_ai.py]
    end
    
    subgraph "Servicios Externos"
        DB[(MySQL)]
        GEMINI[Gemini AI]
        EMAIL[Gmail SMTP]
    end
    
    ENVVARS -->|Lee| SEC
    SEC -->|Provee config| MOD1
    SEC -->|Provee config| MOD2
    SEC -->|Provee config| MOD3
    SEC -->|Provee config| MOD4
    
    MOD2 -->|Conecta| DB
    MOD3 -->|Conecta| DB
    MOD4 -->|Conecta| DB
    MOD4 -->|API Call| GEMINI
    MOD1 -->|Envía reporte| EMAIL
    
    style ENVVARS fill:#c8e6c9
    style SEC fill:#fff9c4
    style DB fill:#ffccbc
    style GEMINI fill:#e1bee7
    style EMAIL fill:#b3e5fc
```

## 📈 Métricas del Sistema

### Estado Actual (18 Dic 2024)

| Métrica | Valor | Estado |
|---------|-------|--------|
| **Licitaciones** | 10,043 | ✅ 100% coincidencia OECE |
| **Adjudicaciones** | 7,959 | ✅ Completo |
| **Contratos** | 6,687 | ✅ Mapeados |
| **Consorcios** | 0 | ⚠️ Pendiente ETL |
| **Archivos JSON** | 24 meses | ✅ 2024-2025 |
| **Calidad RUC** | 96.26% | ✅ Alta |
| **Calidad Contratos** | 76.76% | ⚠️ Mejorable |
| **Calidad Monto** | 85.37% | ✅ Buena |

### Rendimiento ETL

| Etapa | Tiempo Promedio | Estado |
|-------|----------------|--------|
| Descarga | ~14 segundos | ✅ Rápido |
| Carga | ~0.5 segundos | ✅ Muy rápido |
| Enriquecimiento | ~1 segundo | ✅ Rápido |
| IA Consorcios | Variable | ⚠️ Depende de API |

## 🛠️ Stack Tecnológico

```mermaid
graph TB
    subgraph "Frontend/Interfaz"
        CLI[Command Line Interface]
        SCRIPTS[Scripts Python]
    end
    
    subgraph "Backend/Lógica"
        PYTHON[Python 3.8+]
        SELENIUM[Selenium WebDriver]
        IJSON[ijson Streaming]
        MYSQL_CONN[mysql-connector-python]
    end
    
    subgraph "Datos"
        MYSQL[(MySQL 5.7+)]
        JSON_FILES[Archivos JSON<br/>OCDS Format]
        PDF_FILES[PDFs Consorcios]
    end
    
    subgraph "Servicios Externos"
        SEACE_API[SEACE API]
        GEMINI_API[Google Gemini AI]
        GROQ_API[Groq API]
        SMTP[Gmail SMTP]
    end
    
    CLI --> SCRIPTS
    SCRIPTS --> PYTHON
    PYTHON --> SELENIUM
    PYTHON --> IJSON
    PYTHON --> MYSQL_CONN
    
    SELENIUM --> SEACE_API
    IJSON --> JSON_FILES
    MYSQL_CONN --> MYSQL
    
    PYTHON --> GEMINI_API
    PYTHON --> GROQ_API
    PYTHON --> SMTP
    
    SEACE_API --> JSON_FILES
    SEACE_API --> PDF_FILES
    
    style PYTHON fill:#4caf50
    style MYSQL fill:#ff9800
    style SEACE_API fill:#2196f3
    style GEMINI_API fill:#9c27b0
```

## 📚 Documentación del Proyecto

```
proyecto_garantias/
├── README.md                          ⭐ Este documento
├── ARQUITECTURA.md                    ⭐ Arquitectura detallada
├── QUICKSTART.md                      🚀 Inicio rápido
├── COMO_EJECUTAR.md                   📖 Guía de ejecución
├── SECURITY.md                        🔒 Seguridad
├── GUIA_TIPOS_GARANTIA.md            💰 Interpretación de garantías
├── ANALISIS_RETENCION.md             📊 Análisis normativo
├── REPORTE_AUDITORIA_NULL.md         🔍 Auditoría de calidad
├── RESUMEN_IMPLEMENTACION.md         📝 Historial de cambios
└── ... (15+ documentos adicionales)
```

---

**Última actualización**: 18 de diciembre de 2024  
**Versión**: 2.0  
**Estado**: ✅ Producción
