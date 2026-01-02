import mysql.connector
import sys
sys.path.insert(0, 'config')
from secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

print("="*80)
print("VERIFICACION FINAL - 100% COMPLETADO")
print("="*80)

# 1. Verificar los 3 registros específicos
print("\n1. Los 3 registros procesados:")
print("-"*80)
cursor.execute('''
    SELECT id_adjudicacion, entidad_financiera, LENGTH(entidad_financiera) as len
    FROM Licitaciones_Adjudicaciones 
    WHERE id_adjudicacion IN ("1136959-20602007970", "1148638-20602007970", "1164267-1746873")
''')

for row in cursor.fetchall():
    print(f"{row[0]}: '{row[1]}' (length: {row[2]})")

# 2. Total de registros procesables
cursor.execute('''
    SELECT COUNT(*) 
    FROM Licitaciones_Adjudicaciones 
    WHERE id_contrato IS NOT NULL AND id_contrato != ""
''')
total_procesables = cursor.fetchone()[0]

# 3. Registros procesados (NOT NULL AND NOT EMPTY)
cursor.execute('''
    SELECT COUNT(*) 
    FROM Licitaciones_Adjudicaciones 
    WHERE (id_contrato IS NOT NULL AND id_contrato != "")
      AND (entidad_financiera IS NOT NULL AND entidad_financiera != "")
''')
procesados = cursor.fetchone()[0]

# 4. Registros pendientes (NULL OR EMPTY)
cursor.execute('''
    SELECT COUNT(*) 
    FROM Licitaciones_Adjudicaciones 
    WHERE (id_contrato IS NOT NULL AND id_contrato != "")
      AND (entidad_financiera IS NULL OR entidad_financiera = "")
''')
pendientes = cursor.fetchone()[0]

print(f"\n2. RESUMEN:")
print("-"*80)
print(f"Total procesables: {total_procesables}")
print(f"Procesados: {procesados} ({procesados*100/total_procesables:.2f}%)")
print(f"Pendientes: {pendientes} ({pendientes*100/total_procesables:.2f}%)")

if pendientes == 0:
    print("\n" + "="*80)
    print("EXITO! 100% COMPLETADO")
    print("="*80)
else:
    print(f"\nAun hay {pendientes} pendientes")
    
    # Mostrar cuáles son
    cursor.execute('''
        SELECT id_adjudicacion, id_contrato, entidad_financiera, LENGTH(entidad_financiera) as len
        FROM Licitaciones_Adjudicaciones 
        WHERE (id_contrato IS NOT NULL AND id_contrato != "")
          AND (entidad_financiera IS NULL OR entidad_financiera = "")
        LIMIT 10
    ''')
    
    print("\nRegistros pendientes:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: '{row[1]}' (length: {row[3]})")

conn.close()
