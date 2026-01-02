"""
INVESTIGACION DETALLADA: Problemas detectados en auditoria
"""
import mysql.connector
from config.secrets_manager import get_db_config
import json
import os

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

print("=" * 100)
print(" INVESTIGACION DETALLADA DE PROBLEMAS")
print("=" * 100)

# ============================================================================
# PROBLEMA 1: id_convocatoria duplicados (108)
# ============================================================================
print("\n" + "=" * 100)
print(" PROBLEMA 1: id_convocatoria duplicados")
print("=" * 100)

cursor.execute("""
    SELECT id_convocatoria, COUNT(*) as total
    FROM Licitaciones_Cabecera
    GROUP BY id_convocatoria
    HAVING COUNT(*) > 1
    ORDER BY total DESC
    LIMIT 10
""")

duplicados = cursor.fetchall()
print(f"\nTotal id_convocatoria duplicados: {len(duplicados)}")
print(f"\nTop 10 duplicados:")
print(f"{'ID Convocatoria':<20} {'Cantidad':>10}")
print("-" * 35)

for id_conv, total in duplicados:
    print(f"{id_conv:<20} {total:>10}")

# Ver detalles de un duplicado
if duplicados:
    id_ejemplo = duplicados[0][0]
    cursor.execute("""
        SELECT ocid, nomenclatura, fecha_publicacion, archivo_origen
        FROM Licitaciones_Cabecera
        WHERE id_convocatoria = %s
    """, (id_ejemplo,))
    
    print(f"\nDetalle de duplicados para id_convocatoria '{id_ejemplo}':")
    for row in cursor.fetchall():
        print(f"  - OCID: {row[0]}")
        print(f"    Nomenclatura: {row[1][:80]}")
        print(f"    Fecha: {row[2]}")
        print(f"    Archivo: {row[3]}")
        print()

print("\nCAUSA PROBABLE:")
print("  - Un mismo id_convocatoria aparece en multiples archivos JSON mensuales")
print("  - El OCID es unico, pero id_convocatoria se repite")
print("\nSOLUCION:")
print("  - CORRECTO: OCID debe ser la clave primaria (ya implementado)")
print("  - id_convocatoria puede repetirse legitimamente")
print("  - NO ES UN ERROR, es comportamiento esperado")

# ============================================================================
# PROBLEMA 2: Adjudicaciones huerfanas (5)
# ============================================================================
print("\n" + "=" * 100)
print(" PROBLEMA 2: Adjudicaciones huerfanas")
print("=" * 100)

cursor.execute("""
    SELECT a.id_adjudicacion, a.id_convocatoria, a.ganador_nombre, a.ocid
    FROM Licitaciones_Adjudicaciones a
    LEFT JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
    WHERE c.id_convocatoria IS NULL
""")

huerfanas = cursor.fetchall()
print(f"\nTotal adjudicaciones huerfanas: {len(huerfanas)}")
print(f"\nDetalle:")
print(f"{'ID Adjudicacion':<25} {'ID Convocatoria':<15} {'OCID':<30} {'Ganador':<40}")
print("-" * 115)

for row in huerfanas:
    ganador = row[2][:37] + "..." if len(row[2]) > 40 else row[2]
    print(f"{row[0]:<25} {row[1]:<15} {row[3]:<30} {ganador:<40}")

print("\nCAUSA PROBABLE:")
print("  - Adjudicaciones cuya cabecera fue eliminada en limpieza de obsoletos")
print("  - O error en la relacion FK (deberia usar OCID en lugar de id_convocatoria)")
print("\nSOLUCION:")
print("  - Eliminar estas 5 adjudicaciones huerfanas")
print("  - O corregir la relacion FK para usar OCID")

# ============================================================================
# PROBLEMA 3: Contratos huerfanos (19)
# ============================================================================
print("\n" + "=" * 100)
print(" PROBLEMA 3: Contratos huerfanos")
print("=" * 100)

cursor.execute("""
    SELECT c.id_contrato, c.id_adjudicacion, c.id_convocatoria, c.fecha_firma
    FROM Contratos c
    LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_adjudicacion = a.id_adjudicacion
    WHERE a.id_adjudicacion IS NULL
    LIMIT 10
""")

cont_huerfanos = cursor.fetchall()
print(f"\nTotal contratos huerfanos: 19")
print(f"\nPrimeros 10:")
print(f"{'ID Contrato':<20} {'ID Adjudicacion':<25} {'ID Convocatoria':<15} {'Fecha Firma':<15}")
print("-" * 80)

for row in cont_huerfanos:
    print(f"{row[0]:<20} {row[1]:<25} {row[2]:<15} {str(row[3]):<15}")

print("\nCAUSA PROBABLE:")
print("  - Contratos cuyas adjudicaciones fueron eliminadas")
print("  - O error en el mapeo id_adjudicacion")
print("\nSOLUCION:")
print("  - Eliminar estos 19 contratos huerfanos")

# ============================================================================
# PROBLEMA 4: RUCs con prefijo PE-RUC (7,661)
# ============================================================================
print("\n" + "=" * 100)
print(" PROBLEMA 4: RUCs con prefijo PE-RUC")
print("=" * 100)

cursor.execute("""
    SELECT ganador_ruc, COUNT(*) as total
    FROM Licitaciones_Adjudicaciones
    WHERE ganador_ruc LIKE 'PE-RUC-%'
    GROUP BY ganador_ruc
    ORDER BY total DESC
    LIMIT 5
""")

print(f"\nTotal RUCs con prefijo PE-RUC: 7,661")
print(f"\nEjemplos mas frecuentes:")
print(f"{'RUC con prefijo':<25} {'Cantidad':>10}")
print("-" * 40)

for ruc, total in cursor.fetchall():
    print(f"{ruc:<25} {total:>10}")

print("\nCAUSA:")
print("  - El JSON de SEACE incluye el prefijo 'PE-RUC-' en el campo suppliers.id")
print("  - Deberia limpiarse para dejar solo los 11 digitos")
print("\nSOLUCION:")
print("  - Modificar cargador.py para limpiar el prefijo")
print("  - Actualizar registros existentes: UPDATE ... SET ganador_ruc = REPLACE(ganador_ruc, 'PE-RUC-', '')")

# ============================================================================
# PROBLEMA 5: Estado DESCONOCIDO (7,954)
# ============================================================================
print("\n" + "=" * 100)
print(" PROBLEMA 5: Estado DESCONOCIDO")
print("=" * 100)

cursor.execute("""
    SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE estado_item = 'DESCONOCIDO'
""")
total_desconocido = cursor.fetchone()[0]

print(f"\nTotal con estado DESCONOCIDO: {total_desconocido:,}")

print("\nCAUSA:")
print("  - Los awards en el JSON NO tienen campo 'status'")
print("  - El cargador.py intenta leer aw.get('status') que siempre es None")
print("\nSOLUCION:")
print("  - Investigar donde esta el estado real en el JSON")
print("  - Opciones: tender.status, items[].statusDetails, o aceptar DESCONOCIDO")

# ============================================================================
# PROBLEMA 6: Fechas en orden illogico (11)
# ============================================================================
print("\n" + "=" * 100)
print(" PROBLEMA 6: Fechas en orden illogico")
print("=" * 100)

cursor.execute("""
    SELECT c.id_convocatoria, c.fecha_publicacion, a.fecha_adjudicacion, 
           DATEDIFF(a.fecha_adjudicacion, c.fecha_publicacion) as dias_diferencia
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE a.fecha_adjudicacion < c.fecha_publicacion
    ORDER BY dias_diferencia
""")

print(f"\nTotal adjudicaciones antes de publicacion: 11")
print(f"\nDetalle:")
print(f"{'ID Convocatoria':<20} {'Fecha Publicacion':<20} {'Fecha Adjudicacion':<20} {'Dias Diferencia':>15}")
print("-" * 80)

for row in cursor.fetchall():
    print(f"{row[0]:<20} {str(row[1]):<20} {str(row[2]):<20} {row[3]:>15}")

print("\nCAUSA PROBABLE:")
print("  - Error en los datos fuente (SEACE)")
print("  - O error en la extraccion de fechas")
print("\nSOLUCION:")
print("  - Verificar en JSON original")
print("  - Si es error de fuente, documentar como anomalia")

print("\n" + "=" * 100)
print(" FIN DE INVESTIGACION")
print("=" * 100)

conn.close()
