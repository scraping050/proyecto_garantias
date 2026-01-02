"""
Análisis de distribución de tipos de procedimiento
"""
import mysql.connector
from config.secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

# Distribución por tipo
cursor.execute("""
    SELECT tipo_procedimiento, COUNT(*) as total 
    FROM Licitaciones_Cabecera 
    GROUP BY tipo_procedimiento 
    ORDER BY total DESC
""")

resultados = cursor.fetchall()

print("=" * 70)
print("DISTRIBUCIÓN POR TIPO DE PROCEDIMIENTO")
print("=" * 70)

for tipo, total in resultados:
    print(f"{tipo:45} | {total:>6,}")

# Total Licitación Pública
cursor.execute("""
    SELECT COUNT(*) 
    FROM Licitaciones_Cabecera 
    WHERE tipo_procedimiento = 'Licitación Pública'
""")

lp_count = cursor.fetchone()[0]

print("=" * 70)
print(f"{'TOTAL Licitación Pública':45} | {lp_count:>6,}")
print("=" * 70)

# Comparación con API
print("\nCOMPARACIÓN CON API SEACE:")
print(f"  API SEACE reporta: 9,981")
print(f"  Base de datos tiene: {lp_count:,}")
print(f"  Diferencia: {lp_count - 9981:+,} ({((lp_count - 9981) / 9981 * 100):+.2f}%)")

conn.close()
