"""
Script para analizar el campo de estado en los JSON de SEACE
"""
import json
import sys
from collections import Counter

# Configurar encoding UTF-8
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analizar_estados_json(archivo):
    """Analiza los estados en un archivo JSON"""
    print(f"\n{'='*80}")
    print(f"ANÁLISIS DE ESTADOS EN: {archivo}")
    print(f"{'='*80}\n")
    
    with open(archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = data.get('records', data)
    
    tender_statuses = []
    item_statuses = []
    
    for i, rec in enumerate(records[:10]):  # Primeros 10 registros
        compiled = rec.get('compiledRelease', {})
        tender = compiled.get('tender', {})
        
        # Verificar tipo de procedimiento
        tipo_proc = tender.get('procurementMethodDetails')
        if tipo_proc != 'Licitación Pública':
            continue
        
        tender_status = tender.get('status')
        tender_id = tender.get('id')
        
        print(f"\n--- Registro {i+1} ---")
        print(f"  Tender ID: {tender_id}")
        print(f"  tender.status: {tender_status}")
        print(f"  Tender keys disponibles: {list(tender.keys())}")
        
        # Verificar awards
        awards = compiled.get('awards', [])
        if awards:
            print(f"  Awards encontrados: {len(awards)}")
            for j, aw in enumerate(awards[:2]):
                items = aw.get('items', [])
                if items:
                    status_details = items[0].get('statusDetails')
                    print(f"    Award {j+1} - items[0].statusDetails: {status_details}")
                    item_statuses.append(status_details)
        
        tender_statuses.append(tender_status)
    
    print(f"\n{'='*80}")
    print("RESUMEN:")
    print(f"{'='*80}")
    print(f"\nTender statuses encontrados:")
    print(Counter(tender_statuses))
    print(f"\nItem statusDetails encontrados:")
    print(Counter(item_statuses))

if __name__ == "__main__":
    analizar_estados_json('1_database/2024-01_seace_v3.json')
