"""
Investigacion exhaustiva del estado_item en JSONs
Busca TODOS los posibles campos de estado en awards
"""
import json
import os
from collections import Counter

db_folder = os.path.join(os.path.dirname(__file__), "1_database")
archivo = os.path.join(db_folder, "2024-01_seace_v3.json")

print("=" * 100)
print(" INVESTIGACION: Estado real de awards en JSON")
print("=" * 100)

with open(archivo, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Analizar estructura completa de awards
print("\n1. ESTRUCTURA COMPLETA DE UN AWARD:")
print("-" * 100)

for r in data.get('records', [])[:1]:
    compiled = r.get('compiledRelease', {})
    tender = compiled.get('tender', {})
    
    if tender.get('procurementMethodDetails') == 'Licitación Pública':
        awards = compiled.get('awards', [])
        if awards:
            award = awards[0]
            print(f"\nCampos disponibles en award:")
            for key in award.keys():
                print(f"  - {key}: {type(award[key]).__name__}")
            
            print(f"\nContenido completo del primer award:")
            print(json.dumps(award, indent=2, ensure_ascii=False)[:1000])
            break

# Buscar todos los campos posibles de estado
print("\n\n2. BUSCANDO CAMPOS DE ESTADO EN AWARDS:")
print("-" * 100)

campos_estado = Counter()
valores_status = Counter()
valores_statusDetails = Counter()

count = 0
for r in data.get('records', []):
    compiled = r.get('compiledRelease', {})
    tender = compiled.get('tender', {})
    
    if tender.get('procurementMethodDetails') == 'Licitación Pública':
        for aw in compiled.get('awards', []):
            count += 1
            
            # Buscar todos los campos que contengan "status"
            for key in aw.keys():
                if 'status' in key.lower():
                    campos_estado[key] += 1
                    
                    # Guardar valores
                    if key == 'status':
                        val = aw.get(key)
                        if val:
                            valores_status[val] += 1
                    elif key == 'statusDetails':
                        val = aw.get(key)
                        if val:
                            valores_statusDetails[val] += 1

print(f"\nTotal awards analizados: {count}")
print(f"\nCampos relacionados con 'status' encontrados:")
for campo, cantidad in campos_estado.most_common():
    print(f"  - {campo}: {cantidad} veces")

if valores_status:
    print(f"\nValores de 'status':")
    for valor, cantidad in valores_status.most_common():
        print(f"  - {valor}: {cantidad}")
else:
    print(f"\nNO SE ENCONTRO campo 'status' en awards")

if valores_statusDetails:
    print(f"\nValores de 'statusDetails':")
    for valor, cantidad in valores_statusDetails.most_common():
        print(f"  - {valor}: {cantidad}")
else:
    print(f"\nNO SE ENCONTRO campo 'statusDetails' en awards")

# Buscar en items
print("\n\n3. BUSCANDO ESTADO EN ITEMS:")
print("-" * 100)

items_status = Counter()
items_statusDetails = Counter()

for r in data.get('records', []):
    compiled = r.get('compiledRelease', {})
    tender = compiled.get('tender', {})
    
    if tender.get('procurementMethodDetails') == 'Licitación Pública':
        for aw in compiled.get('awards', []):
            items = aw.get('items', [])
            for item in items:
                if 'status' in item:
                    items_status[item['status']] += 1
                if 'statusDetails' in item:
                    items_statusDetails[item['statusDetails']] += 1

if items_status:
    print(f"\nValores de 'status' en items:")
    for valor, cantidad in items_status.most_common():
        print(f"  - {valor}: {cantidad}")
else:
    print(f"\nNO SE ENCONTRO 'status' en items")

if items_statusDetails:
    print(f"\nValores de 'statusDetails' en items:")
    for valor, cantidad in items_statusDetails.most_common():
        print(f"  - {valor}: {cantidad}")
else:
    print(f"\nNO SE ENCONTRO 'statusDetails' en items")

# Buscar en tender
print("\n\n4. ESTADO EN TENDER (proceso completo):")
print("-" * 100)

tender_status = Counter()

for r in data.get('records', []):
    compiled = r.get('compiledRelease', {})
    tender = compiled.get('tender', {})
    
    if tender.get('procurementMethodDetails') == 'Licitación Pública':
        status = tender.get('status')
        if status:
            tender_status[status] += 1

if tender_status:
    print(f"\nValores de tender.status:")
    for valor, cantidad in tender_status.most_common():
        print(f"  - {valor}: {cantidad}")

print("\n" + "=" * 100)
print(" CONCLUSION")
print("=" * 100)

if valores_status:
    print("\nOPCION 1: Usar award.status")
    print(f"  Disponible en: {sum(valores_status.values())} awards")
elif items_statusDetails:
    print("\nOPCION 2: Usar items[0].statusDetails")
    print(f"  Disponible en: {sum(items_statusDetails.values())} items")
elif tender_status:
    print("\nOPCION 3: Usar tender.status (estado del proceso completo)")
    print(f"  Disponible en: {sum(tender_status.values())} tenders")
else:
    print("\nNO HAY CAMPO DE ESTADO DISPONIBLE en awards")
    print("Mantener 'DESCONOCIDO' es correcto")

print("=" * 100)
