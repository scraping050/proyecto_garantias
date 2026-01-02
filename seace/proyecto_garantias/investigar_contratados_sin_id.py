"""
Investigar por qué 429 casos CONTRATADO no tienen id_contrato
"""
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456789',
    database='garantias_seace'
)

cursor = conn.cursor(dictionary=True)

print("=" * 100)
print("INVESTIGACION: CONTRATADOS sin id_contrato")
print("=" * 100)

# Obtener ejemplos
cursor.execute("""
    SELECT 
        c.id_convocatoria,
        c.nomenclatura,
        c.estado_proceso,
        a.id_adjudicacion,
        a.ganador_nombre
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.estado_proceso = 'CONTRATADO'
    AND (a.id_contrato IS NULL OR a.id_contrato = '')
    LIMIT 10
""")

print("\nEjemplos de CONTRATADOS sin id_contrato:")
print("-" * 100)
for row in cursor.fetchall():
    print(f"ID: {row['id_convocatoria']:10} | Adj: {row['id_adjudicacion']:25} | Ganador: {row['ganador_nombre'][:40]}")

# Verificar si tienen contratos en la tabla Contratos
print("\nVerificando si tienen contratos en tabla Contratos:")
print("-" * 100)

cursor.execute("""
    SELECT 
        a.id_adjudicacion,
        a.id_contrato as id_contrato_adj,
        COUNT(ct.id_contrato) as num_contratos_tabla
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    LEFT JOIN Contratos ct ON a.id_adjudicacion = ct.id_adjudicacion
    WHERE c.estado_proceso = 'CONTRATADO'
    AND (a.id_contrato IS NULL OR a.id_contrato = '')
    GROUP BY a.id_adjudicacion, a.id_contrato
    LIMIT 10
""")

for row in cursor.fetchall():
    print(f"Adj: {row['id_adjudicacion']:30} | id_contrato en adj: {row['id_contrato_adj'] or 'NULL':15} | Contratos en tabla: {row['num_contratos_tabla']}")

cursor.close()
conn.close()

print("\n" + "=" * 100)
print("CONCLUSION:")
print("Si num_contratos_tabla = 0, significa que NO hay contratos en el JSON")
print("Esto es NORMAL - algunos procesos CONTRATADOS no tienen contracts[] en SEACE")
print("=" * 100)
