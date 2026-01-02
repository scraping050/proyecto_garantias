import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='garantias_seace'
    )
    
    cursor = conn.cursor()
    
    print("=" * 60)
    print("DIAGNÓSTICO COMPLETO - CONSORCIOS")
    print("=" * 60)
    
    # 1. Total de adjudicaciones
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    total_adj = cursor.fetchone()[0]
    print(f"\n1. Total de adjudicaciones: {total_adj:,}")
    
    # 2. Adjudicaciones con CONSORCIO en el nombre
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE ganador_nombre LIKE '%CONSORCIO%'
    """)
    total_consorcios = cursor.fetchone()[0]
    print(f"2. Adjudicaciones con 'CONSORCIO' en el nombre: {total_consorcios:,}")
    
    # 3. Consorcios con id_contrato válido
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE ganador_nombre LIKE '%CONSORCIO%'
          AND id_contrato IS NOT NULL 
          AND id_contrato != ''
    """)
    consorcios_con_id = cursor.fetchone()[0]
    print(f"3. Consorcios con id_contrato válido: {consorcios_con_id:,}")
    
    # 4. Consorcios pendientes (sin detalle)
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones a
        LEFT JOIN Detalle_Consorcios d ON a.id_contrato = d.id_contrato
        WHERE a.ganador_nombre LIKE '%CONSORCIO%' 
          AND d.id_contrato IS NULL
          AND a.id_contrato IS NOT NULL 
          AND a.id_contrato != ''
    """)
    pendientes = cursor.fetchone()[0]
    print(f"4. Consorcios PENDIENTES de procesar: {pendientes:,}")
    
    # 5. Mostrar algunos ejemplos
    print(f"\n{'=' * 60}")
    print("EJEMPLOS DE CONSORCIOS PENDIENTES (Primeros 5):")
    print("=" * 60)
    cursor.execute("""
        SELECT a.id_contrato, a.ganador_nombre, a.id_adjudicacion
        FROM Licitaciones_Adjudicaciones a
        LEFT JOIN Detalle_Consorcios d ON a.id_contrato = d.id_contrato
        WHERE a.ganador_nombre LIKE '%CONSORCIO%' 
          AND d.id_contrato IS NULL
          AND a.id_contrato IS NOT NULL 
          AND a.id_contrato != ''
        LIMIT 5
    """)
    
    for row in cursor.fetchall():
        print(f"\nID Contrato: {row[0]}")
        print(f"Ganador: {row[1][:80]}")
        print(f"ID Adjudicación: {row[2]}")
    
    # 6. Verificar si hay consorcios procesados
    cursor.execute("SELECT COUNT(*) FROM Detalle_Consorcios")
    procesados = cursor.fetchone()[0]
    print(f"\n{'=' * 60}")
    print(f"CONSORCIOS YA PROCESADOS: {procesados:,}")
    print("=" * 60)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
