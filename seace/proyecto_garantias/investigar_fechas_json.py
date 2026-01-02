"""
Investigar el campo 'date' en los JSONs para entender el problema de fechas
"""
import json
import os
import sys
from collections import Counter

# Fix encoding
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

parent_dir = os.path.dirname(os.path.abspath(__file__))
db_folder = os.path.join(parent_dir, "1_database")

def investigar_fechas():
    """Investiga las fechas en los JSONs"""
    
    print("=" * 100)
    print(" INVESTIGACIÓN DE FECHAS EN JSONs")
    print("=" * 100)
    
    # Analizar algunos archivos
    archivos_muestra = [
        "2024-01_seace_v3.json",
        "2024-06_seace_v3.json",
        "2024-12_seace_v3.json",
        "2025-01_seace_v3.json",
        "2025-06_seace_v3.json",
        "2025-12_seace_v3.json"
    ]
    
    for archivo in archivos_muestra:
        ruta = os.path.join(db_folder, archivo)
        if not os.path.exists(ruta):
            continue
            
        print(f"\n{'='*100}")
        print(f" ARCHIVO: {archivo}")
        print(f"{'='*100}")
        
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        records = data.get('records', [])
        if not records:
            print("  ⚠️ No hay records")
            continue
        
        # Analizar primeros 5 registros
        print(f"\n  Analizando primeros 5 registros de Licitación Pública:")
        
        count = 0
        for i, r in enumerate(records):
            compiled = r.get('compiledRelease', {})
            tender = compiled.get('tender', {})
            
            if tender.get('procurementMethodDetails') != 'Licitación Pública':
                continue
            
            count += 1
            if count > 5:
                break
            
            # Extraer todas las fechas posibles
            r_date = r.get('date')
            compiled_date = compiled.get('date')
            tender_period = tender.get('tenderPeriod', {})
            tender_start = tender_period.get('startDate')
            tender_end = tender_period.get('endDate')
            
            print(f"\n  Registro {count}:")
            print(f"    r.get('date'):              {r_date}")
            print(f"    compiled.get('date'):       {compiled_date}")
            print(f"    tender.tenderPeriod.start:  {tender_start}")
            print(f"    tender.tenderPeriod.end:    {tender_end}")
            
            # Mostrar año de cada fecha
            if compiled_date:
                año_compiled = compiled_date[:4]
                print(f"    → AÑO en compiled.date:     {año_compiled}")
            if tender_start:
                año_start = tender_start[:4]
                print(f"    → AÑO en tenderPeriod.start: {año_start}")
    
    # Estadísticas generales
    print(f"\n{'='*100}")
    print(" ESTADÍSTICAS GENERALES")
    print(f"{'='*100}")
    
    for archivo in ["2024-01_seace_v3.json", "2025-01_seace_v3.json"]:
        ruta = os.path.join(db_folder, archivo)
        if not os.path.exists(ruta):
            continue
        
        print(f"\n  {archivo}:")
        
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        records = data.get('records', [])
        años_compiled = []
        años_tender = []
        
        for r in records:
            compiled = r.get('compiledRelease', {})
            tender = compiled.get('tender', {})
            
            if tender.get('procurementMethodDetails') != 'Licitación Pública':
                continue
            
            compiled_date = compiled.get('date')
            tender_period = tender.get('tenderPeriod', {})
            tender_start = tender_period.get('startDate')
            
            if compiled_date:
                años_compiled.append(compiled_date[:4])
            if tender_start:
                años_tender.append(tender_start[:4])
        
        print(f"    Años en compiled.date:")
        for año, count in Counter(años_compiled).most_common():
            print(f"      {año}: {count:>4} registros")
        
        print(f"    Años en tenderPeriod.startDate:")
        for año, count in Counter(años_tender).most_common():
            print(f"      {año}: {count:>4} registros")

if __name__ == "__main__":
    investigar_fechas()
