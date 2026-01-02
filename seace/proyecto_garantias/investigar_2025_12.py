"""
Script para investigar por qué 2025-12 cargó 0 licitaciones
"""
import json
from pathlib import Path

data_dir = Path(r"c:\laragon\www\proyecto_garantias\1_database")
archivo = data_dir / "2025-12_seace_v3.json"

print("=" * 120)
print(f"INVESTIGACION: {archivo.name}")
print("=" * 120)

with open(archivo, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Obtener registros
records = data.get('records', data) if 'records' in data else [data]

print(f"\nTotal registros en JSON: {len(records) if isinstance(records, list) else 1}")

# Analizar primeros 10 registros
print("\nAnalizando primeros 10 registros:")
print("-" * 120)

contador_lp = 0
contador_otros = 0
tipos_encontrados = {}

for i, record in enumerate(records[:50], 1):
    compiled = record.get('compiledRelease', {})
    tender = compiled.get('tender', {})
    
    tipo_proc = tender.get('procurementMethodDetails')
    ocid = record.get('ocid', 'N/A')
    id_conv = tender.get('id', 'N/A')
    
    # Contar tipos
    if tipo_proc not in tipos_encontrados:
        tipos_encontrados[tipo_proc] = 0
    tipos_encontrados[tipo_proc] += 1
    
    if tipo_proc == 'Licitación Pública':
        contador_lp += 1
        if contador_lp <= 5:
            print(f"\n{i}. LICITACION PUBLICA ENCONTRADA:")
            print(f"   OCID: {ocid}")
            print(f"   ID Convocatoria: {id_conv}")
            print(f"   Tipo: {tipo_proc}")
            print(f"   Título: {tender.get('title', 'N/A')[:60]}...")
    else:
        contador_otros += 1

print(f"\n{'='*120}")
print("RESUMEN DE TIPOS DE PROCEDIMIENTO:")
print("-" * 120)
for tipo, count in sorted(tipos_encontrados.items(), key=lambda x: x[1], reverse=True):
    print(f"{tipo or 'NULL':50} | Total: {count}")

print(f"\n{'='*120}")
print(f"LICITACIONES PUBLICAS en primeros 50: {contador_lp}")
print(f"OTROS TIPOS en primeros 50: {contador_otros}")
print(f"{'='*120}")

# Analizar TODO el archivo
print("\nAnalizando TODO el archivo...")
total_lp = 0
total_otros = 0
todos_tipos = {}

for record in records:
    compiled = record.get('compiledRelease', {})
    tender = compiled.get('tender', {})
    tipo_proc = tender.get('procurementMethodDetails')
    
    if tipo_proc not in todos_tipos:
        todos_tipos[tipo_proc] = 0
    todos_tipos[tipo_proc] += 1
    
    if tipo_proc == 'Licitación Pública':
        total_lp += 1
    else:
        total_otros += 1

print(f"\nRESULTADO COMPLETO:")
print("-" * 120)
for tipo, count in sorted(todos_tipos.items(), key=lambda x: x[1], reverse=True):
    print(f"{tipo or 'NULL':50} | Total: {count}")

print(f"\n{'='*120}")
print(f"TOTAL LICITACIONES PUBLICAS: {total_lp}")
print(f"TOTAL OTROS TIPOS: {total_otros}")
print(f"TOTAL REGISTROS: {len(records)}")
print(f"{'='*120}")

if total_lp > 0:
    print(f"\n⚠️ PROBLEMA IDENTIFICADO:")
    print(f"   El archivo SÍ tiene {total_lp} Licitaciones Públicas")
    print(f"   Pero el ETL cargó 0")
    print(f"   >>> Hay un BUG en el ETL <<<")
else:
    print(f"\n✅ El archivo realmente NO tiene Licitaciones Públicas")
