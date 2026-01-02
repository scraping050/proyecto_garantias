"""
Análisis COMPLETO de Entidades Financieras
Datos EXACTOS de la base de datos
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from secrets_manager import get_db_config
import mysql.connector

print("=" * 100)
print("📊 ANÁLISIS EXHAUSTIVO DE ENTIDADES FINANCIERAS")
print("=" * 100)
print()

# Conectar a BD
DB_CONFIG = get_db_config()
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Query completo con todos los datos
query = """
SELECT 
    a.entidad_financiera,
    COUNT(*) as total_garantias,
    COALESCE(SUM(a.monto_adjudicado), 0) as monto_total,
    COUNT(DISTINCT c.departamento) as departamentos_atendidos,
    COUNT(DISTINCT c.provincia) as provincias_atendidas,
    COUNT(DISTINCT c.distrito) as distritos_atendidos,
    COUNT(DISTINCT c.categoria) as categorias_atendidas
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

print(f"Total de entidades encontradas: {len(results)}")
print()
print("=" * 100)
print()

# Función para determinar cobertura
def get_cobertura(departamentos, provincias, distritos):
    if departamentos >= 24:
        return "NACIONAL", "🟢"
    elif departamentos >= 15:
        return "REGIONAL", "🔵"
    elif departamentos >= 5:
        return "MULTI-DEPARTAMENTAL", "🟡"
    elif provincias >= 5:
        return "PROVINCIAL", "🟠"
    else:
        return "LOCAL", "⚪"

# Procesar y mostrar resultados
total_garantias_sistema = 0
total_monto_sistema = 0

for idx, row in enumerate(results, 1):
    entidad = row[0]
    garantias = row[1]
    monto = float(row[2])
    departamentos = row[3]
    provincias = row[4]
    distritos = row[5]
    categorias = row[6]
    
    cobertura, emoji = get_cobertura(departamentos, provincias, distritos)
    
    total_garantias_sistema += garantias
    total_monto_sistema += monto
    
    print(f"[{idx}] {entidad}")
    print(f"    ├─ Garantías/Licitaciones: {garantias:,}")
    print(f"    ├─ Monto Total: S/ {monto:,.2f}")
    print(f"    ├─ Departamentos: {departamentos}")
    print(f"    ├─ Provincias: {provincias}")
    print(f"    ├─ Distritos: {distritos}")
    print(f"    ├─ Categorías: {categorias}")
    print(f"    └─ Cobertura: {emoji} {cobertura}")
    print()

print("=" * 100)
print("📈 RESUMEN GENERAL")
print("=" * 100)
print(f"Total Entidades: {len(results)}")
print(f"Total Garantías en el Sistema: {total_garantias_sistema:,}")
print(f"Total Monto en el Sistema: S/ {total_monto_sistema:,.2f}")
print(f"Promedio Garantías por Entidad: {total_garantias_sistema / len(results):.1f}")
print(f"Promedio Monto por Entidad: S/ {total_monto_sistema / len(results):,.2f}")
print()

# Clasificación por cobertura
print("=" * 100)
print("📊 CLASIFICACIÓN POR COBERTURA")
print("=" * 100)

cobertura_count = {
    "NACIONAL": 0,
    "REGIONAL": 0,
    "MULTI-DEPARTAMENTAL": 0,
    "PROVINCIAL": 0,
    "LOCAL": 0
}

for row in results:
    departamentos = row[3]
    provincias = row[4]
    distritos = row[5]
    cobertura, _ = get_cobertura(departamentos, provincias, distritos)
    cobertura_count[cobertura] += 1

for cob, count in cobertura_count.items():
    porcentaje = (count / len(results)) * 100
    print(f"{cob}: {count} entidades ({porcentaje:.1f}%)")

print()
print("=" * 100)

conn.close()
