"""
Verificación post-ejecución del spider
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
    print("VERIFICACION POST-EJECUCION DEL SPIDER")
    print("="*120)
    
    # Verificar los 3 registros específicos
    print("\n1. VERIFICANDO LOS 3 REGISTROS ESPECIFICOS:")
    print("-"*120)
    
    registros = [
        '1136959-20602007970',
        '1148638-20602007970',
        '1164267-1746873'
    ]
    
    for id_adj in registros:
        cursor.execute("""
            SELECT id_adjudicacion, id_contrato, entidad_financiera, ganador_nombre
            FROM Licitaciones_Adjudicaciones
            WHERE id_adjudicacion = %s
        """, (id_adj,))
        
        row = cursor.fetchone()
        if row:
            print(f"\nID: {row[0]}")
            print(f"  Contrato: {row[1]}")
            print(f"  Entidad: {row[2] or 'NULL'}")
            print(f"  Ganador: {row[3]}")
        else:
            print(f"\n[ERROR] No se encontro el registro {id_adj}")
    
    # Estadísticas generales
    print("\n\n2. ESTADISTICAS GENERALES ACTUALES:")
    print("-"*120)
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE (id_contrato IS NOT NULL AND id_contrato != '')
          AND (entidad_financiera IS NULL OR entidad_financiera = '')
    """)
    pendientes = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE entidad_financiera IS NOT NULL AND entidad_financiera != ''
    """)
    procesados = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE id_contrato IS NOT NULL AND id_contrato != ''
    """)
    procesables = cursor.fetchone()[0]
    
    print(f"\nTotal procesables (con id_contrato): {procesables:,}")
    print(f"Procesados (con entidad): {procesados:,}")
    print(f"Pendientes (sin entidad): {pendientes:,}")
    
    if pendientes == 0:
        print("\n[OK] PERFECTO! Todos los registros procesables han sido procesados.")
        print(f"     Completitud: 100%")
    else:
        print(f"\n[ADVERTENCIA] Aun hay {pendientes} registros pendientes")
        
        # Mostrar cuáles son
        cursor.execute("""
            SELECT id_adjudicacion, id_contrato, ganador_nombre
            FROM Licitaciones_Adjudicaciones
            WHERE (id_contrato IS NOT NULL AND id_contrato != '')
              AND (entidad_financiera IS NULL OR entidad_financiera = '')
            LIMIT 10
        """)
        
        print("\nRegistros pendientes:")
        for row in cursor.fetchall():
            print(f"  - {row[0]} | {row[1]} | {row[2][:50]}")
    
    # Verificar la consulta que usa el spider
    print("\n\n3. VERIFICANDO CONSULTA DEL SPIDER:")
    print("-"*120)
    
    cursor.execute("""
        SELECT id_adjudicacion, id_contrato, ganador_nombre 
        FROM Licitaciones_Adjudicaciones 
        WHERE (id_contrato IS NOT NULL AND id_contrato != '')
          AND (entidad_financiera IS NULL) 
        LIMIT 10
    """)
    
    spider_pendientes = cursor.fetchall()
    
    print(f"\nRegistros que el spider deberia procesar: {len(spider_pendientes)}")
    
    if len(spider_pendientes) == 0:
        print("[OK] El spider no encuentra pendientes porque todos tienen algun valor en entidad_financiera")
        print("     (incluso si es vacio '')")
    else:
        print("[ADVERTENCIA] El spider SI deberia encontrar estos registros:")
        for row in spider_pendientes:
            print(f"  - {row[0]} | {row[1]} | {row[2][:50]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*120)
    print("FIN DE VERIFICACION")
    print("="*120)

if __name__ == "__main__":
    main()
