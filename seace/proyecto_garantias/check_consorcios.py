import mysql.connector
from config.secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE ganador_nombre LIKE '%CONSORCIO%'")
total_consorcios = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM Detalle_Consorcios")
total_detalle = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*) 
    FROM Licitaciones_Adjudicaciones a
    LEFT JOIN Detalle_Consorcios d ON a.id_contrato = d.id_contrato
    WHERE a.ganador_nombre LIKE '%CONSORCIO%' 
      AND d.id_contrato IS NULL
      AND a.id_contrato IS NOT NULL AND a.id_contrato != ''
""")
pendientes = cursor.fetchone()[0]

print("=" * 60)
print(" ESTADO DE CONSORCIOS")
print("=" * 60)
print(f"Total adjudicaciones con CONSORCIO: {total_consorcios:,}")
print(f"Registros en Detalle_Consorcios:    {total_detalle:,}")
print(f"Consorcios pendientes de procesar:  {pendientes:,}")
print("=" * 60)

conn.close()
