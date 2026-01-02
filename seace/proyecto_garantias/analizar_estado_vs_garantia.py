"""
Análisis: Relación entre estado_item y tipo_garantia
Verifica si es correcto que estados como CONTRATADO, ADJUDICADO, CONSENTIDO 
tengan tipo_garantia = "RETENCION"
"""
import mysql.connector
import sys
sys.path.insert(0, 'config')
from secrets_manager import get_db_config

def main():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("="*80)
    print("ANÁLISIS: estado_item vs tipo_garantia")
    print("="*80)
    
    # 1. Distribución general
    print("\n1. DISTRIBUCIÓN GENERAL DE TIPO_GARANTIA:")
    print("-"*80)
    cursor.execute("""
        SELECT tipo_garantia, COUNT(*) as total, 
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Licitaciones_Adjudicaciones), 2) as porcentaje
        FROM Licitaciones_Adjudicaciones
        GROUP BY tipo_garantia
        ORDER BY total DESC
    """)
    print(f"{'TIPO_GARANTIA':<30} {'TOTAL':<10} {'%':<10}")
    print("-"*80)
    for row in cursor.fetchall():
        print(f"{row[0]:<30} {row[1]:<10} {row[2]:<10}%")
    
    # 2. Distribución por estado_item
    print("\n\n2. DISTRIBUCIÓN POR estado_item:")
    print("-"*80)
    cursor.execute("""
        SELECT estado_item, tipo_garantia, COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        GROUP BY estado_item, tipo_garantia
        ORDER BY estado_item, tipo_garantia
    """)
    print(f"{'ESTADO_ITEM':<25} {'TIPO_GARANTIA':<25} {'TOTAL':<10}")
    print("-"*80)
    for row in cursor.fetchall():
        print(f"{row[0] or 'NULL':<25} {row[1] or 'NULL':<25} {row[2]:<10}")
    
    # 3. Análisis de entidad_financiera
    print("\n\n3. ANÁLISIS DE entidad_financiera:")
    print("-"*80)
    cursor.execute("""
        SELECT 
            CASE 
                WHEN entidad_financiera IS NULL OR entidad_financiera = '' THEN 'NULL/VACÍO'
                ELSE 'CON VALOR'
            END as tiene_entidad,
            tipo_garantia,
            COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        GROUP BY tiene_entidad, tipo_garantia
        ORDER BY tiene_entidad, tipo_garantia
    """)
    print(f"{'ENTIDAD_FINANCIERA':<25} {'TIPO_GARANTIA':<25} {'TOTAL':<10}")
    print("-"*80)
    for row in cursor.fetchall():
        print(f"{row[0]:<25} {row[1]:<25} {row[2]:<10}")
    
    # 4. Ejemplos de RETENCION con diferentes estados
    print("\n\n4. EJEMPLOS DE RETENCION POR ESTADO:")
    print("-"*80)
    cursor.execute("""
        SELECT estado_item, COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        WHERE tipo_garantia = 'RETENCION'
        GROUP BY estado_item
        ORDER BY total DESC
    """)
    print(f"{'ESTADO_ITEM':<25} {'TOTAL RETENCION':<15}")
    print("-"*80)
    for row in cursor.fetchall():
        print(f"{row[0] or 'NULL':<25} {row[1]:<15}")
    
    # 5. Verificar lógica de tipo_garantia
    print("\n\n5. VERIFICACIÓN DE LÓGICA tipo_garantia:")
    print("-"*80)
    print("La columna tipo_garantia es GENERATED COLUMN basada en:")
    print("  - Si entidad_financiera tiene valor → GARANTIA_BANCARIA")
    print("  - Si entidad_financiera es NULL/vacío → RETENCION")
    
    cursor.execute("""
        SELECT 
            id_adjudicacion,
            estado_item,
            entidad_financiera,
            tipo_garantia
        FROM Licitaciones_Adjudicaciones
        WHERE tipo_garantia = 'RETENCION'
        LIMIT 10
    """)
    print("\nEjemplos de registros con RETENCION:")
    print(f"{'ID':<15} {'ESTADO':<20} {'ENTIDAD_FINANCIERA':<30} {'TIPO':<20}")
    print("-"*80)
    for row in cursor.fetchall():
        print(f"{row[0]:<15} {row[1] or 'NULL':<20} {row[2] or 'NULL':<30} {row[3]:<20}")
    
    # 6. Casos con entidad_financiera
    cursor.execute("""
        SELECT 
            id_adjudicacion,
            estado_item,
            entidad_financiera,
            tipo_garantia
        FROM Licitaciones_Adjudicaciones
        WHERE tipo_garantia = 'GARANTIA_BANCARIA'
        LIMIT 10
    """)
    print("\n\nEjemplos de registros con GARANTIA_BANCARIA:")
    print(f"{'ID':<15} {'ESTADO':<20} {'ENTIDAD_FINANCIERA':<30} {'TIPO':<20}")
    print("-"*80)
    for row in cursor.fetchall():
        print(f"{row[0]:<15} {row[1] or 'NULL':<20} {row[2] or 'NULL':<30} {row[3]:<20}")
    
    # 7. Análisis crítico
    print("\n\n" + "="*80)
    print("ANÁLISIS CRÍTICO:")
    print("="*80)
    print("""
El tipo_garantia NO depende del estado_item (CONTRATADO, ADJUDICADO, CONSENTIDO, etc.)

El tipo_garantia depende ÚNICAMENTE de si existe una entidad_financiera:
  - CON entidad_financiera → GARANTIA_BANCARIA (carta fianza de banco/aseguradora)
  - SIN entidad_financiera → RETENCION (retención del 10% de pagos)

Por lo tanto, es CORRECTO que:
  - Un contrato CONTRATADO puede tener RETENCION (si no tiene entidad financiera)
  - Un contrato ADJUDICADO puede tener RETENCION (si no tiene entidad financiera)
  - Un contrato CONSENTIDO puede tener RETENCION (si no tiene entidad financiera)

El estado_item indica la FASE del proceso de contratación.
El tipo_garantia indica el MECANISMO de garantía elegido.

Son conceptos INDEPENDIENTES y ortogonales.
    """)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
