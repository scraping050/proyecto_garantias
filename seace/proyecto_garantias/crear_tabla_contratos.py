"""
Script para crear la tabla Contratos en la base de datos
"""
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456789',
    database='garantias_seace'
)

cursor = conn.cursor()

print("=" * 100)
print("CREANDO TABLA CONTRATOS")
print("=" * 100)

# Crear tabla Contratos
sql_create = """
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
"""

try:
    cursor.execute(sql_create)
    conn.commit()
    print("\nOK - Tabla Contratos creada exitosamente")
    
    # Verificar estructura
    cursor.execute("DESCRIBE Contratos")
    print("\nEstructura de la tabla Contratos:")
    print("-" * 100)
    for row in cursor.fetchall():
        print(f"  {row[0]:25} | {row[1]:20} | {row[2]:5} | {row[3]:5}")
    
    # Verificar tablas
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"\nTablas en la base de datos: {len(tables)}")
    for table in tables:
        print(f"  - {table}")
    
except mysql.connector.Error as e:
    print(f"\nERROR: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()

print("\n" + "=" * 100)
print("PROCESO COMPLETADO")
print("=" * 100)
