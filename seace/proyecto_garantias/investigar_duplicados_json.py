"""
Investiga los 106 registros duplicados en JSON que no se cargan a BD
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

def encontrar_duplicados():
    """Encuentra IDs duplicados en JSONs"""
    ids_counter = Counter()
    ids_por_archivo = {}
    
    archivos = sorted([f for f in os.listdir(db_folder) if f.endswith('.json')])
    
    print("="*80)
    print("BUSCANDO DUPLICADOS EN JSONs")
    print("="*80)
    
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
                    id_conv = tender.get('id')
                    if id_conv:
                        id_str = str(id_conv)
                        ids_counter[id_str] += 1
                        
                        if id_str not in ids_por_archivo:
                            ids_por_archivo[id_str] = []
                        ids_por_archivo[id_str].append(archivo)
                        
        except Exception as e:
            print(f"ERROR en {archivo}: {e}")
    
    # Encontrar duplicados
    duplicados = {id_conv: count for id_conv, count in ids_counter.items() if count > 1}
    
    print(f"\nTotal de IDs únicos: {len(ids_counter):,}")
    print(f"IDs duplicados: {len(duplicados):,}")
    print(f"Total de registros: {sum(ids_counter.values()):,}")
    print(f"Registros duplicados: {sum(count - 1 for count in duplicados.values()):,}")
    
    if duplicados:
        print("\n" + "="*80)
        print(f"PRIMEROS 20 IDs DUPLICADOS")
        print("="*80)
        
        for i, (id_conv, count) in enumerate(sorted(duplicados.items(), key=lambda x: -x[1])[:20], 1):
            archivos_dup = ids_por_archivo[id_conv]
            print(f"\n{i:2}. ID: {id_conv} (aparece {count} veces)")
            print(f"    Archivos: {', '.join(archivos_dup)}")
    
    return duplicados, ids_por_archivo

if __name__ == "__main__":
    encontrar_duplicados()
