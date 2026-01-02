# Script para crear el esquema completo de la base de datos garantias_seace
import mysql.connector

SQL_SCHEMA = """
-- Tabla principal de licitaciones
CREATE TABLE IF NOT EXISTS Licitaciones_Cabecera (
    id_convocatoria VARCHAR(100) PRIMARY KEY,
    ocid VARCHAR(100) UNIQUE,
    nomenclatura VARCHAR(4000),
    descripcion TEXT,
    comprador VARCHAR(500),
    categoria VARCHAR(50),
    tipo_procedimiento VARCHAR(100),
    monto_estimado DECIMAL(15,2),
    moneda VARCHAR(10) DEFAULT 'PEN',
    fecha_publicacion DATE,
    estado_proceso VARCHAR(50),
    ubicacion_completa VARCHAR(500),
    departamento VARCHAR(100),
    provincia VARCHAR(100),
    distrito VARCHAR(100),
    archivo_origen VARCHAR(100),
    fecha_carga DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_update DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_fecha (fecha_publicacion),
    INDEX idx_comprador (comprador(255)),
    INDEX idx_estado (estado_proceso),
    INDEX idx_categoria (categoria),
    INDEX idx_departamento (departamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de adjudicaciones
CREATE TABLE IF NOT EXISTS Licitaciones_Adjudicaciones (
    id_adjudicacion VARCHAR(100) PRIMARY KEY,
    id_contrato VARCHAR(100),
    id_convocatoria VARCHAR(100) NOT NULL,
    ganador_nombre VARCHAR(500),
    ganador_ruc VARCHAR(50),
    monto_adjudicado DECIMAL(15,2),
    fecha_adjudicacion DATE,
    estado_item VARCHAR(50),
    entidad_financiera VARCHAR(255),
    tipo_garantia VARCHAR(50) GENERATED ALWAYS AS (
        CASE 
            WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' 
            THEN 'GARANTIA_BANCARIA'
            ELSE 'RETENCION'
        END
    ) STORED,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_convocatoria) REFERENCES Licitaciones_Cabecera(id_convocatoria)
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_convocatoria (id_convocatoria),
    INDEX idx_ruc (ganador_ruc),
    INDEX idx_fecha_adj (fecha_adjudicacion),
    INDEX idx_tipo_garantia (tipo_garantia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de contratos
CREATE TABLE IF NOT EXISTS Contratos (
    id_contrato VARCHAR(100) PRIMARY KEY,
    id_adjudicacion VARCHAR(100) NOT NULL,
    id_convocatoria VARCHAR(100) NOT NULL,
    fecha_firma DATE,
    estado_contrato VARCHAR(50),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_adjudicacion) REFERENCES Licitaciones_Adjudicaciones(id_adjudicacion)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_convocatoria) REFERENCES Licitaciones_Cabecera(id_convocatoria)
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_adjudicacion (id_adjudicacion),
    INDEX idx_convocatoria (id_convocatoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de consorcios
CREATE TABLE IF NOT EXISTS Detalle_Consorcios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_contrato VARCHAR(100),
    ruc_miembro VARCHAR(20),
    nombre_miembro VARCHAR(500),
    porcentaje_participacion DECIMAL(5,2),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_consorcio (id_contrato, ruc_miembro),
    INDEX idx_contrato (id_contrato),
    INDEX idx_ruc (ruc_miembro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de control de cargas
CREATE TABLE IF NOT EXISTS control_cargas (
    nombre_archivo VARCHAR(255) PRIMARY KEY,
    estado VARCHAR(50),
    fecha_fin DATETIME,
    registros_procesados INT DEFAULT 0,
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

try:
    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='garantias_seace'
    )
    
    cursor = conn.cursor()
    
    # Ejecutar cada sentencia CREATE TABLE
    for statement in SQL_SCHEMA.split(';'):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)
            print(f"OK - Ejecutado: {statement[:50]}...")
    
    conn.commit()
    print("\nOK - Esquema de base de datos creado exitosamente")
    
    # Verificar tablas creadas
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\nTablas creadas ({len(tables)}):")
    for table in tables:
        print(f"  - {table[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
