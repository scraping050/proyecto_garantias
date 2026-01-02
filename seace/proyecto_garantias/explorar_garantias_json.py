"""
Script para buscar ejemplos de garantías en los JSONs de SEACE
Enfocado en identificar el campo de garantías y entidad financiera
"""
import json
import os
from pathlib import Path

# Directorio de datos
data_dir = Path(r"c:\laragon\www\proyecto_garantias\1_database")

# Buscar un archivo JSON
json_files = list(data_dir.glob("*.json"))
if not json_files:
    print("No se encontraron archivos JSON")
    exit(1)

# Tomar el primer archivo
json_file = json_files[0]
print(f"Analizando: {json_file.name}")
print("=" * 80)

# Leer el archivo
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Obtener registros
records = data.get('records', data) if 'records' in data else [data]

# Buscar el primer registro con información de garantías
contador = 0
for record in records[:100]:  # Revisar los primeros 100 registros
    contador += 1
    
    compiled = record.get('compiledRelease', {})
    tender = compiled.get('tender', {})
    
    # Filtrar solo Licitación Pública
    if tender.get('procurementMethodDetails') != 'Licitación Pública':
        continue
    
    # Buscar información de garantías
    guarantees = tender.get('guarantees', [])
    contracts = compiled.get('contracts', [])
    awards = compiled.get('awards', [])
    
    if guarantees or contracts:
        print(f"\n{'='*80}")
        print(f"REGISTRO #{contador}")
        print(f"ID Convocatoria: {tender.get('id')}")
        print(f"Estado Tender: {tender.get('status')}")
        print(f"{'='*80}")
        
        # Mostrar guarantees
        if guarantees:
            print("\n--- GUARANTEES (Garantías) ---")
            for i, g in enumerate(guarantees, 1):
                print(f"\nGarantía #{i}:")
                print(json.dumps(g, indent=2, ensure_ascii=False))
        
        # Mostrar contracts
        if contracts:
            print("\n--- CONTRACTS (Contratos) ---")
            for i, c in enumerate(contracts[:2], 1):  # Solo primeros 2
                print(f"\nContrato #{i}:")
                print(f"  ID: {c.get('id')}")
                print(f"  Award ID: {c.get('awardID')}")
                print(f"  Status: {c.get('status')}")
                
                # Buscar información de garantías en el contrato
                if 'guarantees' in c:
                    print(f"  Guarantees en contrato:")
                    print(json.dumps(c.get('guarantees'), indent=4, ensure_ascii=False))
        
        # Mostrar awards
        if awards:
            print("\n--- AWARDS (Adjudicaciones) ---")
            for i, a in enumerate(awards[:2], 1):
                print(f"\nAdjudicación #{i}:")
                print(f"  ID: {a.get('id')}")
                print(f"  Status: {a.get('status')}")
                
                # Buscar suppliers
                suppliers = a.get('suppliers', [])
                if suppliers:
                    print(f"  Proveedor: {suppliers[0].get('name')}")
        
        # Solo mostrar los primeros 3 ejemplos
        if contador >= 3:
            break

print("\n" + "=" * 80)
print("BÚSQUEDA COMPLETADA")
print("=" * 80)
