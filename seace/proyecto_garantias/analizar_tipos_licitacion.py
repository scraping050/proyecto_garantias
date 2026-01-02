"""
Analiza todos los tipos de procurementMethodDetails en los JSONs
para identificar todas las variantes de Licitacion Publica
"""
import json
import os
import sys
from collections import Counter

# Fix encoding for Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

parent_dir = os.path.dirname(os.path.abspath(__file__))
db_folder = os.path.join(parent_dir, "1_database")

def analizar_tipos():
    tipos_counter = Counter()
    total_records = 0
    
    archivos = sorted([f for f in os.listdir(db_folder) if f.endswith('.json')])
    
    for archivo in archivos:
        print(f"\nAnalizando: {archivo}")
        ruta = os.path.join(db_folder, archivo)
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            records = data.get('records', data if isinstance(data, list) else [])
            
            for r in records:
                total_records += 1
                compiled = r.get('compiledRelease', {})
                tender = compiled.get('tender', {})
                tipo = tender.get('procurementMethodDetails')
                
                if tipo:
                    tipos_counter[tipo] += 1
            
            print(f"   OK - {len(records)} registros procesados")
            
        except Exception as e:
            print(f"   ERROR: {e}")
    
    print(f"\n{'='*80}")
    print(f"RESUMEN DE TIPOS DE PROCEDIMIENTO")
    print(f"{'='*80}")
    print(f"Total de registros analizados: {total_records:,}")
    print(f"\nTipos encontrados ({len(tipos_counter)}):\n")
    
    # Ordenar por cantidad descendente
    for tipo, cantidad in tipos_counter.most_common():
        porcentaje = (cantidad / total_records * 100) if total_records > 0 else 0
        marca = "[LP]" if "Licitación Pública" in tipo or "Licitacion Publica" in tipo else "    "
        print(f"{marca} {tipo:50} | {cantidad:6,} ({porcentaje:5.2f}%)")
    
    print(f"\n{'='*80}")
    print(f"TIPOS QUE CONTIENEN 'Licitacion Publica':")
    print(f"{'='*80}")
    
    lp_total = 0
    for tipo, cantidad in tipos_counter.items():
        if "Licitación Pública" in tipo or "Licitacion Publica" in tipo:
            porcentaje = (cantidad / total_records * 100) if total_records > 0 else 0
            print(f"   {tipo:50} | {cantidad:6,} ({porcentaje:5.2f}%)")
            lp_total += cantidad
    
    porcentaje_lp = (lp_total / total_records * 100) if total_records > 0 else 0
    print(f"\n   {'TOTAL LICITACION PUBLICA':50} | {lp_total:6,} ({porcentaje_lp:5.2f}%)")

if __name__ == "__main__":
    analizar_tipos()
