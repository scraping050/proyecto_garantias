"""
Contar registros DIRECTAMENTE en los JSONs y comparar con BD
Para identificar exactamente dónde está la diferencia
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

def contar_en_json():
    """Cuenta Licitación Pública directamente en JSONs"""
    
    print("=" * 100)
    print(" CONTEO DIRECTO EN ARCHIVOS JSON")
    print("=" * 100)
    
    archivos = sorted([f for f in os.listdir(db_folder) if f.endswith('.json')])
    
    conteo_por_archivo = {}
    conteo_por_mes_2024 = defaultdict(int)
    conteo_por_mes_2025 = defaultdict(int)
    
    for archivo in archivos:
        ruta = os.path.join(db_folder, archivo)
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            records = data.get('records', [])
            count = 0
            
            for r in records:
                compiled = r.get('compiledRelease', {})
                tender = compiled.get('tender', {})
                
                # Mismo filtro que usa el cargador
                if tender.get('procurementMethodDetails') == 'Licitación Pública':
                    count += 1
                    
                    # Contar por mes usando tenderPeriod.startDate
                    tender_period = tender.get('tenderPeriod', {})
                    fecha = tender_period.get('startDate', '')
                    
                    if fecha:
                        año_mes = fecha[:7]  # YYYY-MM
                        año = int(fecha[:4])
                        mes = int(fecha[5:7])
                        
                        if año == 2024:
                            conteo_por_mes_2024[mes] += 1
                        elif año == 2025:
                            conteo_por_mes_2025[mes] += 1
            
            conteo_por_archivo[archivo] = count
            print(f"  {archivo:30} | {count:>6,} Licitaciones Públicas")
            
        except Exception as e:
            print(f"  ERROR en {archivo}: {e}")
    
    # Totales
    total_2024 = sum(conteo_por_mes_2024.values())
    total_2025 = sum(conteo_por_mes_2025.values())
    total_general = total_2024 + total_2025
    
    print(f"\n{'='*100}")
    print(" TOTALES POR AÑO")
    print(f"{'='*100}")
    print(f"  2024: {total_2024:>6,}")
    print(f"  2025: {total_2025:>6,}")
    print(f"  TOTAL: {total_general:>6,}")
    
    # Comparar con OECE
    print(f"\n{'='*100}")
    print(" COMPARACIÓN CON OECE")
    print(f"{'='*100}")
    
    oece_2024 = 5812
    oece_2025 = 4231
    oece_total = 10043
    
    print(f"\n  {'Año':<10} | {'JSON':>8} | {'OECE':>8} | {'Diferencia':>12}")
    print(f"  {'-'*50}")
    print(f"  {'2024':<10} | {total_2024:>8,} | {oece_2024:>8,} | {total_2024-oece_2024:>+12,}")
    print(f"  {'2025':<10} | {total_2025:>8,} | {oece_2025:>8,} | {total_2025-oece_2025:>+12,}")
    print(f"  {'-'*50}")
    print(f"  {'TOTAL':<10} | {total_general:>8,} | {oece_total:>8,} | {total_general-oece_total:>+12,}")
    
    # Detalle por mes 2025
    print(f"\n{'='*100}")
    print(" DETALLE 2025 POR MES")
    print(f"{'='*100}")
    
    meses_oece_2025 = {
        1: 71, 2: 228, 3: 340, 4: 614, 5: 143, 6: 329,
        7: 389, 8: 416, 9: 488, 10: 634, 11: 377, 12: 202
    }
    
    print(f"\n  {'Mes':<15} | {'JSON':>8} | {'OECE':>8} | {'Diferencia':>12}")
    print(f"  {'-'*60}")
    
    for mes in range(1, 13):
        json_count = conteo_por_mes_2025.get(mes, 0)
        oece_count = meses_oece_2025.get(mes, 0)
        diff = json_count - oece_count
        
        mes_nombre = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][mes]
        
        estado = "✅" if diff == 0 else "❌"
        print(f"  {estado} {mes_nombre:<12} | {json_count:>8,} | {oece_count:>8,} | {diff:>+12,}")
    
    print(f"  {'-'*60}")
    print(f"  {'TOTAL 2025':<15} | {total_2025:>8,} | {oece_2025:>8,} | {total_2025-oece_2025:>+12,}")
    
    return conteo_por_archivo, total_2024, total_2025

if __name__ == "__main__":
    contar_en_json()
