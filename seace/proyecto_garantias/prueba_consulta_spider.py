"""
Prueba directa de la consulta del spider
"""
import mysql.connector
import sys

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

def main():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("="*120)
    print("PRUEBA DIRECTA DE LA CONSULTA DEL SPIDER")
    print("="*120)
    
    # Consulta EXACTA del spider
    print("\n1. CONSULTA EXACTA DEL SPIDER:")
    print("-"*120)
    
    sql_spider = """
        SELECT id_adjudicacion, id_contrato, ganador_nombre 
        FROM Licitaciones_Adjudicaciones 
        WHERE (id_contrato IS NOT NULL AND id_contrato != '')
          AND (entidad_financiera IS NULL) 
        LIMIT 50 
    """
    
    print(sql_spider)
    
    cursor.execute(sql_spider)
    resultados = cursor.fetchall()
    
    print(f"\nResultados: {len(resultados)}")
    
    for row in resultados:
        print(f"  - {row[0]} | {row[1]} | {row[2][:50]}")
    
    # Verificar estado de los 3 registros específicos
    print("\n\n2. ESTADO DETALLADO DE LOS 3 REGISTROS:")
    print("-"*120)
    
    registros = [
        '1136959-20602007970',
        '1148638-20602007970',
        '1164267-1746873'
    ]
    
    for id_adj in registros:
        cursor.execute("""
            SELECT 
                id_adjudicacion,
                id_contrato,
                id_contrato IS NOT NULL as tiene_id,
                id_contrato != '' as id_no_vacio,
                entidad_financiera,
                entidad_financiera IS NULL as es_null,
                LENGTH(entidad_financiera) as longitud
            FROM Licitaciones_Adjudicaciones
            WHERE id_adjudicacion = %s
        """, (id_adj,))
        
        row = cursor.fetchone()
        if row:
            print(f"\n{row[0]}:")
            print(f"  id_contrato: '{row[1]}'")
            print(f"  tiene_id: {row[2]}")
            print(f"  id_no_vacio: {row[3]}")
            print(f"  entidad_financiera: {row[4]}")
            print(f"  es_null: {row[5]}")
            print(f"  longitud: {row[6]}")
            
            # Verificar si cumple condiciones del spider
            cumple = (row[1] is not None and row[1] != '') and (row[4] is None)
            print(f"  CUMPLE CONDICIONES SPIDER: {cumple}")
    
    # Verificar tipo de datos de id_contrato
    print("\n\n3. VERIFICAR TIPO DE DATO DE id_contrato:")
    print("-"*120)
    
    cursor.execute("""
        DESCRIBE Licitaciones_Adjudicaciones
    """)
    
    for row in cursor.fetchall():
        if row[0] in ['id_contrato', 'entidad_financiera']:
            print(f"{row[0]}: {row[1]} | NULL={row[2]} | Default={row[4]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*120)
    print("FIN DE PRUEBA")
    print("="*120)

if __name__ == "__main__":
    main()
