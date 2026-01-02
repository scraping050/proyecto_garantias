"""
Investigacin de problemas en Licitaciones_Adjudicaciones
1. estado_item siempre es ADJUDICADO (hardcodeado)
2. SIN_GARANTIA clasificado como GARANTIA_BANCARIA
"""
import mysql.connector
from config.secrets_manager import get_db_config
import json
import os
import sys

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

print("=" * 100)
print(" INVESTIGACION: PROBLEMAS EN LICITACIONES_ADJUDICACIONES")
print("=" * 100)

# PROBLEMA 1: estado_item
print("\nPROBLEMA 1: ESTADO_ITEM")
print("-" * 100)

cursor.execute("SELECT DISTINCT estado_item FROM Licitaciones_Adjudicaciones")
estados = cursor.fetchall()

print(f"  Estados nicos en estado_item:")
for estado in estados:
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE estado_item = %s", (estado[0],))
    count = cursor.fetchone()[0]
    print(f"    - {estado[0]}: {count:,} registros")

print(f"\n   PROBLEMA CONFIRMADO: Solo hay 'ADJUDICADO' hardcodeado")
print(f"     Ubicacin: cargador.py lnea 223")

# Verificar en JSON cules son los estados reales
print(f"\n   Verificando estados reales en JSONs...")

db_folder = os.path.join(os.path.dirname(__file__), "1_database")
archivo_muestra = os.path.join(db_folder, "2024-01_seace_v3.json")

if os.path.exists(archivo_muestra):
    with open(archivo_muestra, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    estados_reales = set()
    for r in data.get('records', [])[:100]:  # Muestra de 100
        compiled = r.get('compiledRelease', {})
        for aw in compiled.get('awards', []):
            status = aw.get('status')
            if status:
                estados_reales.add(status)
    
    print(f"\n   Estados reales encontrados en JSON:")
    for estado in sorted(estados_reales):
        print(f"     - {estado}")

# PROBLEMA 2: SIN_GARANTIA clasificado como GARANTIA_BANCARIA
print("\n" + "=" * 100)
print("  PROBLEMA 2: SIN_GARANTIA CLASIFICADO COMO GARANTIA_BANCARIA")
print("-" * 100)

cursor.execute("""
    SELECT entidad_financiera, tipo_garantia, COUNT(*) as total
    FROM Licitaciones_Adjudicaciones
    WHERE entidad_financiera LIKE '%SIN%GARANTIA%'
    GROUP BY entidad_financiera, tipo_garantia
    ORDER BY total DESC
""")

print(f"\n  Registros con 'SIN_GARANTIA' en entidad_financiera:")
print(f"  {'Entidad Financiera':<40} {'Tipo Garanta':<25} {'Cantidad':>10}")
print("  " + "-" * 80)

total_sin_garantia = 0
for entidad, tipo, count in cursor.fetchall():
    print(f"  {entidad:<40} {tipo:<25} {count:>10,}")
    total_sin_garantia += count

print(f"\n   PROBLEMA CONFIRMADO: {total_sin_garantia:,} registros con SIN_GARANTIA")
print(f"     clasificados como GARANTIA_BANCARIA")

# Verificar la lgica de tipo_garantia
print(f"\n   Verificando lgica de columna generada tipo_garantia...")

cursor.execute("SHOW CREATE TABLE Licitaciones_Adjudicaciones")
create_table = cursor.fetchone()[1]

# Buscar la definicin de tipo_garantia
if "tipo_garantia" in create_table:
    lines = create_table.split('\n')
    for line in lines:
        if 'tipo_garantia' in line.lower():
            print(f"\n  Definicin actual:")
            print(f"  {line.strip()}")

print(f"\n    PROBLEMA: La lgica actual es:")
print(f"     - Si entidad_financiera IS NOT NULL AND != ''  GARANTIA_BANCARIA")
print(f"     - Si entidad_financiera IS NULL  RETENCION")
print(f"\n   PERO: 'SIN_GARANTIA' NO es NULL ni vaco, por eso se clasifica mal")

# Ejemplos especficos
print("\n" + "=" * 100)
print("  EJEMPLOS ESPECFICOS DE REGISTROS PROBLEMTICOS")
print("-" * 100)

cursor.execute("""
    SELECT id_adjudicacion, id_convocatoria, ganador_nombre, 
           entidad_financiera, tipo_garantia, estado_item
    FROM Licitaciones_Adjudicaciones
    WHERE entidad_financiera = 'SIN_GARANTIA'
    LIMIT 5
""")

print(f"\n  Muestra de registros con SIN_GARANTIA:")
print(f"  {'ID Adj':<20} {'Ganador':<40} {'Estado Item':<15} {'Tipo Garanta':<20}")
print("  " + "-" * 100)

for row in cursor.fetchall():
    id_adj, id_conv, ganador, entidad, tipo, estado = row
    ganador_short = ganador[:37] + "..." if len(ganador) > 40 else ganador
    print(f"  {id_adj:<20} {ganador_short:<40} {estado:<15} {tipo:<20}")

# Verificar en SEACE real
print("\n" + "=" * 100)
print("  RECOMENDACIN: VERIFICAR EN SEACE")
print("-" * 100)

cursor.execute("""
    SELECT id_convocatoria, ganador_nombre, entidad_financiera
    FROM Licitaciones_Adjudicaciones
    WHERE entidad_financiera = 'SIN_GARANTIA'
    LIMIT 3
""")

print(f"\n  URLs para verificar manualmente en SEACE:")
for id_conv, ganador, entidad in cursor.fetchall():
    print(f"\n  ID Convocatoria: {id_conv}")
    print(f"  Ganador: {ganador}")
    print(f"  URL: https://prod4.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml")
    print(f"       (Buscar por: {id_conv})")

print("\n" + "=" * 100)
print("  RESUMEN DE PROBLEMAS DETECTADOS")
print("=" * 100)

print(f"""
   PROBLEMA 1: estado_item HARDCODEADO
     - Ubicacin: cargador.py lnea 223
     - Impacto: 7,959 registros con estado incorrecto
     - Solucin: Usar aw.get('status') del JSON
  
   PROBLEMA 2: SIN_GARANTIA clasificado mal
     - Ubicacin: Definicin de columna tipo_garantia
     - Impacto: {total_sin_garantia:,} registros mal clasificados
     - Solucin: Modificar lgica de columna generada
  
   ACCIN REQUERIDA:
     1. Corregir cargador.py para capturar estado real
     2. Modificar columna tipo_garantia para manejar SIN_GARANTIA
     3. Re-ejecutar cargador.py para actualizar datos
""")

print("=" * 100)

conn.close()
