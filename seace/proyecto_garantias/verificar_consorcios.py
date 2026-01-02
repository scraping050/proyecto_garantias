# Script para verificar consorcios en la base de datos
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
    print("VERIFICANDO CONSORCIOS EN LA BASE DE DATOS")
    print("=" * 60)
    
    # Buscar adjudicaciones con "CONSORCIO" en el nombre
    sql = """
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE ganador_nombre LIKE '%CONSORCIO%'
    """
    cursor.execute(sql)
    count_consorcios = cursor.fetchone()[0]
    print(f"\nAdjudicaciones con 'CONSORCIO' en el nombre: {count_consorcios:,}")
    
    # Verificar cuántos tienen id_contrato
    sql = """
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE ganador_nombre LIKE '%CONSORCIO%'
        AND id_contrato IS NOT NULL 
        AND id_contrato != ''
    """
    cursor.execute(sql)
    count_con_id = cursor.fetchone()[0]
    print(f"Consorcios con id_contrato: {count_con_id:,}")
    
    # Verificar cuántos ya están en Detalle_Consorcios
    sql = """
        SELECT COUNT(DISTINCT a.id_contrato)
        FROM Licitaciones_Adjudicaciones a
        INNER JOIN Detalle_Consorcios d ON a.id_contrato = d.id_contrato
        WHERE a.ganador_nombre LIKE '%CONSORCIO%'
    """
    cursor.execute(sql)
    count_procesados = cursor.fetchone()[0]
    print(f"Consorcios ya procesados: {count_procesados:,}")
    
    # Consorcios pendientes
    pendientes = count_con_id - count_procesados
    print(f"Consorcios pendientes de procesar: {pendientes:,}")
    
    # Mostrar algunos ejemplos
    if count_consorcios > 0:
        print(f"\n{'=' * 60}")
        print("EJEMPLOS DE CONSORCIOS (primeros 10)")
        print("=" * 60)
        sql = """
            SELECT id_adjudicacion, id_contrato, ganador_nombre, monto_adjudicado
            FROM Licitaciones_Adjudicaciones 
            WHERE ganador_nombre LIKE '%CONSORCIO%'
            AND id_contrato IS NOT NULL 
            AND id_contrato != ''
            LIMIT 10
        """
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(f"\nID Contrato: {row[1]}")
            print(f"  Ganador: {row[2][:80]}...")
            print(f"  Monto: S/ {row[3]:,.2f}" if row[3] else "  Monto: N/A")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
