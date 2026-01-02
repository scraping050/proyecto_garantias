import mysql.connector
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'config'))
from secrets_manager import get_db_config

def main():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("="*80)
    print("ANÁLISIS DE ADJUDICACIONES SIN id_contrato")
    print("="*80)
    print()
    
    # Distribución por estado_item
    cursor.execute("""
        SELECT estado_item, COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        WHERE id_contrato IS NULL OR id_contrato = ''
        GROUP BY estado_item
        ORDER BY total DESC
    """)
    
    print("DISTRIBUCIÓN POR ESTADO_ITEM:")
    print("-"*80)
    for row in cursor.fetchall():
        estado, count = row
        print(f"  {estado}: {count:,}")
    
    print()
    print("="*80)
    print("VERIFICACIÓN: ¿Están procesadas las adjudicaciones CON id_contrato?")
    print("="*80)
    print()
    
    # Verificar adjudicaciones CON contrato
    cursor.execute("""
        SELECT 
            COUNT(*) as total_con_contrato,
            SUM(CASE WHEN entidad_financiera IS NULL THEN 1 ELSE 0 END) as sin_procesar,
            SUM(CASE WHEN entidad_financiera IS NOT NULL THEN 1 ELSE 0 END) as procesadas
        FROM Licitaciones_Adjudicaciones
        WHERE id_contrato IS NOT NULL AND id_contrato != ''
    """)
    result = cursor.fetchone()
    total_con_contrato, sin_procesar, procesadas = result
    
    print(f"Total adjudicaciones CON id_contrato: {total_con_contrato:,}")
    print(f"Sin procesar: {sin_procesar:,}")
    print(f"Procesadas: {procesadas:,}")
    
    if sin_procesar == 0:
        print()
        print("✅ PERFECTO: El spider procesó el 100% de adjudicaciones con contrato!")
    else:
        print()
        print(f"⚠️ ATENCIÓN: Quedan {sin_procesar:,} adjudicaciones con contrato sin procesar")
    
    conn.close()

if __name__ == "__main__":
    main()
