"""
AUDITORÍA EXHAUSTIVA DE ENTIDADES FINANCIERAS
Análisis detallado de todas las variantes de cada entidad
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from secrets_manager import get_db_config
import mysql.connector
from collections import defaultdict

print("=" * 100)
print("🔍 AUDITORÍA EXHAUSTIVA DE ENTIDADES FINANCIERAS")
print("=" * 100)
print()

# Conectar a BD
DB_CONFIG = get_db_config()
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Obtener TODAS las entidades tal como están en la BD
query = """
SELECT 
    a.entidad_financiera,
    COUNT(*) as total_garantias,
    COALESCE(SUM(a.monto_adjudicado), 0) as monto_total,
    COUNT(DISTINCT c.departamento) as departamentos,
    COUNT(DISTINCT c.provincia) as provincias,
    COUNT(DISTINCT c.distrito) as distritos
FROM licitaciones_adjudicaciones a
LEFT JOIN licitaciones_cabecera c ON a.id_convocatoria = c.id_convocatoria
WHERE a.entidad_financiera IS NOT NULL 
AND a.entidad_financiera != ''
AND a.entidad_financiera != 'SIN_GARANTIA'
GROUP BY a.entidad_financiera
ORDER BY total_garantias DESC
"""

cursor.execute(query)
results = cursor.fetchall()

print(f"Total de registros únicos en BD: {len(results)}")
print()

# Función para extraer nombre principal
def get_main_entity(name):
    if '|' in name:
        return name.split('|')[0].strip()
    return name.strip()

# Agrupar por entidad principal
entities_consolidated = defaultdict(lambda: {
    'variantes': [],
    'total_garantias': 0,
    'monto_total': 0,
    'departamentos': set(),
    'provincias': set(),
    'distritos': set()
})

for row in results:
    nombre_completo = row[0]
    nombre_principal = get_main_entity(nombre_completo)
    
    entities_consolidated[nombre_principal]['variantes'].append({
        'nombre': nombre_completo,
        'garantias': row[1],
        'monto': float(row[2])
    })
    entities_consolidated[nombre_principal]['total_garantias'] += row[1]
    entities_consolidated[nombre_principal]['monto_total'] += float(row[2])

# Necesitamos recalcular departamentos consolidados
print("Recalculando departamentos consolidados...")
for nombre_principal in entities_consolidated.keys():
    # Buscar todas las variantes de esta entidad
    variantes = [v['nombre'] for v in entities_consolidated[nombre_principal]['variantes']]
    
    # Query para obtener departamentos únicos de todas las variantes
    placeholders = ','.join(['%s'] * len(variantes))
    query_depts = f"""
    SELECT DISTINCT c.departamento
    FROM licitaciones_adjudicaciones a
    LEFT JOIN licitaciones_cabecera c ON a.id_convocatoria = c.id_convocatoria
    WHERE a.entidad_financiera IN ({placeholders})
    AND c.departamento IS NOT NULL
    """
    cursor.execute(query_depts, variantes)
    depts = cursor.fetchall()
    entities_consolidated[nombre_principal]['departamentos_count'] = len(depts)

# Ordenar por total de garantías
sorted_entities = sorted(entities_consolidated.items(), 
                         key=lambda x: x[1]['total_garantias'], 
                         reverse=True)

print()
print("=" * 100)
print("📊 AUDITORÍA COMPLETA - ENTIDADES CONSOLIDADAS")
print("=" * 100)
print()

# Mostrar TOP 20 con detalles
print("TOP 20 ENTIDADES CONSOLIDADAS:")
print()

for idx, (nombre_principal, data) in enumerate(sorted_entities[:20], 1):
    num_variantes = len(data['variantes'])
    total_garantias = data['total_garantias']
    monto_total = data['monto_total']
    departamentos = data.get('departamentos_count', 0)
    
    # Determinar cobertura
    if departamentos >= 24:
        cobertura = "🟢 NACIONAL"
    elif departamentos >= 15:
        cobertura = "🔵 REGIONAL"
    elif departamentos >= 5:
        cobertura = "🟡 MULTI-DEPT"
    else:
        cobertura = "⚪ LOCAL"
    
    print(f"[{idx}] {nombre_principal}")
    print(f"    ├─ Variantes en BD: {num_variantes}")
    print(f"    ├─ Total Garantías: {total_garantias:,}")
    print(f"    ├─ Monto Total: S/ {monto_total:,.2f}")
    print(f"    ├─ Departamentos: {departamentos}")
    print(f"    └─ Cobertura: {cobertura}")
    
    if num_variantes > 1:
        print(f"    ")
        print(f"    Desglose de variantes:")
        for v in data['variantes']:
            print(f"      • \"{v['nombre']}\" → {v['garantias']} garantías, S/ {v['monto']:,.2f}")
    
    print()

# Resumen general
print("=" * 100)
print("📈 RESUMEN DE AUDITORÍA")
print("=" * 100)
print(f"Registros en BD (sin consolidar): {len(results)}")
print(f"Entidades ÚNICAS (consolidadas): {len(sorted_entities)}")
print(f"Reducción: {len(results) - len(sorted_entities)} registros duplicados")
print()

# Contar cuántas tienen múltiples variantes
multi_variant = sum(1 for _, data in sorted_entities if len(data['variantes']) > 1)
print(f"Entidades con múltiples variantes: {multi_variant}")
print(f"Entidades con 1 sola variante: {len(sorted_entities) - multi_variant}")
print()

# Totales
total_garantias = sum(data['total_garantias'] for _, data in sorted_entities)
total_monto = sum(data['monto_total'] for _, data in sorted_entities)
print(f"Total Garantías en el Sistema: {total_garantias:,}")
print(f"Total Monto en el Sistema: S/ {total_monto:,.2f}")
print()

print("=" * 100)

conn.close()
