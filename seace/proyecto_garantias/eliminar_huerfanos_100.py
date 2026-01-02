"""
Eliminar los 6 OCIDs huérfanos para llegar a 100% coincidencia
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

def eliminar_huerfanos():
    """Elimina OCIDs que están en BD pero no en JSONs"""
    
    print("=" * 100)
    print(" ELIMINACIÓN DE OCIDs HUÉRFANOS")
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
    
    print(f"  ✅ OCIDs huérfanos encontrados: {len(huerfanos)}")
    
    if huerfanos:
        print(f"\n{'='*100}")
        print(" DETALLES DE HUÉRFANOS")
        print(f"{'='*100}")
        
        for ocid in sorted(huerfanos):
            cursor.execute("""
                SELECT 
                    id_convocatoria,
                    nomenclatura,
                    DATE(fecha_publicacion) as fecha,
                    estado_proceso,
                    archivo_origen
                FROM Licitaciones_Cabecera
                WHERE ocid = %s
            """, (ocid,))
            
            resultado = cursor.fetchone()
            
            if resultado:
                id_conv, nomenclatura, fecha, estado, archivo = resultado
                
                print(f"\n  OCID: {ocid}")
                print(f"    id_convocatoria: {id_conv}")
                print(f"    Nomenclatura: {nomenclatura[:60] if nomenclatura else 'N/A'}...")
                print(f"    Fecha: {fecha}")
                print(f"    Estado: {estado}")
                print(f"    Archivo: {archivo}")
        
        # Confirmar eliminación
        print(f"\n{'='*100}")
        print(" CONFIRMACIÓN DE ELIMINACIÓN")
        print(f"{'='*100}")
        print(f"\n⚠️  Se eliminarán {len(huerfanos)} registros huérfanos")
        print(f"⚠️  Esto reducirá el total de 10,049 a 10,043 (100% coincidencia con OECE)")
        
        respuesta = input("\n¿Deseas continuar con la eliminación? (si/no): ")
        
        if respuesta.lower() in ['si', 's', 'yes', 'y']:
            print(f"\n🗑️  Eliminando huérfanos...")
            
            for ocid in huerfanos:
                cursor.execute("DELETE FROM Licitaciones_Cabecera WHERE ocid = %s", (ocid,))
                print(f"   ✅ Eliminado: {ocid}")
            
            conn.commit()
            
            print(f"\n✅ Eliminación completada exitosamente")
            
            # Verificar resultado
            cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
            total_final = cursor.fetchone()[0]
            
            print(f"\n📊 Total de registros después de eliminación: {total_final:,}")
            print(f"📊 Diferencia con OECE (10,043): {total_final - 10043:+,}")
            
            if total_final == 10043:
                print(f"\n🎉 ¡PERFECTO! Ahora tenemos 100% de coincidencia con OECE")
            else:
                print(f"\n⚠️  Aún hay diferencia de {abs(total_final - 10043)} registros")
        else:
            print(f"\n❌ Eliminación cancelada por el usuario")
    else:
        print(f"\n✅ No hay huérfanos para eliminar")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    eliminar_huerfanos()
