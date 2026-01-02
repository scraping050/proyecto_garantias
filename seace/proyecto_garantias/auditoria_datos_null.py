"""
Auditoría completa de datos NULL en la base de datos
Identifica campos que están NULL pero deberían tener información
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

print("=" * 120)
print("AUDITORIA COMPLETA DE DATOS NULL/VACIOS")
print("=" * 120)

# 1. Análisis de Licitaciones_Cabecera
print("\n1. TABLA: Licitaciones_Cabecera")
print("-" * 120)

campos_cabecera = [
    'ocid', 'nomenclatura', 'descripcion', 'comprador', 'categoria', 
    'tipo_procedimiento', 'monto_estimado', 'moneda', 'fecha_publicacion',
    'estado_proceso', 'ubicacion_completa', 'departamento', 'provincia', 
    'distrito', 'archivo_origen'
]

for campo in campos_cabecera:
    # Para campos DATE, solo verificar NULL
    if campo in ['fecha_publicacion']:
        cursor.execute(f"""
            SELECT COUNT(*) as total_null
            FROM Licitaciones_Cabecera
            WHERE {campo} IS NULL
        """)
    else:
        cursor.execute(f"""
            SELECT COUNT(*) as total_null
            FROM Licitaciones_Cabecera
            WHERE {campo} IS NULL OR {campo} = ''
        """)
    total_null = cursor.fetchone()['total_null']
    
    cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Cabecera")
    total = cursor.fetchone()['total']
    
    porcentaje = (total_null / total * 100) if total > 0 else 0
    
    if total_null > 0:
        print(f"  {campo:25} | NULL/Vacio: {total_null:6} ({porcentaje:5.2f}%)")

# 2. Análisis de Licitaciones_Adjudicaciones
print("\n2. TABLA: Licitaciones_Adjudicaciones")
print("-" * 120)

campos_adjudicaciones = [
    'id_contrato', 'ganador_nombre', 'ganador_ruc', 'monto_adjudicado',
    'fecha_adjudicacion', 'estado_item', 'entidad_financiera'
]

for campo in campos_adjudicaciones:
    # Para campos DATE, solo verificar NULL
    if campo in ['fecha_adjudicacion']:
        cursor.execute(f"""
            SELECT COUNT(*) as total_null
            FROM Licitaciones_Adjudicaciones
            WHERE {campo} IS NULL
        """)
    else:
        cursor.execute(f"""
            SELECT COUNT(*) as total_null
            FROM Licitaciones_Adjudicaciones
            WHERE {campo} IS NULL OR {campo} = ''
        """)
    total_null = cursor.fetchone()['total_null']
    
    cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Adjudicaciones")
    total = cursor.fetchone()['total']
    
    porcentaje = (total_null / total * 100) if total > 0 else 0
    
    if total_null > 0:
        print(f"  {campo:25} | NULL/Vacio: {total_null:6} ({porcentaje:5.2f}%)")

# 3. Casos críticos: id_contrato NULL
print("\n3. CASOS CRITICOS: id_contrato NULL")
print("-" * 120)

cursor.execute("""
    SELECT COUNT(*) as total_sin_contrato
    FROM Licitaciones_Adjudicaciones
    WHERE id_contrato IS NULL OR id_contrato = ''
""")
total_sin_contrato = cursor.fetchone()['total_sin_contrato']

print(f"Total adjudicaciones SIN id_contrato: {total_sin_contrato}")

# Ejemplos
cursor.execute("""
    SELECT 
        a.id_adjudicacion,
        a.id_contrato,
        c.id_convocatoria,
        c.nomenclatura,
        c.estado_proceso,
        a.ganador_nombre
    FROM Licitaciones_Adjudicaciones a
    INNER JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
    WHERE a.id_contrato IS NULL OR a.id_contrato = ''
    LIMIT 10
""")

print("\nEjemplos de adjudicaciones sin id_contrato:")
for row in cursor.fetchall():
    print(f"  ID Adj: {row['id_adjudicacion']:20} | Estado: {row['estado_proceso']:15} | Convocatoria: {row['id_convocatoria']}")

# 4. Análisis por estado
print("\n4. ADJUDICACIONES SIN id_contrato POR ESTADO")
print("-" * 120)

cursor.execute("""
    SELECT 
        c.estado_proceso,
        COUNT(*) as total_sin_contrato
    FROM Licitaciones_Adjudicaciones a
    INNER JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
    WHERE a.id_contrato IS NULL OR a.id_contrato = ''
    GROUP BY c.estado_proceso
    ORDER BY total_sin_contrato DESC
""")

for row in cursor.fetchall():
    print(f"  {row['estado_proceso']:35} | Sin contrato: {row['total_sin_contrato']:6}")

# 5. Fechas NULL
print("\n5. FECHAS NULL")
print("-" * 120)

cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Cabecera
    WHERE fecha_publicacion IS NULL
""")
print(f"  Licitaciones sin fecha_publicacion: {cursor.fetchone()['total']}")

cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Adjudicaciones
    WHERE fecha_adjudicacion IS NULL
""")
print(f"  Adjudicaciones sin fecha_adjudicacion: {cursor.fetchone()['total']}")

# 6. Montos en 0 o NULL
print("\n6. MONTOS EN 0 O NULL")
print("-" * 120)

cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Cabecera
    WHERE monto_estimado IS NULL OR monto_estimado = 0
""")
print(f"  Licitaciones con monto_estimado NULL/0: {cursor.fetchone()['total']}")

cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Adjudicaciones
    WHERE monto_adjudicado IS NULL OR monto_adjudicado = 0
""")
print(f"  Adjudicaciones con monto_adjudicado NULL/0: {cursor.fetchone()['total']}")

# 7. Ubicación incompleta
print("\n7. UBICACION INCOMPLETA")
print("-" * 120)

cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Cabecera
    WHERE departamento IS NULL OR departamento = ''
""")
print(f"  Sin departamento: {cursor.fetchone()['total']}")

cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Cabecera
    WHERE provincia IS NULL OR provincia = ''
""")
print(f"  Sin provincia: {cursor.fetchone()['total']}")

cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Cabecera
    WHERE distrito IS NULL OR distrito = ''
""")
print(f"  Sin distrito: {cursor.fetchone()['total']}")

# 8. Detalle_Consorcios
print("\n8. TABLA: Detalle_Consorcios")
print("-" * 120)

cursor.execute("SELECT COUNT(*) as total FROM Detalle_Consorcios")
total_consorcios = cursor.fetchone()['total']
print(f"  Total registros en Detalle_Consorcios: {total_consorcios}")

if total_consorcios > 0:
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM Detalle_Consorcios
        WHERE ruc_miembro IS NULL OR ruc_miembro = ''
    """)
    print(f"  Sin RUC miembro: {cursor.fetchone()['total']}")
    
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM Detalle_Consorcios
        WHERE nombre_miembro IS NULL OR nombre_miembro = ''
    """)
    print(f"  Sin nombre miembro: {cursor.fetchone()['total']}")

cursor.close()
conn.close()

print("\n" + "=" * 120)
print("AUDITORIA COMPLETADA")
print("=" * 120)
