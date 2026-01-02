"""
Script para comparar ESTADO vs TIPO DE GARANTIA
Muestra ejemplos de diferentes combinaciones
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
print("EJEMPLOS: ESTADO DEL PROCESO vs TIPO DE GARANTIA")
print("=" * 120)
print("\nIMPORTANTE: Son dos conceptos DIFERENTES")
print("- ESTADO: Etapa del proceso de licitacion (CONVOCADO, CONSENTIDO, CONTRATADO, etc.)")
print("- TIPO GARANTIA: Tipo de garantia usada (GARANTIA_BANCARIA o RETENCION)")
print("=" * 120)

# Ejemplos de diferentes combinaciones
combinaciones = [
    ('CONSENTIDO', 'RETENCION'),
    ('CONSENTIDO', 'GARANTIA_BANCARIA'),
    ('CONTRATADO', 'RETENCION'),
    ('CONTRATADO', 'GARANTIA_BANCARIA'),
    ('ADJUDICADO', 'RETENCION'),
    ('ADJUDICADO', 'GARANTIA_BANCARIA')
]

for estado, tipo_gar in combinaciones:
    print(f"\n{'-' * 120}")
    print(f"COMBINACION: Estado={estado} + Tipo Garantia={tipo_gar}")
    print(f"{'-' * 120}")
    
    cursor.execute("""
        SELECT 
            c.id_convocatoria,
            c.nomenclatura,
            c.estado_proceso,
            c.categoria,
            a.ganador_nombre,
            a.tipo_garantia,
            a.entidad_financiera,
            a.monto_adjudicado
        FROM Licitaciones_Cabecera c
        INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
        WHERE c.estado_proceso = %s
        AND a.tipo_garantia = %s
        LIMIT 3
    """, (estado, tipo_gar))
    
    rows = cursor.fetchall()
    
    if not rows:
        print(f"  No se encontraron ejemplos para esta combinacion")
        continue
    
    for i, row in enumerate(rows, 1):
        print(f"\n  Ejemplo {i}:")
        print(f"    ID: {row['id_convocatoria']}")
        print(f"    Categoria: {row['categoria']}")
        print(f"    Monto: S/ {row['monto_adjudicado']:,.2f}" if row['monto_adjudicado'] else "    Monto: N/A")
        print(f"    >>> ESTADO PROCESO: {row['estado_proceso']}")
        print(f"    >>> TIPO GARANTIA: {row['tipo_garantia']}")
        print(f"    Entidad: {row['entidad_financiera'] or 'SIN ENTIDAD'}")

# Resumen estadístico
print("\n" + "=" * 120)
print("RESUMEN ESTADISTICO: ESTADO vs TIPO DE GARANTIA")
print("=" * 120)

cursor.execute("""
    SELECT 
        c.estado_proceso,
        a.tipo_garantia,
        COUNT(*) as total
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    GROUP BY c.estado_proceso, a.tipo_garantia
    ORDER BY total DESC
    LIMIT 15
""")

print(f"\n{'Estado Proceso':35} | {'Tipo Garantia':25} | {'Total':10}")
print("-" * 120)
for row in cursor.fetchall():
    print(f"{row['estado_proceso']:35} | {row['tipo_garantia']:25} | {row['total']:10}")

cursor.close()
conn.close()

print("\n" + "=" * 120)
print("CONCLUSION: El ESTADO y el TIPO DE GARANTIA son INDEPENDIENTES")
print("=" * 120)
