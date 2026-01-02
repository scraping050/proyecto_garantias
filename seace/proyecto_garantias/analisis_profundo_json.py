"""
Análisis PROFUNDO de JSONs para encontrar TODOS los registros
Verifica diferentes estructuras y paths en el JSON
"""
import json
import os
import sys
from collections import defaultdict

# Fix encoding
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

parent_dir = os.path.dirname(os.path.abspath(__file__))
db_folder = os.path.join(parent_dir, "1_database")

def analizar_estructura_json(archivo_path):
    """Analiza la estructura completa de un JSON"""
    with open(archivo_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Verificar diferentes estructuras posibles
    estructuras = {
        'records': 0,
        'releases': 0,
        'compiledReleases': 0,
        'root_list': 0
    }
    
    # Opción 1: data['records']
    if 'records' in data:
        estructuras['records'] = len(data['records'])
    
    # Opción 2: data['releases']
    if 'releases' in data:
        estructuras['releases'] = len(data['releases'])
    
    # Opción 3: data['compiledReleases']
    if 'compiledReleases' in data:
        estructuras['compiledReleases'] = len(data['compiledReleases'])
    
    # Opción 4: data es una lista directamente
    if isinstance(data, list):
        estructuras['root_list'] = len(data)
    
    return estructuras, data

def contar_todos_los_paths():
    """Cuenta registros en TODOS los paths posibles"""
    archivos = sorted([f for f in os.listdir(db_folder) if f.endswith('.json')])
    
    total_por_path = defaultdict(int)
    ids_por_path = defaultdict(set)
    
    print("="*80)
    print("ANÁLISIS PROFUNDO DE ESTRUCTURA JSON")
    print("="*80)
    
    for archivo in archivos:
        ruta = os.path.join(db_folder, archivo)
        
        try:
            estructuras, data = analizar_estructura_json(ruta)
            
            # Analizar cada estructura
            for estructura, count in estructuras.items():
                if count > 0:
                    print(f"\n{archivo}")
                    print(f"  Estructura '{estructura}': {count} elementos")
                    
                    # Contar Licitación Pública en cada estructura
                    lp_count = 0
                    
                    if estructura == 'records':
                        for r in data['records']:
                            compiled = r.get('compiledRelease', {})
                            tender = compiled.get('tender', {})
                            tipo = tender.get('procurementMethodDetails')
                            if tipo == 'Licitación Pública':
                                lp_count += 1
                                id_conv = tender.get('id')
                                if id_conv:
                                    ids_por_path[estructura].add(str(id_conv))
                    
                    elif estructura == 'releases':
                        for r in data['releases']:
                            tender = r.get('tender', {})
                            tipo = tender.get('procurementMethodDetails')
                            if tipo == 'Licitación Pública':
                                lp_count += 1
                                id_conv = tender.get('id')
                                if id_conv:
                                    ids_por_path[estructura].add(str(id_conv))
                    
                    elif estructura == 'compiledReleases':
                        for r in data['compiledReleases']:
                            tender = r.get('tender', {})
                            tipo = tender.get('procurementMethodDetails')
                            if tipo == 'Licitación Pública':
                                lp_count += 1
                                id_conv = tender.get('id')
                                if id_conv:
                                    ids_por_path[estructura].add(str(id_conv))
                    
                    elif estructura == 'root_list':
                        for r in data:
                            compiled = r.get('compiledRelease', {})
                            tender = compiled.get('tender', {})
                            tipo = tender.get('procurementMethodDetails')
                            if tipo == 'Licitación Pública':
                                lp_count += 1
                                id_conv = tender.get('id')
                                if id_conv:
                                    ids_por_path[estructura].add(str(id_conv))
                    
                    if lp_count > 0:
                        print(f"  -> Licitación Pública: {lp_count}")
                        total_por_path[estructura] += lp_count
                        
        except Exception as e:
            print(f"\nERROR en {archivo}: {e}")
    
    print("\n" + "="*80)
    print("RESUMEN POR ESTRUCTURA")
    print("="*80)
    
    for estructura, total in total_por_path.items():
        ids_unicos = len(ids_por_path[estructura])
        print(f"{estructura:20} | Total: {total:6,} | IDs únicos: {ids_unicos:6,}")
    
    # Total combinado
    todos_ids = set()
    for ids in ids_por_path.values():
        todos_ids.update(ids)
    
    print("\n" + "="*80)
    print(f"TOTAL COMBINADO: {sum(total_por_path.values()):,} registros")
    print(f"IDs ÚNICOS TOTALES: {len(todos_ids):,}")
    print("="*80)

def analizar_ocid_vs_id():
    """Verifica si hay diferencia entre OCID y tender.id"""
    archivos = sorted([f for f in os.listdir(db_folder) if f.endswith('.json')])
    
    print("\n" + "="*80)
    print("ANÁLISIS: OCID vs tender.id")
    print("="*80)
    
    total_ocid = set()
    total_tender_id = set()
    diferentes = []
    
    for archivo in archivos:
        ruta = os.path.join(db_folder, archivo)
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            records = data.get('records', data if isinstance(data, list) else [])
            
            for r in records:
                compiled = r.get('compiledRelease', {})
                tender = compiled.get('tender', {})
                tipo = tender.get('procurementMethodDetails')
                
                if tipo == 'Licitación Pública':
                    ocid = r.get('ocid')
                    tender_id = tender.get('id')
                    
                    if ocid:
                        total_ocid.add(str(ocid))
                    if tender_id:
                        total_tender_id.add(str(tender_id))
                    
                    if ocid and tender_id and str(ocid) != str(tender_id):
                        diferentes.append((ocid, tender_id))
                        
        except Exception as e:
            print(f"ERROR en {archivo}: {e}")
    
    print(f"\nTotal OCID únicos: {len(total_ocid):,}")
    print(f"Total tender.id únicos: {len(total_tender_id):,}")
    print(f"Registros donde OCID != tender.id: {len(diferentes)}")
    
    if diferentes:
        print("\nPrimeros 5 ejemplos de diferencias:")
        for i, (ocid, tid) in enumerate(diferentes[:5], 1):
            print(f"  {i}. OCID: {ocid} | tender.id: {tid}")

if __name__ == "__main__":
    print("INICIANDO ANÁLISIS PROFUNDO...")
    contar_todos_los_paths()
    analizar_ocid_vs_id()
