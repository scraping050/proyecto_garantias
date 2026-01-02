"""
Script para investigar si los datos NULL existen en el JSON original
Busca casos específicos en los archivos JSON de SEACE
"""
import json
import os
from pathlib import Path

# Directorio de datos
data_dir = Path(r"c:\laragon\www\proyecto_garantias\1_database")

# IDs de ejemplo que tienen id_contrato NULL
ids_investigar = [
    '1000059',  # CONSENTIDO
    '1001070',  # CONSENTIDO
    '1001603',  # CONTRATADO (crítico - debería tener contrato)
]

print("=" * 120)
print("INVESTIGACION: Datos NULL en JSON de SEACE")
print("=" * 120)

# Buscar en archivos JSON
json_files = list(data_dir.glob("*.json"))

for id_conv in ids_investigar:
    print(f"\n{'='*120}")
    print(f"INVESTIGANDO: ID Convocatoria {id_conv}")
    print(f"{'='*120}")
    
    encontrado = False
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        records = data.get('records', data) if 'records' in data else [data]
        
        for record in records:
            compiled = record.get('compiledRelease', {})
            tender = compiled.get('tender', {})
            
            if tender.get('id') == id_conv:
                encontrado = True
                print(f"\nEncontrado en: {json_file.name}")
                print(f"Estado tender: {tender.get('status')}")
                
                # Verificar contracts
                contracts = compiled.get('contracts', [])
                print(f"\nContracts encontrados: {len(contracts)}")
                
                if contracts:
                    for i, contract in enumerate(contracts, 1):
                        print(f"\n  Contrato #{i}:")
                        print(f"    ID: {contract.get('id')}")
                        print(f"    Award ID: {contract.get('awardID')}")
                        print(f"    Status: {contract.get('status')}")
                        print(f"    Date: {contract.get('dateSigned')}")
                else:
                    print("  >>> NO HAY CONTRATOS EN EL JSON <<<")
                
                # Verificar awards
                awards = compiled.get('awards', [])
                print(f"\nAwards encontrados: {len(awards)}")
                
                if awards:
                    for i, award in enumerate(awards[:3], 1):  # Solo primeros 3
                        print(f"\n  Award #{i}:")
                        print(f"    ID: {award.get('id')}")
                        print(f"    Status: {award.get('status')}")
                        
                        suppliers = award.get('suppliers', [])
                        if suppliers:
                            print(f"    Supplier: {suppliers[0].get('name')}")
                            print(f"    Supplier ID (RUC): {suppliers[0].get('id')}")
                        
                        # Verificar si hay contractID
                        contract_id = award.get('contractID')
                        print(f"    ContractID en award: {contract_id}")
                
                break
        
        if encontrado:
            break
    
    if not encontrado:
        print(f"  >>> NO ENCONTRADO en los archivos JSON <<<")

print("\n" + "=" * 120)
print("INVESTIGACION COMPLETADA")
print("=" * 120)
