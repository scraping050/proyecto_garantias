import mysql.connector
import sys
sys.path.insert(0, 'config')
from secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

print("Actualizando los 3 registros a SIN_GARANTIA...")

# Actualizar uno por uno para asegurar que funcione
registros = [
    "1136959-20602007970",
    "1148638-20602007970",
    "1164267-1746873"
]

for id_adj in registros:
    cursor.execute(
        "UPDATE Licitaciones_Adjudicaciones SET entidad_financiera = 'SIN_GARANTIA' WHERE id_adjudicacion = %s",
        (id_adj,)
    )
    print(f"  Actualizado: {id_adj} (rows affected: {cursor.rowcount})")

conn.commit()

# Verificar
print("\nVerificando...")
for id_adj in registros:
    cursor.execute(
        "SELECT entidad_financiera FROM Licitaciones_Adjudicaciones WHERE id_adjudicacion = %s",
        (id_adj,)
    )
    valor = cursor.fetchone()[0]
    print(f"  {id_adj}: '{valor}'")

# Verificar pendientes
cursor.execute('''
    SELECT COUNT(*) 
    FROM Licitaciones_Adjudicaciones 
    WHERE (id_contrato IS NOT NULL AND id_contrato != "")
      AND (entidad_financiera IS NULL OR entidad_financiera = "")
''')
pendientes = cursor.fetchone()[0]

print(f"\nPendientes restantes: {pendientes}")

if pendientes == 0:
    print("\n*** 100% COMPLETADO ***")
else:
    print(f"\nAun hay {pendientes} pendientes")

conn.close()
