# Script para investigar registros huérfanos (adjudicaciones sin cabecera)
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
    print("INVESTIGACION: ADJUDICACIONES SIN CABECERA")
    print("=" * 80)
    
    # 1. Contar registros en cada tabla
    print("\n1. RESUMEN DE REGISTROS")
    print("-" * 80)
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
    count_cab = cursor.fetchone()[0]
    print(f"Licitaciones_Cabecera: {count_cab:,}")
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    count_adj = cursor.fetchone()[0]
    print(f"Licitaciones_Adjudicaciones: {count_adj:,}")
    
    cursor.execute("SELECT COUNT(DISTINCT id_convocatoria) FROM Licitaciones_Adjudicaciones")
    count_conv_adj = cursor.fetchone()[0]
    print(f"Convocatorias únicas en Adjudicaciones: {count_conv_adj:,}")
    
    # 2. Buscar adjudicaciones sin cabecera (registros huérfanos)
    print("\n2. ADJUDICACIONES SIN CABECERA (HUERFANOS)")
    print("-" * 80)
    
    sql = """
        SELECT a.id_convocatoria, COUNT(*) as num_adjudicaciones
        FROM Licitaciones_Adjudicaciones a
        LEFT JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
        WHERE c.id_convocatoria IS NULL
        GROUP BY a.id_convocatoria
        ORDER BY num_adjudicaciones DESC
        LIMIT 20
    """
    cursor.execute(sql)
    
    huerfanos = cursor.fetchall()
    
    if huerfanos:
        print(f"\n[!] PROBLEMA ENCONTRADO: {len(huerfanos)} convocatorias tienen adjudicaciones pero NO cabecera")
        print(f"\n{'ID Convocatoria':<20} {'# Adjudicaciones':>18}")
        print("-" * 80)
        
        total_huerfanos = 0
        for row in huerfanos:
            print(f"{row[0]:<20} {row[1]:>18,}")
            total_huerfanos += row[1]
        
        print("-" * 80)
        print(f"Total adjudicaciones huérfanas: {total_huerfanos:,}")
        
        # Mostrar ejemplo de adjudicación huérfana
        print(f"\n3. EJEMPLO DE ADJUDICACION HUERFANA")
        print("-" * 80)
        
        id_huerfano = huerfanos[0][0]
        sql = """
            SELECT id_adjudicacion, id_contrato, ganador_nombre, monto_adjudicado, fecha_adjudicacion
            FROM Licitaciones_Adjudicaciones
            WHERE id_convocatoria = %s
            LIMIT 1
        """
        cursor.execute(sql, (id_huerfano,))
        adj = cursor.fetchone()
        
        print(f"\nID Convocatoria: {id_huerfano}")
        print(f"ID Adjudicación: {adj[0]}")
        print(f"ID Contrato: {adj[1]}")
        print(f"Ganador: {adj[2][:60]}...")
        print(f"Monto: S/ {adj[3]:,.2f}" if adj[3] else "Monto: N/A")
        print(f"Fecha: {adj[4]}")
        
        # Investigar causa
        print(f"\n4. POSIBLES CAUSAS")
        print("-" * 80)
        print("""
CAUSA 1: Error en la clave primaria
- La adjudicación tiene un id_convocatoria que no existe en Cabecera
- Puede ser un error en el JSON del SEACE

CAUSA 2: Filtro en el procesamiento
- El código puede estar filtrando algunas licitaciones en Cabecera
- Pero procesando todas las adjudicaciones

CAUSA 3: Datos incompletos en JSON
- El JSON puede tener awards[] pero no tender{}
- O tender{} puede estar vacío/inválido

CAUSA 4: Error en ON DUPLICATE KEY UPDATE
- Puede estar eliminando cabeceras pero manteniendo adjudicaciones
        """)
        
    else:
        print("\n[OK] No se encontraron adjudicaciones huérfanas")
        print("Todas las adjudicaciones tienen su cabecera correspondiente")
    
    # 5. Verificar integridad referencial
    print(f"\n5. VERIFICACION DE INTEGRIDAD")
    print("-" * 80)
    
    sql = """
        SELECT 
            COUNT(*) as total_adjudicaciones,
            COUNT(DISTINCT a.id_convocatoria) as convocatorias_con_adj,
            (SELECT COUNT(*) FROM Licitaciones_Cabecera) as total_cabeceras,
            (SELECT COUNT(DISTINCT id_convocatoria) FROM Licitaciones_Adjudicaciones a
             LEFT JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
             WHERE c.id_convocatoria IS NULL) as convocatorias_huerfanas
        FROM Licitaciones_Adjudicaciones a
    """
    cursor.execute(sql)
    row = cursor.fetchone()
    
    print(f"Total adjudicaciones: {row[0]:,}")
    print(f"Convocatorias con adjudicaciones: {row[1]:,}")
    print(f"Total cabeceras: {row[2]:,}")
    print(f"Convocatorias huérfanas: {row[3]:,}")
    
    if row[3] > 0:
        porcentaje = (row[3] * 100.0) / row[1]
        print(f"\n[!] PROBLEMA: {porcentaje:.2f}% de convocatorias con adjudicaciones NO tienen cabecera")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("INVESTIGACION COMPLETADA")
    print("=" * 80)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
