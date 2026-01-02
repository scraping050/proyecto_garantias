# Script para analizar las columnas de estado en ambas tablas
import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='garantias_seace'
    )
    
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ANALISIS DE COLUMNAS DE ESTADO - LICITACIONES")
    print("=" * 80)
    
    # Analizar estado_proceso en Licitaciones_Cabecera
    print("\n1. TABLA: Licitaciones_Cabecera - Columna: estado_proceso")
    print("-" * 80)
    
    sql = """
        SELECT estado_proceso, COUNT(*) as cantidad, 
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Licitaciones_Cabecera), 2) as porcentaje
        FROM Licitaciones_Cabecera
        WHERE estado_proceso IS NOT NULL
        GROUP BY estado_proceso
        ORDER BY cantidad DESC
    """
    cursor.execute(sql)
    
    print(f"\n{'Estado Proceso':<30} {'Cantidad':>10} {'Porcentaje':>12}")
    print("-" * 80)
    total_cabecera = 0
    for row in cursor.fetchall():
        print(f"{row[0]:<30} {row[1]:>10,} {row[2]:>11.2f}%")
        total_cabecera += row[1]
    print(f"{'TOTAL':<30} {total_cabecera:>10,}")
    
    # Analizar estado_item en Licitaciones_Adjudicaciones
    print("\n\n2. TABLA: Licitaciones_Adjudicaciones - Columna: estado_item")
    print("-" * 80)
    
    sql = """
        SELECT estado_item, COUNT(*) as cantidad,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Licitaciones_Adjudicaciones), 2) as porcentaje
        FROM Licitaciones_Adjudicaciones
        WHERE estado_item IS NOT NULL
        GROUP BY estado_item
        ORDER BY cantidad DESC
    """
    cursor.execute(sql)
    
    print(f"\n{'Estado Item':<30} {'Cantidad':>10} {'Porcentaje':>12}")
    print("-" * 80)
    total_adj = 0
    for row in cursor.fetchall():
        print(f"{row[0]:<30} {row[1]:>10,} {row[2]:>11.2f}%")
        total_adj += row[1]
    print(f"{'TOTAL':<30} {total_adj:>10,}")
    
    # Analizar relación entre ambas tablas
    print("\n\n3. RELACION ENTRE ESTADO_PROCESO Y ESTADO_ITEM")
    print("-" * 80)
    
    sql = """
        SELECT 
            c.estado_proceso,
            a.estado_item,
            COUNT(*) as cantidad
        FROM Licitaciones_Cabecera c
        INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
        GROUP BY c.estado_proceso, a.estado_item
        ORDER BY cantidad DESC
        LIMIT 20
    """
    cursor.execute(sql)
    
    print(f"\n{'Estado Proceso (Cabecera)':<30} {'Estado Item (Adjud.)':<30} {'Cantidad':>10}")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"{row[0]:<30} {row[1]:<30} {row[2]:>10,}")
    
    # Verificar licitaciones con múltiples adjudicaciones
    print("\n\n4. LICITACIONES CON MULTIPLES ADJUDICACIONES")
    print("-" * 80)
    
    sql = """
        SELECT 
            COUNT(DISTINCT id_convocatoria) as licitaciones_con_adj,
            SUM(num_adj) as total_adjudicaciones,
            ROUND(AVG(num_adj), 2) as promedio_adj_por_licitacion
        FROM (
            SELECT id_convocatoria, COUNT(*) as num_adj
            FROM Licitaciones_Adjudicaciones
            GROUP BY id_convocatoria
        ) as subq
    """
    cursor.execute(sql)
    row = cursor.fetchone()
    
    print(f"\nLicitaciones con adjudicaciones: {row[0]:,}")
    print(f"Total de adjudicaciones: {row[1]:,}")
    print(f"Promedio de adjudicaciones por licitación: {row[2]}")
    
    # Ejemplos de licitaciones con múltiples adjudicaciones
    print("\n\n5. EJEMPLOS DE LICITACIONES CON MULTIPLES ADJUDICACIONES")
    print("-" * 80)
    
    sql = """
        SELECT 
            c.id_convocatoria,
            c.nomenclatura,
            c.estado_proceso,
            COUNT(a.id_adjudicacion) as num_adjudicaciones,
            GROUP_CONCAT(DISTINCT a.estado_item) as estados_items
        FROM Licitaciones_Cabecera c
        INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
        GROUP BY c.id_convocatoria, c.nomenclatura, c.estado_proceso
        HAVING num_adjudicaciones > 1
        ORDER BY num_adjudicaciones DESC
        LIMIT 5
    """
    cursor.execute(sql)
    
    print(f"\n{'ID Convocatoria':<20} {'# Adj':>6} {'Estado Proceso':<20} {'Estados Items':<30}")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"{row[0]:<20} {row[3]:>6} {row[2]:<20} {row[4]:<30}")
    
    # Verificar casos donde estado_proceso != "Adjudicado" pero tiene adjudicaciones
    print("\n\n6. CASOS ESPECIALES: Licitaciones NO 'Adjudicado' con adjudicaciones")
    print("-" * 80)
    
    sql = """
        SELECT 
            c.estado_proceso,
            COUNT(DISTINCT c.id_convocatoria) as num_licitaciones,
            COUNT(a.id_adjudicacion) as num_adjudicaciones
        FROM Licitaciones_Cabecera c
        INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
        WHERE c.estado_proceso != 'Adjudicado'
        GROUP BY c.estado_proceso
        ORDER BY num_adjudicaciones DESC
    """
    cursor.execute(sql)
    
    print(f"\n{'Estado Proceso':<30} {'# Licitaciones':>15} {'# Adjudicaciones':>18}")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"{row[0]:<30} {row[1]:>15,} {row[2]:>18,}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("ANALISIS COMPLETADO")
    print("=" * 80)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
