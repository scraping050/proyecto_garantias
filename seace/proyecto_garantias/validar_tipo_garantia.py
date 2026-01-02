"""
Script para validar la clasificación de tipo de garantía
Muestra una muestra aleatoria de datos para revisión manual
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
print("VALIDACION DE CLASIFICACION DE TIPO DE GARANTIA")
print("=" * 100)

# Muestra aleatoria para validación manual
cursor.execute("""
    SELECT 
        c.id_convocatoria,
        c.nomenclatura,
        c.comprador,
        c.categoria,
        c.estado_proceso,
        a.ganador_nombre,
        a.entidad_financiera,
        a.tipo_garantia
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.estado_proceso = 'CONTRATADO'
    ORDER BY RAND()
    LIMIT 20
""")

print("\nMUESTRA ALEATORIA PARA VALIDACION MANUAL (20 casos)")
print("-" * 100)

for i, row in enumerate(cursor.fetchall(), 1):
    print(f"\n{i}. ID Convocatoria: {row['id_convocatoria']}")
    print(f"   Categoria: {row['categoria']}")
    print(f"   Estado: {row['estado_proceso']}")
    print(f"   Ganador: {row['ganador_nombre'][:50]}...")
    print(f"   Entidad Financiera: {row['entidad_financiera'] or 'SIN ENTIDAD'}")
    print(f"   >>> Tipo Garantia (calculado): {row['tipo_garantia']} <<<")

# Verificación de consistencia
print("\n" + "=" * 100)
print("VERIFICACION DE CONSISTENCIA")
print("=" * 100)

# Casos que deberían ser RETENCION
cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Adjudicaciones
    WHERE (entidad_financiera IS NULL OR entidad_financiera = '')
    AND tipo_garantia != 'RETENCION'
""")
inconsistentes_retencion = cursor.fetchone()['total']

# Casos que deberían ser GARANTIA_BANCARIA
cursor.execute("""
    SELECT COUNT(*) as total
    FROM Licitaciones_Adjudicaciones
    WHERE entidad_financiera IS NOT NULL AND entidad_financiera != ''
    AND tipo_garantia != 'GARANTIA_BANCARIA'
""")
inconsistentes_bancaria = cursor.fetchone()['total']

print(f"\nCasos inconsistentes (sin entidad pero NO marcados como RETENCION): {inconsistentes_retencion}")
print(f"Casos inconsistentes (con entidad pero NO marcados como GARANTIA_BANCARIA): {inconsistentes_bancaria}")

if inconsistentes_retencion == 0 and inconsistentes_bancaria == 0:
    print("\nOK - Todos los casos son consistentes!")
else:
    print("\nADVERTENCIA: Se encontraron inconsistencias")

cursor.close()
conn.close()

print("\n" + "=" * 100)
print("VALIDACION COMPLETADA")
print("=" * 100)
