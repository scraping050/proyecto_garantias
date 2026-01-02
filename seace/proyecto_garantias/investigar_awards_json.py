import json
import os

db_folder = os.path.join(os.path.dirname(__file__), "1_database")
archivo = os.path.join(db_folder, "2024-01_seace_v3.json")

with open(archivo, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 100)
print(" INVESTIGACION: Campos disponibles en awards")
print("=" * 100)

# Analizar primeros 10 awards
count = 0
for r in data.get('records', []):
    compiled = r.get('compiledRelease', {})
    tender = compiled.get('tender', {})
    
    if tender.get('procurementMethodDetails') == 'Licitación Pública':
        for aw in compiled.get('awards', []):
            if count >= 3:
                break
            
            print(f"\nAward #{count + 1}:")
            print(f"  ID: {aw.get('id')}")
            print(f"  Campos disponibles: {list(aw.keys())}")
            print(f"  status: {aw.get('status')}")
            print(f"  statusDetails: {aw.get('statusDetails')}")
            
            # Ver si hay status en suppliers
            sups = aw.get('suppliers', [])
            if sups:
                print(f"  supplier[0] keys: {list(sups[0].keys())}")
            
            count += 1
        
        if count >= 3:
            break

print("\n" + "=" * 100)
