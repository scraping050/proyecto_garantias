import mysql.connector
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'config'))
from secrets_manager import get_db_config

def main():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("="*100)
    print("ANÁLISIS: tipo_garantia POR estado_item")
    print("="*100)
    print()
    
    # 1. Distribución general
    print("1. DISTRIBUCIÓN DE tipo_garantia POR estado_item")
    print("-"*100)
    cursor.execute("""
        SELECT 
            estado_item,
            tipo_garantia,
            COUNT(*) as total,
            ROUND(AVG(monto_adjudicado), 2) as monto_promedio
        FROM Licitaciones_Adjudicaciones
        GROUP BY estado_item, tipo_garantia
        ORDER BY estado_item, tipo_garantia
    """)
    
    print(f"{'Estado Item':<30} | {'Tipo Garantía':<20} | {'Total':>8} | {'Monto Promedio':>20}")
    print("-"*100)
    for row in cursor.fetchall():
        estado, tipo, total, monto = row
        print(f"{estado:<30} | {tipo:<20} | {total:>8,} | S/ {monto:>18,.2f}")
    
    print()
    print("="*100)
    print("2. ANÁLISIS ESPECÍFICO: CONTRATADO con RETENCIÓN")
    print("="*100)
    print()
    
    # 2. Casos CONTRATADO con RETENCIÓN
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN id_contrato IS NOT NULL AND id_contrato != '' THEN 1 ELSE 0 END) as con_contrato,
            SUM(CASE WHEN id_contrato IS NULL OR id_contrato = '' THEN 1 ELSE 0 END) as sin_contrato,
            SUM(CASE WHEN entidad_financiera IS NULL THEN 1 ELSE 0 END) as sin_entidad
        FROM Licitaciones_Adjudicaciones
        WHERE estado_item = 'CONTRATADO' AND tipo_garantia = 'RETENCION'
    """)
    result = cursor.fetchone()
    total, con_contrato, sin_contrato, sin_entidad = result
    
    print(f"Total CONTRATADO con tipo_garantia=RETENCIÓN: {total:,}")
    print(f"  - Con id_contrato: {con_contrato:,}")
    print(f"  - Sin id_contrato: {sin_contrato:,}")
    print(f"  - Sin entidad_financiera: {sin_entidad:,}")
    print()
    
    # 3. Lógica actual de tipo_garantia
    print("="*100)
    print("3. VERIFICACIÓN DE LA LÓGICA")
    print("="*100)
    print()
    print("La columna tipo_garantia es GENERADA con esta lógica:")
    print("  - Si entidad_financiera IS NOT NULL → GARANTIA_BANCARIA")
    print("  - Si entidad_financiera IS NULL → RETENCIÓN")
    print()
    
    # 4. Problema potencial
    print("="*100)
    print("4. PROBLEMA IDENTIFICADO")
    print("="*100)
    print()
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones
        WHERE estado_item = 'CONTRATADO' 
          AND (id_contrato IS NULL OR id_contrato = '')
    """)
    contratados_sin_id = cursor.fetchone()[0]
    
    print(f"⚠️ Hay {contratados_sin_id:,} adjudicaciones con estado_item='CONTRATADO' pero SIN id_contrato")
    print()
    print("Estas adjudicaciones:")
    print("  - NO tienen id_contrato → NO fueron procesadas por spider_garantias.py")
    print("  - NO tienen entidad_financiera → Se clasifican como RETENCIÓN por defecto")
    print("  - Pero NO sabemos realmente si usan retención o garantía bancaria")
    print()
    
    # 5. Estados CONSENTIDO y ADJUDICADO
    print("="*100)
    print("5. ESTADOS CONSENTIDO Y ADJUDICADO")
    print("="*100)
    print()
    
    cursor.execute("""
        SELECT 
            estado_item,
            COUNT(*) as total,
            SUM(CASE WHEN id_contrato IS NOT NULL AND id_contrato != '' THEN 1 ELSE 0 END) as con_contrato
        FROM Licitaciones_Adjudicaciones
        WHERE estado_item IN ('CONSENTIDO', 'ADJUDICADO')
        GROUP BY estado_item
    """)
    
    print("¿Estos estados deberían tener tipo de garantía definido?")
    print("-"*100)
    for row in cursor.fetchall():
        estado, total, con_contrato = row
        print(f"{estado}: {total:,} casos, {con_contrato:,} tienen id_contrato")
    
    print()
    print("INTERPRETACIÓN:")
    print("  - CONSENTIDO: Adjudicado pero aún no contratado → NO debería tener garantía aún")
    print("  - ADJUDICADO: Adjudicado pero pendiente → NO debería tener garantía aún")
    print("  - CONTRATADO: Contrato firmado → SÍ debería tener garantía de cumplimiento")
    print()
    
    # 6. Recomendación
    print("="*100)
    print("6. RECOMENDACIÓN")
    print("="*100)
    print()
    print("El tipo_garantia SOLO debería aplicarse a adjudicaciones CONTRATADAS.")
    print()
    print("Estados que NO deberían tener tipo_garantia:")
    print("  - CONSENTIDO (aún no hay contrato)")
    print("  - ADJUDICADO (aún no hay contrato)")
    print("  - DESCONOCIDO (estado indefinido)")
    print()
    print("Estados que SÍ deberían tener tipo_garantia:")
    print("  - CONTRATADO (contrato firmado, requiere garantía de cumplimiento)")
    print()
    
    conn.close()

if __name__ == "__main__":
    main()
