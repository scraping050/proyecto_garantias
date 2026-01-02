"""
Script para implementar clasificación de tipo de garantía en la base de datos
Fecha: 2025-12-18
"""
import mysql.connector
import sys

# Conexión a la base de datos
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='garantias_seace'
    )
    
    cursor = conn.cursor()
    
    print("=" * 80)
    print("IMPLEMENTACIÓN: Clasificación de Tipo de Garantía")
    print("=" * 80)
    
    # 1. Verificar si la columna ya existe
    print("\n1. Verificando si la columna ya existe...")
    cursor.execute("DESCRIBE Licitaciones_Adjudicaciones")
    columns = [row[0] for row in cursor.fetchall()]
    
    if 'tipo_garantia' in columns:
        print("ADVERTENCIA: La columna 'tipo_garantia' ya existe. Eliminandola primero...")
        cursor.execute("ALTER TABLE Licitaciones_Adjudicaciones DROP COLUMN tipo_garantia")
        conn.commit()
        print("OK - Columna anterior eliminada")
    
    # 2. Agregar columna calculada
    print("\n2. Agregando columna calculada 'tipo_garantia'...")
    cursor.execute("""
        ALTER TABLE Licitaciones_Adjudicaciones 
        ADD COLUMN tipo_garantia VARCHAR(50) 
        GENERATED ALWAYS AS (
            CASE 
                WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' 
                THEN 'GARANTIA_BANCARIA'
                ELSE 'RETENCION'
            END
        ) STORED
    """)
    conn.commit()
    print("OK - Columna 'tipo_garantia' agregada exitosamente")
    
    # 3. Crear índice
    print("\n3. Creando índice para optimizar consultas...")
    try:
        cursor.execute("CREATE INDEX idx_tipo_garantia ON Licitaciones_Adjudicaciones(tipo_garantia)")
        conn.commit()
        print("OK - Indice 'idx_tipo_garantia' creado exitosamente")
    except mysql.connector.Error as e:
        if "Duplicate key name" in str(e):
            print("ADVERTENCIA: El indice ya existe, continuando...")
        else:
            raise
    
    # 4. Verificar estructura
    print("\n4. Verificando estructura de la tabla...")
    cursor.execute("DESCRIBE Licitaciones_Adjudicaciones")
    print("\nColumnas de Licitaciones_Adjudicaciones:")
    for row in cursor.fetchall():
        if row[0] in ['entidad_financiera', 'tipo_garantia']:
            print(f"  - {row[0]:25} | {row[1]:20} | {row[5] if row[5] else ''}")
    
    # 5. Verificar distribución
    print("\n5. Verificando distribución de tipos de garantía...")
    cursor.execute("""
        SELECT 
            tipo_garantia, 
            COUNT(*) as total,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Licitaciones_Adjudicaciones), 2) as porcentaje
        FROM Licitaciones_Adjudicaciones
        GROUP BY tipo_garantia
    """)
    
    print("\nDistribución de Tipos de Garantía:")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"  {row[0]:25} | Total: {row[1]:6} | Porcentaje: {row[2]:6.2f}%")
    
    # 6. Ejemplos
    print("\n6. Ejemplos de clasificación...")
    cursor.execute("""
        SELECT 
            id_adjudicacion,
            ganador_nombre,
            entidad_financiera,
            tipo_garantia
        FROM Licitaciones_Adjudicaciones
        LIMIT 5
    """)
    
    print("\nEjemplos:")
    print("-" * 80)
    for row in cursor.fetchall():
        entidad = row[2] if row[2] else "SIN ENTIDAD"
        print(f"  ID: {row[0]:15} | Tipo: {row[3]:20} | Entidad: {entidad[:30]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("OK - IMPLEMENTACION COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    
except mysql.connector.Error as e:
    print(f"\nERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\nERROR INESPERADO: {e}")
    sys.exit(1)
