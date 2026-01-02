import mysql.connector
import sys

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor(dictionary=True)

print("="*80)
print("VERIFICACIÓN DE ESTADOS EN LA BASE DE DATOS")
print("="*80)

# Estados únicos
cursor.execute("SELECT DISTINCT estado_proceso FROM Licitaciones_Cabecera ORDER BY estado_proceso")
estados = cursor.fetchall()
print("\nEstados únicos en Licitaciones_Cabecera:")
for e in estados:
    if e['estado_proceso']:
        cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Cabecera WHERE estado_proceso = %s", (e['estado_proceso'],))
        count = cursor.fetchone()['total']
        print(f"  - {e['estado_proceso']}: {count:,} registros")

# Verificar algunos registros
print("\nPrimeros 10 registros:")
cursor.execute("SELECT id_convocatoria, descripcion, estado_proceso FROM Licitaciones_Cabecera LIMIT 10")
rows = cursor.fetchall()
for r in rows:
    desc = (r['descripcion'] or 'N/A')[:50]
    print(f"  ID: {r['id_convocatoria']}, Estado: {r['estado_proceso']}, Desc: {desc}")

conn.close()
print("\n" + "="*80)
