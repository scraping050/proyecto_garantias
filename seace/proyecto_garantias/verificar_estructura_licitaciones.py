import mysql.connector
import sys
sys.path.insert(0, 'config')
from secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

print("\n" + "="*80)
print("ESTRUCTURA DE LA TABLA Licitaciones_Cabecera")
print("="*80)

cursor.execute("DESCRIBE Licitaciones_Cabecera")
columns = cursor.fetchall()

print(f"\n{'COLUMNA':<35} {'TIPO':<25} {'NULL':<8} {'KEY':<8}")
print("-"*80)
for col in columns:
    print(f"{col[0]:<35} {col[1]:<25} {col[2]:<8} {col[3]:<8}")

print(f"\nTotal de columnas: {len(columns)}")

# Mostrar algunas columnas clave
print("\n" + "="*80)
print("COLUMNAS RELACIONADAS CON MONTOS Y GARANTÍAS:")
print("="*80)
for col in columns:
    col_name = col[0].lower()
    if any(keyword in col_name for keyword in ['monto', 'garantia', 'valor', 'precio']):
        print(f"  - {col[0]}")

conn.close()
