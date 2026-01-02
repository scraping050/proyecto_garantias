"""
Script para corregir la columna tipo_garantia
Modifica la lógica para clasificar SIN_GARANTIA como RETENCION
"""
import mysql.connector
from config.secrets_manager import get_db_config
import sys

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("=" * 100)
print(" CORRECCION: Columna tipo_garantia")
print("=" * 100)

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

try:
    print("\n1. Eliminando columna tipo_garantia actual...")
    cursor.execute("ALTER TABLE Licitaciones_Adjudicaciones DROP COLUMN tipo_garantia")
    print("   OK - Columna eliminada")
    
    print("\n2. Creando nueva columna con logica corregida...")
    cursor.execute("""
        ALTER TABLE Licitaciones_Adjudicaciones ADD COLUMN tipo_garantia VARCHAR(50) 
        GENERATED ALWAYS AS (
            CASE 
                WHEN entidad_financiera IS NULL 
                    OR entidad_financiera = '' 
                    OR entidad_financiera = 'SIN_GARANTIA'
                    OR entidad_financiera = 'NO_INFO'
                    OR entidad_financiera LIKE 'ERROR%'
                    OR entidad_financiera LIKE 'CONTRATO_NO%'
                THEN 'RETENCION'
                ELSE 'GARANTIA_BANCARIA'
            END
        ) STORED
    """)
    print("   OK - Columna creada con nueva logica")
    
    print("\n3. Creando indice...")
    cursor.execute("CREATE INDEX idx_tipo_garantia ON Licitaciones_Adjudicaciones(tipo_garantia)")
    print("   OK - Indice creado")
    
    conn.commit()
    
    print("\n4. Verificando resultados...")
    cursor.execute("""
        SELECT tipo_garantia, COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        GROUP BY tipo_garantia
        ORDER BY total DESC
    """)
    
    print("\n   Distribucion de tipo_garantia:")
    print("   " + "-" * 60)
    for tipo, total in cursor.fetchall():
        porcentaje = (total / 7959 * 100)
        print(f"   {tipo:<30} {total:>10,} ({porcentaje:>6.2f}%)")
    
    print("\n5. Verificando SIN_GARANTIA...")
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE entidad_financiera = 'SIN_GARANTIA'
    """)
    total_sin_garantia = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE entidad_financiera = 'SIN_GARANTIA' AND tipo_garantia = 'RETENCION'
    """)
    sin_garantia_retencion = cursor.fetchone()[0]
    
    print(f"\n   Total con SIN_GARANTIA: {total_sin_garantia:,}")
    print(f"   Clasificados como RETENCION: {sin_garantia_retencion:,}")
    
    if total_sin_garantia == sin_garantia_retencion:
        print("   OK - Todos los SIN_GARANTIA estan clasificados como RETENCION")
    else:
        print(f"   ERROR - {total_sin_garantia - sin_garantia_retencion} registros mal clasificados")
    
    print("\n" + "=" * 100)
    print(" CORRECCION COMPLETADA EXITOSAMENTE")
    print("=" * 100)
    
except Exception as e:
    print(f"\nERROR: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
