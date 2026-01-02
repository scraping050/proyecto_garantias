"""
Identificar los 6 registros que el cargador está duplicando
Comparar OCID en JSONs vs OCID en BD
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

def identificar_duplicados_cargador():
    """Identifica qué OCIDs están duplicados en BD pero no en JSON"""
    
    print("=" * 100)
    print(" IDENTIFICACIÓN DE DUPLICADOS CREADOS POR EL CARGADOR")
    print("=" * 100)
    
    # Paso 1: Obtener todos los OCIDs de los JSONs
    print("\n📂 Paso 1: Leyendo OCIDs de los JSONs...")
    
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
        except Exception as e:
            print(f"  ERROR en {archivo}: {e}")
    
    print(f"  ✅ Total OCIDs en JSONs: {len(ocids_json):,}")
    
    # Paso 2: Obtener todos los OCIDs de la BD
    print("\n💾 Paso 2: Leyendo OCIDs de la Base de Datos...")
    
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    cursor.execute("SELECT ocid FROM Licitaciones_Cabecera")
    ocids_bd = [row[0] for row in cursor.fetchall()]
    
    print(f"  ✅ Total OCIDs en BD: {len(ocids_bd):,}")
    
    # Paso 3: Encontrar duplicados en BD
    print("\n🔍 Paso 3: Identificando duplicados en BD...")
    
    from collections import Counter
    conteo_bd = Counter(ocids_bd)
    duplicados_bd = {ocid: count for ocid, count in conteo_bd.items() if count > 1}
    
    print(f"  ✅ OCIDs duplicados en BD: {len(duplicados_bd)}")
    print(f"  ✅ Registros extras por duplicación: {sum(count - 1 for count in duplicados_bd.values())}")
    
    # Paso 4: Mostrar detalles de duplicados
    if duplicados_bd:
        print(f"\n{'='*100}")
        print(" DETALLES DE DUPLICADOS")
        print(f"{'='*100}")
        
        for ocid, count in sorted(duplicados_bd.items(), key=lambda x: x[1], reverse=True):
            print(f"\n  OCID: {ocid}")
            print(f"  Veces en BD: {count}")
            print(f"  ¿Está en JSON?: {'✅ Sí' if ocid in ocids_json else '❌ No'}")
            
            # Obtener detalles de cada registro
            cursor.execute("""
                SELECT 
                    id_convocatoria,
                    nomenclatura,
                    DATE_FORMAT(fecha_publicacion, '%%Y-%%m-%%d') as fecha,
                    estado_proceso,
                    archivo_origen
                FROM Licitaciones_Cabecera
                WHERE ocid = %s
            """, (ocid,))
            
            registros = cursor.fetchall()
            
            for i, (id_conv, nomenclatura, fecha, estado, archivo) in enumerate(registros, 1):
                print(f"    Registro {i}:")
                print(f"      id_convocatoria: {id_conv}")
                print(f"      Nomenclatura: {nomenclatura[:50]}...")
                print(f"      Fecha: {fecha}")
                print(f"      Estado: {estado}")
                print(f"      Archivo: {archivo}")
    
    # Paso 5: Generar SQL para eliminar duplicados
    if duplicados_bd:
        print(f"\n{'='*100}")
        print(" SOLUCIÓN: ELIMINAR DUPLICADOS")
        print(f"{'='*100}")
        
        print("\n-- SQL para eliminar duplicados (mantener solo el primero):")
        for ocid in duplicados_bd.keys():
            print(f"""
DELETE FROM Licitaciones_Cabecera 
WHERE ocid = '{ocid}' 
  AND last_update NOT IN (
    SELECT * FROM (
      SELECT MIN(last_update) 
      FROM Licitaciones_Cabecera 
      WHERE ocid = '{ocid}'
    ) AS temp
  );""")
    
    cursor.close()
    conn.close()
    
    return duplicados_bd

if __name__ == "__main__":
    duplicados_bd = identificar_duplicados_cargador()
    
    print(f"\n{'='*100}")
    print(" RESUMEN")
    print(f"{'='*100}")
    print(f"\n✅ JSONs tienen: 10,043 registros (100% OECE)")
    print(f"❌ BD tiene: 10,049 registros (+6)")
    print(f"🔧 Duplicados a eliminar: {sum(count - 1 for count in duplicados_bd.values())}")
