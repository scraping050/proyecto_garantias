"""
Script para analizar el problema del mapeo de contratos
Verifica cómo se están mapeando los contratos a los awards
"""
import json
from pathlib import Path

data_dir = Path(r"c:\laragon\www\proyecto_garantias\1_database")

# Buscar convocatoria 1001603 que tiene contratos
id_conv = '1001603'

json_files = list(data_dir.glob("*.json"))

for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = data.get('records', data) if 'records' in data else [data]
    
    for record in records:
        compiled = record.get('compiledRelease', {})
        tender = compiled.get('tender', {})
        
        if tender.get('id') == id_conv:
            print("=" * 120)
            print(f"ANALISIS DE MAPEO: Convocatoria {id_conv}")
            print("=" * 120)
            
            # Analizar contracts
            contracts = compiled.get('contracts', [])
            print(f"\n1. CONTRACTS en JSON: {len(contracts)}")
            print("-" * 120)
            
            mapa_contratos = {}
            for i, c in enumerate(contracts, 1):
                aw_id = c.get('awardID')
                c_id = c.get('id')
                print(f"\n  Contrato #{i}:")
                print(f"    Contract ID: {c_id}")
                print(f"    Award ID: {aw_id}")
                
                if aw_id and c_id:
                    # Simular el código del cargador
                    mapa_contratos[str(aw_id)] = c_id
                    print(f"    >>> Agregado al mapa: mapa_contratos['{aw_id}'] = '{c_id}'")
            
            # Analizar awards
            awards = compiled.get('awards', [])
            print(f"\n2. AWARDS en JSON: {len(awards)}")
            print("-" * 120)
            
            for i, aw in enumerate(awards, 1):
                id_adj_raw = aw.get('id')
                print(f"\n  Award #{i}:")
                print(f"    Award ID (id_adj_raw): {id_adj_raw}")
                
                # Simular búsqueda en mapa
                id_contrato = mapa_contratos.get(str(id_adj_raw), None)
                print(f"    Buscando en mapa: mapa_contratos['{id_adj_raw}']")
                print(f"    >>> Resultado: {id_contrato}")
                
                suppliers = aw.get('suppliers', [])
                if suppliers:
                    print(f"    Supplier: {suppliers[0].get('name')}")
                    print(f"    Supplier RUC: {suppliers[0].get('id')}")
            
            # Mostrar mapa completo
            print(f"\n3. MAPA DE CONTRATOS COMPLETO")
            print("-" * 120)
            for award_id, contract_id in mapa_contratos.items():
                print(f"  '{award_id}' -> '{contract_id}'")
            
            # Diagnóstico
            print(f"\n4. DIAGNOSTICO")
            print("-" * 120)
            
            awards_con_contrato = 0
            awards_sin_contrato = 0
            
            for aw in awards:
                id_adj_raw = aw.get('id')
                if mapa_contratos.get(str(id_adj_raw)):
                    awards_con_contrato += 1
                else:
                    awards_sin_contrato += 1
            
            print(f"  Awards CON contrato mapeado: {awards_con_contrato}")
            print(f"  Awards SIN contrato mapeado: {awards_sin_contrato}")
            
            if awards_sin_contrato > 0:
                print(f"\n  PROBLEMA: {awards_sin_contrato} awards no tienen contrato mapeado")
                print(f"  Esto explica por que hay NULL en id_contrato en la BD")
            
            break
    
    if 'encontrado' in locals():
        break

print("\n" + "=" * 120)
print("ANALISIS COMPLETADO")
print("=" * 120)
