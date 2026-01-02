import mysql.connector
import sys
sys.path.insert(0, 'config')
from secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

# Actualizar los 3 registros a SIN_GARANTIA
ids = ["1136959-20602007970", "1148638-20602007970", "1164267-1746873"]

for id_adj in ids:
    cursor.execute(
        "UPDATE Licitaciones_Adjudicaciones SET entidad_financiera = %s WHERE id_adjudicacion = %s",
        ("SIN_GARANTIA", id_adj)
    )

conn.commit()
print(f"Actualizados: {cursor.rowcount} registros")

# Verificar
cursor.execute('''
    SELECT id_adjudicacion, entidad_financiera 
    FROM Licitaciones_Adjudicaciones 
    WHERE id_adjudicacion IN (%s, %s, %s)
''', tuple(ids))

print("\nVerificacion:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

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
    print("\n🎉 100% COMPLETADO!")

conn.close()
