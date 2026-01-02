"""
Script para generar estadísticas sobre tipos de garantía
Análisis por categoría, departamento, estado, etc.
"""
import mysql.connector
from collections import defaultdict

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456789',
    database='garantias_seace'
)

cursor = conn.cursor(dictionary=True)

print("=" * 100)
print("ESTADISTICAS DE TIPOS DE GARANTIA")
print("=" * 100)

# 1. Estadísticas generales
print("\n1. DISTRIBUCION GENERAL")
print("-" * 100)
cursor.execute("""
    SELECT tipo_garantia, COUNT(*) as total,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Licitaciones_Adjudicaciones), 2) as porcentaje
    FROM Licitaciones_Adjudicaciones
    GROUP BY tipo_garantia
    ORDER BY total DESC
""")

for row in cursor.fetchall():
    print(f"{row['tipo_garantia']:25} | Total: {row['total']:6} | Porcentaje: {row['porcentaje']:6.2f}%")

# 2. Por categoría
print("\n2. DISTRIBUCION POR CATEGORIA (Solo CONTRATADOS)")
print("-" * 100)
cursor.execute("""
    SELECT c.categoria, a.tipo_garantia, COUNT(*) as total
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.estado_proceso = 'CONTRATADO'
    GROUP BY c.categoria, a.tipo_garantia
    ORDER BY c.categoria, total DESC
""")

categoria_actual = None
for row in cursor.fetchall():
    if categoria_actual != row['categoria']:
        if categoria_actual is not None:
            print("-" * 100)
        categoria_actual = row['categoria']
        print(f"\n{categoria_actual}:")
    print(f"  {row['tipo_garantia']:25} | Total: {row['total']:6}")

# 3. Por departamento (Top 10)
print("\n3. TOP 10 DEPARTAMENTOS CON MAS RETENCIONES")
print("-" * 100)
cursor.execute("""
    SELECT c.departamento, COUNT(*) as total_retenciones
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE a.tipo_garantia = 'RETENCION'
    AND c.estado_proceso = 'CONTRATADO'
    AND c.departamento IS NOT NULL
    GROUP BY c.departamento
    ORDER BY total_retenciones DESC
    LIMIT 10
""")

for i, row in enumerate(cursor.fetchall(), 1):
    print(f"{i:2}. {row['departamento']:30} | Retenciones: {row['total_retenciones']:6}")

# 4. Por estado de proceso
print("\n4. DISTRIBUCION POR ESTADO DE PROCESO")
print("-" * 100)
cursor.execute("""
    SELECT c.estado_proceso, a.tipo_garantia, COUNT(*) as total
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    GROUP BY c.estado_proceso, a.tipo_garantia
    ORDER BY total DESC
    LIMIT 20
""")

for row in cursor.fetchall():
    print(f"{row['estado_proceso']:35} | {row['tipo_garantia']:25} | Total: {row['total']:6}")

# 5. Análisis de montos
print("\n5. ANALISIS DE MONTOS (Solo CONTRATADOS)")
print("-" * 100)
cursor.execute("""
    SELECT 
        a.tipo_garantia,
        COUNT(*) as cantidad,
        ROUND(AVG(a.monto_adjudicado), 2) as monto_promedio,
        ROUND(MIN(a.monto_adjudicado), 2) as monto_minimo,
        ROUND(MAX(a.monto_adjudicado), 2) as monto_maximo,
        ROUND(SUM(a.monto_adjudicado), 2) as monto_total
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.estado_proceso = 'CONTRATADO'
    AND a.monto_adjudicado > 0
    GROUP BY a.tipo_garantia
""")

for row in cursor.fetchall():
    print(f"\n{row['tipo_garantia']}:")
    print(f"  Cantidad: {row['cantidad']:,}")
    print(f"  Monto Promedio: S/ {row['monto_promedio']:,.2f}")
    print(f"  Monto Minimo: S/ {row['monto_minimo']:,.2f}")
    print(f"  Monto Maximo: S/ {row['monto_maximo']:,.2f}")
    print(f"  Monto Total: S/ {row['monto_total']:,.2f}")

# 6. Obras con retención (casos especiales)
print("\n6. OBRAS CON RETENCION (Primeros 10 casos)")
print("-" * 100)
cursor.execute("""
    SELECT 
        c.id_convocatoria,
        c.nomenclatura,
        c.comprador,
        a.monto_adjudicado,
        c.departamento
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.categoria = 'OBRAS'
    AND a.tipo_garantia = 'RETENCION'
    AND c.estado_proceso = 'CONTRATADO'
    ORDER BY a.monto_adjudicado DESC
    LIMIT 10
""")

for i, row in enumerate(cursor.fetchall(), 1):
    monto = f"S/ {row['monto_adjudicado']:,.2f}" if row['monto_adjudicado'] else "N/A"
    print(f"{i:2}. {row['id_convocatoria']:15} | {monto:20} | {row['departamento'] or 'N/A'}")

cursor.close()
conn.close()

print("\n" + "=" * 100)
print("ESTADISTICAS COMPLETADAS")
print("=" * 100)
