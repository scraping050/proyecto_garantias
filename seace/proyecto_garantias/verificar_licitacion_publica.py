"""
Verifica la carga completa de Licitación Pública (EXACTA)
Compara JSON vs Base de Datos
"""
import json
import os
import sys
import mysql.connector

# Fix encoding
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Configuración
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from secrets_manager import get_db_config

parent_dir = os.path.dirname(os.path.abspath(__file__))
db_folder = os.path.join(parent_dir, "1_database")

def contar_en_json():
    """Cuenta registros de Licitación Pública EXACTA en JSONs"""
    total = 0
    ids_json = set()
    por_archivo = {}
    
    archivos = sorted([f for f in os.listdir(db_folder) if f.endswith('.json')])
    
    print("="*80)
    print("CONTEO EN ARCHIVOS JSON")
    print("="*80)
    
    for archivo in archivos:
        ruta = os.path.join(db_folder, archivo)
        count = 0
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            records = data.get('records', data if isinstance(data, list) else [])
            
            for r in records:
                compiled = r.get('compiledRelease', {})
                tender = compiled.get('tender', {})
                tipo = tender.get('procurementMethodDetails')
                
                # SOLO EXACTO
                if tipo == 'Licitación Pública':
                    count += 1
                    id_conv = tender.get('id')
                    if id_conv:
                        ids_json.add(str(id_conv))
            
            if count > 0:
                print(f"{archivo:30} | {count:5,} registros")
                por_archivo[archivo] = count
                total += count
                
        except Exception as e:
            print(f"{archivo:30} | ERROR: {e}")
    
    print("="*80)
    print(f"TOTAL EN JSON: {total:,} registros")
    print(f"IDs únicos: {len(ids_json):,}")
    print("="*80)
    
    return total, ids_json, por_archivo

def contar_en_bd():
    """Cuenta registros en base de datos"""
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("CONTEO EN BASE DE DATOS")
    print("="*80)
    
    # Total registros
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Cabecera 
        WHERE tipo_procedimiento = 'Licitación Pública'
    """)
    total = cursor.fetchone()[0]
    print(f"Total registros: {total:,}")
    
    # IDs únicos
    cursor.execute("""
        SELECT COUNT(DISTINCT id_convocatoria) 
        FROM Licitaciones_Cabecera 
        WHERE tipo_procedimiento = 'Licitación Pública'
    """)
    unicos = cursor.fetchone()[0]
    print(f"IDs únicos: {unicos:,}")
    
    # Por archivo origen
    cursor.execute("""
        SELECT archivo_origen, COUNT(*) as total
        FROM Licitaciones_Cabecera 
        WHERE tipo_procedimiento = 'Licitación Pública'
        GROUP BY archivo_origen
        ORDER BY archivo_origen
    """)
    
    por_archivo = {}
    print("\nPor archivo:")
    for archivo, count in cursor.fetchall():
        print(f"{archivo:30} | {count:5,} registros")
        por_archivo[archivo] = count
    
    print("="*80)
    
    # Obtener IDs
    cursor.execute("""
        SELECT DISTINCT id_convocatoria 
        FROM Licitaciones_Cabecera 
        WHERE tipo_procedimiento = 'Licitación Pública'
    """)
    ids_bd = set(str(row[0]) for row in cursor.fetchall())
    
    conn.close()
    
    return total, ids_bd, por_archivo

def comparar():
    """Compara JSON vs BD"""
    print("\n" + "="*80)
    print("ANÁLISIS COMPARATIVO")
    print("="*80)
    
    total_json, ids_json, archivos_json = contar_en_json()
    total_bd, ids_bd, archivos_bd = contar_en_bd()
    
    print("\n" + "="*80)
    print("RESUMEN")
    print("="*80)
    print(f"Registros en JSON:     {total_json:,}")
    print(f"Registros en BD:       {total_bd:,}")
    print(f"Diferencia:            {total_json - total_bd:,}")
    print()
    print(f"IDs únicos en JSON:    {len(ids_json):,}")
    print(f"IDs únicos en BD:      {len(ids_bd):,}")
    print(f"IDs faltantes en BD:   {len(ids_json - ids_bd):,}")
    
    # Verificar vs API SEACE
    print("\n" + "="*80)
    print("COMPARACIÓN CON API SEACE")
    print("="*80)
    print(f"Reportado por SEACE API: 9,981")
    print(f"Encontrado en JSON:      {total_json:,}")
    print(f"Diferencia:              {9981 - total_json:,}")
    
    if 9981 - total_json > 0:
        print("\n⚠️ ADVERTENCIA: Faltan registros en los JSONs descargados")
        print("   Posibles causas:")
        print("   1. Descarga incompleta de algunos archivos")
        print("   2. JSONs no actualizados vs API en tiempo real")
        print("   3. Filtros aplicados durante descarga")
    
    # Comparar por archivo
    print("\n" + "="*80)
    print("COMPARACIÓN POR ARCHIVO")
    print("="*80)
    print(f"{'Archivo':30} | {'JSON':>8} | {'BD':>8} | {'Diff':>8}")
    print("-"*80)
    
    todos_archivos = set(archivos_json.keys()) | set(archivos_bd.keys())
    for archivo in sorted(todos_archivos):
        json_count = archivos_json.get(archivo, 0)
        bd_count = archivos_bd.get(archivo, 0)
        diff = json_count - bd_count
        marca = "⚠️" if diff != 0 else "✅"
        print(f"{archivo:30} | {json_count:8,} | {bd_count:8,} | {diff:8,} {marca if diff != 0 else ''}")
    
    # Mostrar algunos IDs faltantes
    faltantes = ids_json - ids_bd
    if faltantes:
        print("\n" + "="*80)
        print(f"PRIMEROS 10 IDs FALTANTES EN BD (de {len(faltantes):,} total)")
        print("="*80)
        for i, id_conv in enumerate(sorted(faltantes)[:10], 1):
            print(f"{i:2}. {id_conv}")

if __name__ == "__main__":
    comparar()
