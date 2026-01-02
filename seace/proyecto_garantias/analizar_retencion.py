"""
Script para analizar patrones de RETENCIÓN en garantías de obra
Basado en la normativa peruana de contrataciones públicas
"""
import mysql.connector
from collections import defaultdict

# Conexión a la base de datos
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456789',
    database='garantias_seace'
)

cursor = conn.cursor(dictionary=True)

print("=" * 80)
print("ANÁLISIS DE PATRONES PARA IDENTIFICAR RETENCIÓN")
print("=" * 80)

# 1. Analizar entidades financieras en adjudicaciones
print("\n1. DISTRIBUCIÓN DE ENTIDAD FINANCIERA")
print("-" * 80)
cursor.execute("""
    SELECT 
        CASE 
            WHEN entidad_financiera IS NULL OR entidad_financiera = '' THEN 'SIN ENTIDAD FINANCIERA'
            ELSE 'CON ENTIDAD FINANCIERA'
        END as tiene_entidad,
        COUNT(*) as total,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Licitaciones_Adjudicaciones), 2) as porcentaje
    FROM Licitaciones_Adjudicaciones
    GROUP BY tiene_entidad
    ORDER BY total DESC
""")
for row in cursor.fetchall():
    print(f"{row['tiene_entidad']}: {row['total']} ({row['porcentaje']}%)")

# 2. Cruce entre estado_proceso y entidad_financiera
print("\n2. ESTADO PROCESO vs ENTIDAD FINANCIERA")
print("-" * 80)
cursor.execute("""
    SELECT 
        c.estado_proceso,
        CASE 
            WHEN a.entidad_financiera IS NULL OR a.entidad_financiera = '' THEN 'SIN ENTIDAD'
            ELSE 'CON ENTIDAD'
        END as tiene_entidad,
        COUNT(*) as total
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.estado_proceso IN ('CONTRATADO', 'CONSENTIDO', 'ADJUDICADO')
    GROUP BY c.estado_proceso, tiene_entidad
    ORDER BY c.estado_proceso, total DESC
""")
for row in cursor.fetchall():
    print(f"{row['estado_proceso']:30} | {row['tiene_entidad']:15} | Total: {row['total']}")

# 3. Analizar casos específicos de CONTRATADO sin entidad financiera
print("\n3. CASOS CONTRATADO SIN ENTIDAD FINANCIERA (Posible RETENCIÓN)")
print("-" * 80)
cursor.execute("""
    SELECT 
        c.id_convocatoria,
        c.nomenclatura,
        c.comprador,
        c.categoria,
        c.monto_estimado,
        c.estado_proceso,
        a.ganador_nombre,
        a.monto_adjudicado,
        a.entidad_financiera
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.estado_proceso = 'CONTRATADO'
    AND (a.entidad_financiera IS NULL OR a.entidad_financiera = '')
    LIMIT 10
""")
print(f"{'ID Convocatoria':15} | {'Estado':15} | {'Categoría':15} | {'Monto':15} | {'Entidad':20}")
print("-" * 80)
for row in cursor.fetchall():
    monto = f"S/ {row['monto_adjudicado']:,.2f}" if row['monto_adjudicado'] else "N/A"
    entidad = row['entidad_financiera'] if row['entidad_financiera'] else "SIN ENTIDAD"
    print(f"{row['id_convocatoria']:15} | {row['estado_proceso']:15} | {row['categoria']:15} | {monto:15} | {entidad:20}")

# 4. Estadísticas por categoría
print("\n4. ANÁLISIS POR CATEGORÍA (OBRAS vs OTROS)")
print("-" * 80)
cursor.execute("""
    SELECT 
        c.categoria,
        c.estado_proceso,
        CASE 
            WHEN a.entidad_financiera IS NULL OR a.entidad_financiera = '' THEN 'SIN ENTIDAD'
            ELSE 'CON ENTIDAD'
        END as tiene_entidad,
        COUNT(*) as total
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.estado_proceso = 'CONTRATADO'
    GROUP BY c.categoria, c.estado_proceso, tiene_entidad
    ORDER BY c.categoria, total DESC
""")
for row in cursor.fetchall():
    print(f"{row['categoria']:15} | {row['estado_proceso']:15} | {row['tiene_entidad']:15} | Total: {row['total']}")

# 5. Resumen ejecutivo
print("\n5. RESUMEN EJECUTIVO")
print("=" * 80)
cursor.execute("""
    SELECT COUNT(*) as total_sin_entidad
    FROM Licitaciones_Adjudicaciones
    WHERE entidad_financiera IS NULL OR entidad_financiera = ''
""")
total_sin_entidad = cursor.fetchone()['total_sin_entidad']

cursor.execute("""
    SELECT COUNT(*) as total_contratado_sin_entidad
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.estado_proceso = 'CONTRATADO'
    AND (a.entidad_financiera IS NULL OR a.entidad_financiera = '')
""")
contratado_sin_entidad = cursor.fetchone()['total_contratado_sin_entidad']

cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Adjudicaciones")
total_adjudicaciones = cursor.fetchone()['total']

print(f"Total adjudicaciones: {total_adjudicaciones}")
print(f"Adjudicaciones SIN entidad financiera: {total_sin_entidad} ({total_sin_entidad*100/total_adjudicaciones:.2f}%)")
print(f"CONTRATADOS sin entidad financiera (posible RETENCIÓN): {contratado_sin_entidad}")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print("ANÁLISIS COMPLETADO")
print("=" * 80)
