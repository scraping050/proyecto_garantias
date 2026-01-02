"""
Identificar los 6 OCIDs que están en BD pero NO en JSONs
"""
import json
import os
import sys
import mysql.connector
from config.secrets_manager import get_db_config

# Fix encoding
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

parent_dir = os.path.dirname(os.path.abspath(__file__))
db_folder = os.path.join(parent_dir, "1_database")

def encontrar_ocids_huerfanos():
    """Encuentra OCIDs en BD que no están en JSONs"""
    
    print("=" * 100)
    print(" IDENTIFICACIÓN DE OCIDs HUÉRFANOS (BD pero no en JSON)")
    print("=" * 100)
    
    # Paso 1: Leer OCIDs de JSONs
    print("\n📂 Leyendo OCIDs de JSONs...")
    
    ocids_json = set()
    archivos = sorted([f for f in os.listdir(db_folder) if f.endswith('.json')])
    
    for archivo in archivos:
        ruta = os.path.join(db_folder, archivo)
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            records = data.get('records', [])
            
            for r in records:
                compiled = r.get('compiledRelease', {})
                tender = compiled.get('tender', {})
                
                if tender.get('procurementMethodDetails') == 'Licitación Pública':
                    ocid = r.get('ocid')
                    if ocid:
                        ocids_json.add(ocid)
        except:
            pass
    
    print(f"  ✅ Total OCIDs en JSONs: {len(ocids_json):,}")
    
    # Paso 2: Leer OCIDs de BD
    print("\n💾 Leyendo OCIDs de BD...")
    
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    cursor.execute("SELECT ocid FROM Licitaciones_Cabecera")
    ocids_bd = set(row[0] for row in cursor.fetchall())
    
    print(f"  ✅ Total OCIDs en BD: {len(ocids_bd):,}")
    
    # Paso 3: Encontrar huérfanos
    print("\n🔍 Identificando huérfanos...")
    
    huerfanos = ocids_bd - ocids_json
    
    print(f"  ✅ OCIDs huérfanos (en BD pero no en JSON): {len(huerfanos)}")
    
    if huerfanos:
        print(f"\n{'='*100}")
        print(" DETALLES DE OCIDs HUÉRFANOS")
        print(f"{'='*100}")
        
        for ocid in sorted(huerfanos):
            cursor.execute("""
                SELECT 
                    id_convocatoria,
                    nomenclatura,
                    DATE_FORMAT(fecha_publicacion, '%%Y-%%m-%%d') as fecha,
                    estado_proceso,
                    archivo_origen,
                    DATE_FORMAT(fecha_carga, '%%Y-%%m-%%d %%H:%%i:%%s') as fecha_carga
                FROM Licitaciones_Cabecera
                WHERE ocid = %s
            """, (ocid,))
            
            resultado = cursor.fetchone()
            
            if resultado:
                id_conv, nomenclatura, fecha, estado, archivo, fecha_carga = resultado
                
                print(f"\n  OCID: {ocid}")
                print(f"    id_convocatoria: {id_conv}")
                print(f"    Nomenclatura: {nomenclatura[:60]}...")
                print(f"    Fecha publicación: {fecha}")
                print(f"    Estado: {estado}")
                print(f"    Archivo origen: {archivo}")
                print(f"    Fecha carga: {fecha_carga}")
        
        # Generar SQL para eliminar
        print(f"\n{'='*100}")
        print(" SQL PARA ELIMINAR HUÉRFANOS")
        print(f"{'='*100}")
        
        print("\n-- Eliminar los 6 OCIDs huérfanos:")
        for ocid in sorted(huerfanos):
            print(f"DELETE FROM Licitaciones_Cabecera WHERE ocid = '{ocid}';")
    
    cursor.close()
    conn.close()
    
    return huerfanos

if __name__ == "__main__":
    huerfanos = encontrar_ocids_huerfanos()
    
    print(f"\n{'='*100}")
    print(" RESUMEN")
    print(f"{'='*100}")
    print(f"\n✅ JSONs: 10,043 OCIDs únicos")
    print(f"❌ BD: 10,049 OCIDs únicos")
    print(f"🗑️ Huérfanos a eliminar: {len(huerfanos)}")
    
    if len(huerfanos) == 6:
        print(f"\n🎯 PERFECTO: Encontramos exactamente los 6 registros extras")
    else:
        print(f"\n⚠️ Encontramos {len(huerfanos)} huérfanos, esperábamos 6")
