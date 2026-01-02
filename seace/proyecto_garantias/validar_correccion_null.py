"""
Script para validar la corrección de datos NULL
"""
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456789',
    database='garantias_seace'
)

cursor = conn.cursor(dictionary=True)

print("=" * 120)
print("VALIDACION: Corrección de Datos NULL")
print("=" * 120)

# 1. Tabla Contratos
print("\n1. TABLA CONTRATOS")
print("-" * 120)

cursor.execute("SELECT COUNT(*) as total FROM Contratos")
total_contratos = cursor.fetchone()['total']
print(f"Total contratos en BD: {total_contratos}")

# Ejemplos
cursor.execute("""
    SELECT c.id_contrato, c.id_adjudicacion, c.fecha_firma, c.estado_contrato
    FROM Contratos c
    LIMIT 5
""")
print("\nEjemplos:")
for row in cursor.fetchall():
    print(f"  {row['id_contrato']:15} | Adj: {row['id_adjudicacion']:20} | Fecha: {row['fecha_firma']}")

# 2. Adjudicaciones con id_contrato
print("\n2. ADJUDICACIONES CON id_contrato")
print("-" * 120)

cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Adjudicaciones
    WHERE id_contrato IS NOT NULL AND id_contrato != ''
""")
adj_con_contrato = cursor.fetchone()['total']

cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Adjudicaciones")
total_adj = cursor.fetchone()['total']

porcentaje = (adj_con_contrato / total_adj * 100) if total_adj > 0 else 0

print(f"Adjudicaciones CON id_contrato: {adj_con_contrato} de {total_adj} ({porcentaje:.2f}%)")

# 3. Casos CONTRATADO sin id_contrato (ANTES: 429)
print("\n3. CASOS CONTRATADO SIN id_contrato")
print("-" * 120)

cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.estado_proceso = 'CONTRATADO'
    AND (a.id_contrato IS NULL OR a.id_contrato = '')
""")
contratado_sin_id = cursor.fetchone()['total']

print(f"CONTRATADOS sin id_contrato: {contratado_sin_id}")
print(f"ANTES: 429")
print(f"MEJORA: {429 - contratado_sin_id} casos corregidos")

# 4. Relación Contratos vs Adjudicaciones
print("\n4. RELACION CONTRATOS vs ADJUDICACIONES")
print("-" * 120)

cursor.execute("""
    SELECT 
        COUNT(DISTINCT c.id_adjudicacion) as adj_con_contratos,
        COUNT(*) as total_contratos
    FROM Contratos c
""")
row = cursor.fetchone()
print(f"Adjudicaciones con contratos: {row['adj_con_contratos']}")
print(f"Total contratos: {row['total_contratos']}")
print(f"Promedio contratos por adjudicación: {row['total_contratos'] / row['adj_con_contratos']:.2f}")

# 5. Adjudicaciones con múltiples contratos
print("\n5. ADJUDICACIONES CON MULTIPLES CONTRATOS")
print("-" * 120)

cursor.execute("""
    SELECT id_adjudicacion, COUNT(*) as num_contratos
    FROM Contratos
    GROUP BY id_adjudicacion
    HAVING COUNT(*) > 1
    ORDER BY num_contratos DESC
    LIMIT 10
""")

print("Top 10 adjudicaciones con más contratos:")
for row in cursor.fetchall():
    print(f"  {row['id_adjudicacion']:30} | Contratos: {row['num_contratos']}")

# 6. Resumen de mejoras
print("\n6. RESUMEN DE MEJORAS")
print("=" * 120)

cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Adjudicaciones WHERE id_contrato IS NULL OR id_contrato = ''")
total_sin_contrato_ahora = cursor.fetchone()['total']

print(f"ANTES: 1,825 adjudicaciones sin id_contrato (23.97%)")
print(f"AHORA: {total_sin_contrato_ahora} adjudicaciones sin id_contrato ({total_sin_contrato_ahora*100/total_adj:.2f}%)")
print(f"MEJORA: {1825 - total_sin_contrato_ahora} casos corregidos")

cursor.close()
conn.close()

print("\n" + "=" * 120)
print("VALIDACION COMPLETADA")
print("=" * 120)
