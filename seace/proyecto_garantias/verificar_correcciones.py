import mysql.connector
from config.secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

print("=" * 80)
print(" VERIFICACION FINAL DE CORRECCIONES")
print("=" * 80)

print("\n1. Estados en estado_item:")
cursor.execute('SELECT DISTINCT estado_item, COUNT(*) FROM Licitaciones_Adjudicaciones GROUP BY estado_item ORDER BY COUNT(*) DESC')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1]:,}')

print("\n2. Tipos de garantia:")
cursor.execute('SELECT tipo_garantia, COUNT(*) FROM Licitaciones_Adjudicaciones GROUP BY tipo_garantia')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1]:,}')

print("\n3. SIN_GARANTIA clasificacion:")
cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE entidad_financiera = 'SIN_GARANTIA' AND tipo_garantia = 'RETENCION'")
print(f'  SIN_GARANTIA como RETENCION: {cursor.fetchone()[0]:,}')

conn.close()
print("\n" + "=" * 80)
