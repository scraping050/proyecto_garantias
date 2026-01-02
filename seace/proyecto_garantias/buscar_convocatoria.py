"""
Script para aclarar la diferencia entre ESTADO y TIPO DE GARANTIA
Busca una convocatoria específica
"""
import mysql.connector
import sys

if len(sys.argv) < 2:
    print("Uso: python buscar_convocatoria.py <id_convocatoria>")
    sys.exit(1)

id_conv = sys.argv[1]

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456789',
    database='garantias_seace'
)

cursor = conn.cursor(dictionary=True)

cursor.execute("""
    SELECT 
        c.id_convocatoria,
        c.nomenclatura,
        c.estado_proceso,
        c.categoria,
        c.comprador,
        a.ganador_nombre,
        a.entidad_financiera,
        a.tipo_garantia,
        a.monto_adjudicado
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE c.id_convocatoria = %s
""", (id_conv,))

row = cursor.fetchone()

if not row:
    print(f"No se encontro la convocatoria {id_conv}")
    cursor.close()
    conn.close()
    sys.exit(1)

print("=" * 100)
print(f"CONVOCATORIA: {row['id_convocatoria']}")
print("=" * 100)
print(f"\nNomenclatura: {row['nomenclatura'][:80]}...")
print(f"Categoria: {row['categoria']}")
print(f"Comprador: {row['comprador'][:60]}...")
print(f"Ganador: {row['ganador_nombre'][:60]}...")
print(f"Monto: S/ {row['monto_adjudicado']:,.2f}" if row['monto_adjudicado'] else "Monto: N/A")

print("\n" + "-" * 100)
print("IMPORTANTE: Diferencia entre ESTADO y TIPO DE GARANTIA")
print("-" * 100)

print(f"\n1. ESTADO DEL PROCESO (estado_proceso):")
print(f"   >>> {row['estado_proceso']} <<<")
print(f"   Esto indica en que etapa esta el proceso de licitacion:")
print(f"   - CONVOCADO: En proceso de convocatoria")
print(f"   - ADJUDICADO: Ya se adjudico pero no se firmo contrato")
print(f"   - CONSENTIDO: Adjudicacion consentida (sin apelaciones)")
print(f"   - CONTRATADO: Contrato firmado")
print(f"   - DESIERTO: Sin postores validos")
print(f"   - NULO: Proceso anulado")

print(f"\n2. TIPO DE GARANTIA (tipo_garantia):")
print(f"   >>> {row['tipo_garantia']} <<<")
print(f"   Esto indica QUE TIPO DE GARANTIA se uso:")
print(f"   - GARANTIA_BANCARIA: Carta fianza o poliza de caucion")
print(f"   - RETENCION: Retencion del 10% de pagos")

print(f"\n3. ENTIDAD FINANCIERA:")
print(f"   >>> {row['entidad_financiera'] or 'SIN ENTIDAD'} <<<")
print(f"   Si hay entidad: GARANTIA_BANCARIA")
print(f"   Si NO hay entidad: RETENCION")

print("\n" + "=" * 100)
print("CONCLUSION")
print("=" * 100)
print(f"Esta convocatoria esta en estado: {row['estado_proceso']}")
print(f"Y usa garantia tipo: {row['tipo_garantia']}")
print("\nSON DOS COSAS DIFERENTES!")
print("=" * 100)

cursor.close()
conn.close()
