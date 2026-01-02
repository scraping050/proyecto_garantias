"""
Script para identificar TODOS los tipos de Licitacion Publica en SEACE
"""
import json
from pathlib import Path
from collections import defaultdict

data_dir = Path(r"c:\laragon\www\proyecto_garantias\1_database")
json_files = list(data_dir.glob("*.json"))

print("=" * 120)
print("ANALISIS: Todos los tipos de procedimiento en SEACE")
print("=" * 120)

todos_tipos = defaultdict(int)
tipos_licitacion_publica = defaultdict(int)

for json_file in json_files:
    print(f"\nProcesando: {json_file.name}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = data.get('records', data) if 'records' in data else [data]
    
    for record in records:
        compiled = record.get('compiledRelease', {})
        tender = compiled.get('tender', {})
        tipo_proc = tender.get('procurementMethodDetails')
        
        if tipo_proc:
            todos_tipos[tipo_proc] += 1
            
            # Identificar variantes de Licitacion Publica
            if 'licitaci' in tipo_proc.lower() and 'p' in tipo_proc.lower():
                tipos_licitacion_publica[tipo_proc] += 1

print("\n" + "=" * 120)
print("TODOS LOS TIPOS DE PROCEDIMIENTO ENCONTRADOS:")
print("-" * 120)
for tipo, count in sorted(todos_tipos.items(), key=lambda x: x[1], reverse=True):
    print(f"{tipo:60} | Total: {count:6}")

print("\n" + "=" * 120)
print("TIPOS QUE CONTIENEN 'LICITACION' Y 'PUBLICA':")
print("-" * 120)
for tipo, count in sorted(tipos_licitacion_publica.items(), key=lambda x: x[1], reverse=True):
    es_exacto = " <<<< ACTUAL FILTRO" if tipo == "Licitacion Publica" else ""
    print(f"{tipo:60} | Total: {count:6}{es_exacto}")

print("\n" + "=" * 120)
print("RECOMENDACION:")
print("-" * 120)
print("El ETL actual solo filtra: 'Licitacion Publica' (exacto)")
print("Pero existen variantes que tambien son Licitaciones Publicas")
print("\nSolucion: Modificar filtro para incluir TODAS las variantes")
print("=" * 120)
