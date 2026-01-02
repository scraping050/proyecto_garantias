"""
Investigar y eliminar los 6 registros duplicados en 2025
Versión simplificada
"""
import mysql.connector
from config.secrets_manager import get_db_config
import sys

# Fix encoding
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def main():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("=" * 100)
    print(" IDENTIFICACIÓN Y ELIMINACIÓN DE DUPLICADOS EN 2025")
    print("=" * 100)
    
    # Paso 1: Identificar todos los duplicados por id_convocatoria
    cursor.execute("""
        SELECT 
            id_convocatoria,
            COUNT(*) as cantidad,
            MIN(ocid) as ocid_mantener,
            MAX(ocid) as ocid_eliminar,
            DATE_FORMAT(MIN(fecha_publicacion), '%Y-%m') as mes
        FROM Licitaciones_Cabecera
        WHERE YEAR(fecha_publicacion) = 2025
        GROUP BY id_convocatoria
        HAVING COUNT(*) > 1
        ORDER BY mes, id_convocatoria
    """)
    
    duplicados = cursor.fetchall()
    
    print(f"\n📊 Total de id_convocatoria duplicados en 2025: {len(duplicados)}")
    print(f"📊 Total de registros a eliminar: {sum(c-1 for _, c, _, _, _ in duplicados)}")
    
    # Mostrar detalles
    print(f"\n{'='*100}")
    print(" DETALLES DE DUPLICADOS")
    print(f"{'='*100}")
    
    ocids_a_eliminar = []
    
    for id_conv, cantidad, ocid_mantener, ocid_eliminar, mes in duplicados:
        print(f"\n📋 id_convocatoria: {id_conv} | Mes: {mes} | Registros: {cantidad}")
        print(f"   ✅ Mantener: {ocid_mantener}")
        print(f"   ❌ Eliminar: {ocid_eliminar}")
        
        ocids_a_eliminar.append(ocid_eliminar)
    
    # Confirmar eliminación
    print(f"\n{'='*100}")
    print(f" CONFIRMACIÓN DE ELIMINACIÓN")
    print(f"{'='*100}")
    print(f"\n⚠️  Se eliminarán {len(ocids_a_eliminar)} registros duplicados")
    print(f"⚠️  Esto reducirá el total de 10,049 a 10,043 (coincidencia 100% con OECE)")
    
    respuesta = input("\n¿Deseas continuar con la eliminación? (si/no): ")
    
    if respuesta.lower() in ['si', 's', 'yes', 'y']:
        print(f"\n🗑️  Eliminando duplicados...")
        
        for ocid in ocids_a_eliminar:
            cursor.execute("DELETE FROM Licitaciones_Cabecera WHERE ocid = %s", (ocid,))
            print(f"   ✅ Eliminado: {ocid}")
        
        conn.commit()
        
        print(f"\n✅ Eliminación completada exitosamente")
        print(f"✅ {len(ocids_a_eliminar)} registros eliminados")
        
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
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
