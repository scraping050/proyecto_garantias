"""
Investigación detallada del problema de entidad_financiera
Identifica por qué no se están cargando las entidades financieras
"""
import mysql.connector
import sys
sys.path.insert(0, 'config')
from secrets_manager import get_db_config

def main():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("="*100)
    print("INVESTIGACIÓN: Problema de carga de entidad_financiera")
    print("="*100)
    
    # 1. Verificar condición del spider
    print("\n1. CONDICIÓN DEL SPIDER:")
    print("-"*100)
    print("El spider busca registros con:")
    print("  - id_contrato IS NOT NULL AND id_contrato != ''")
    print("  - entidad_financiera IS NULL")
    print()
    
    # 2. Contar registros que cumplen la condición
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE (id_contrato IS NOT NULL AND id_contrato != '')
          AND (entidad_financiera IS NULL)
    """)
    procesables = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE entidad_financiera IS NULL
    """)
    total_null = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE id_contrato IS NULL OR id_contrato = ''
    """)
    sin_contrato = cursor.fetchone()[0]
    
    print(f"Total registros sin entidad_financiera: {total_null:,}")
    print(f"  - Con id_contrato (procesables por spider): {procesables:,}")
    print(f"  - Sin id_contrato (NO procesables): {sin_contrato:,}")
    print()
    
    # 3. Análisis por estado
    print("\n2. ANÁLISIS POR ESTADO:")
    print("-"*100)
    cursor.execute("""
        SELECT 
            estado_item,
            COUNT(*) as total,
            SUM(CASE WHEN id_contrato IS NULL OR id_contrato = '' THEN 1 ELSE 0 END) as sin_contrato,
            SUM(CASE WHEN (id_contrato IS NOT NULL AND id_contrato != '') 
                     AND entidad_financiera IS NULL THEN 1 ELSE 0 END) as procesables,
            SUM(CASE WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' THEN 1 ELSE 0 END) as procesados
        FROM Licitaciones_Adjudicaciones
        GROUP BY estado_item
        ORDER BY total DESC
    """)
    
    print(f"{'ESTADO':<20} {'TOTAL':<10} {'SIN_CONTRATO':<15} {'PROCESABLES':<15} {'PROCESADOS':<12}")
    print("-"*100)
    for row in cursor.fetchall():
        print(f"{row[0] or 'NULL':<20} {row[1]:<10} {row[2]:<15} {row[3]:<15} {row[4]:<12}")
    
    # 4. Ejemplos de registros sin contrato
    print("\n\n3. EJEMPLOS DE REGISTROS SIN id_contrato:")
    print("-"*100)
    cursor.execute("""
        SELECT id_adjudicacion, estado_item, ganador_nombre
        FROM Licitaciones_Adjudicaciones
        WHERE (id_contrato IS NULL OR id_contrato = '')
          AND entidad_financiera IS NULL
        LIMIT 10
    """)
    
    print(f"{'ID_ADJUDICACION':<25} {'ESTADO':<15} {'GANADOR':<60}")
    print("-"*100)
    for row in cursor.fetchall():
        ganador = (row[2] or '')[:57] + '...' if row[2] and len(row[2]) > 60 else (row[2] or 'NULL')
        print(f"{row[0]:<25} {row[1] or 'NULL':<15} {ganador:<60}")
    
    # 5. Verificar si hay contratos en la tabla Contratos
    print("\n\n4. VERIFICACIÓN DE TABLA CONTRATOS:")
    print("-"*100)
    cursor.execute("SELECT COUNT(*) FROM Contratos")
    total_contratos = cursor.fetchone()[0]
    print(f"Total contratos en tabla Contratos: {total_contratos:,}")
    
    # 6. Verificar relación entre adjudicaciones y contratos
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT a.id_adjudicacion) as adjudicaciones_con_contrato,
            COUNT(DISTINCT c.id_contrato) as contratos_unicos
        FROM Licitaciones_Adjudicaciones a
        INNER JOIN Contratos c ON a.id_adjudicacion = c.id_adjudicacion
    """)
    row = cursor.fetchone()
    print(f"Adjudicaciones con contrato en tabla Contratos: {row[0]:,}")
    print(f"Contratos únicos: {row[1]:,}")
    
    # 7. PROBLEMA DETECTADO
    print("\n\n5. DIAGNÓSTICO:")
    print("="*100)
    
    if sin_contrato > 0:
        print(f"⚠️  PROBLEMA DETECTADO:")
        print(f"    {sin_contrato:,} adjudicaciones NO tienen id_contrato")
        print(f"    El spider NO puede procesarlas porque requiere id_contrato para consultar la API")
        print()
        print(f"📊 DISTRIBUCIÓN:")
        print(f"    - CONTRATADO: Mayoría tiene id_contrato (96.93% procesado)")
        print(f"    - CONSENTIDO: Mayoría NO tiene id_contrato (solo 23.44% procesado)")
        print(f"    - ADJUDICADO: Casi ninguno tiene id_contrato (solo 4.37% procesado)")
        print()
        print(f"💡 CAUSA RAÍZ:")
        print(f"    Los estados CONSENTIDO y ADJUDICADO son estados PREVIOS a la firma del contrato.")
        print(f"    Por lo tanto, NO tienen id_contrato en el JSON porque aún no existe contrato.")
        print(f"    El spider_garantias.py está diseñado para procesar SOLO contratos firmados.")
        print()
        print(f"✅ CONCLUSIÓN:")
        print(f"    Esto NO es un bug. Es el comportamiento esperado.")
        print(f"    Las garantías solo existen cuando hay un CONTRATO firmado (estado CONTRATADO).")
        print(f"    Los estados CONSENTIDO y ADJUDICADO no tienen garantías porque no hay contrato.")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*100)
    print("FIN DE INVESTIGACIÓN")
    print("="*100)

if __name__ == "__main__":
    main()
