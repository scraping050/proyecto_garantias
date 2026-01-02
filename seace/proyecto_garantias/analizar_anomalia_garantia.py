"""
Análisis: Casos con entidad_financiera pero clasificados como RETENCION
"""
import mysql.connector
import sys
sys.path.insert(0, 'config')
from secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

print("="*100)
print("CASOS CON entidad_financiera PERO CLASIFICADOS COMO RETENCION")
print("="*100)

cursor.execute("""
    SELECT id_adjudicacion, estado_item, entidad_financiera, tipo_garantia
    FROM Licitaciones_Adjudicaciones
    WHERE entidad_financiera IS NOT NULL 
    AND entidad_financiera != '' 
    AND tipo_garantia = 'RETENCION'
    LIMIT 30
""")

print(f"\n{'ID':<20} {'ESTADO':<20} {'ENTIDAD_FINANCIERA':<40} {'TIPO':<20}")
print("-"*100)
for row in cursor.fetchall():
    print(f"{row[0]:<20} {row[1] or 'NULL':<20} {row[2] or 'NULL':<40} {row[3]:<20}")

print("\n\nConteo por entidad_financiera (clasificados como RETENCION):")
print("-"*100)
cursor.execute("""
    SELECT entidad_financiera, COUNT(*) as total
    FROM Licitaciones_Adjudicaciones
    WHERE tipo_garantia = 'RETENCION'
    AND entidad_financiera IS NOT NULL
    AND entidad_financiera != ''
    GROUP BY entidad_financiera
    ORDER BY total DESC
    LIMIT 20
""")

print(f"{'ENTIDAD_FINANCIERA':<50} {'TOTAL':<10}")
print("-"*100)
for row in cursor.fetchall():
    print(f"{row[0]:<50} {row[1]:<10}")

cursor.close()
conn.close()
