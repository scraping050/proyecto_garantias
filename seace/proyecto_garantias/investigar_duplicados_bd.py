"""
Investigación detallada de duplicados por id_convocatoria
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

def investigar_duplicados():
    """Investiga los duplicados por id_convocatoria"""
    
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("=" * 80)
    print(" INVESTIGACIÓN DE DUPLICADOS POR id_convocatoria")
    print("=" * 80)
    
    # Obtener todos los duplicados
    cursor.execute("""
        SELECT id_convocatoria, COUNT(*) as cantidad
        FROM Licitaciones_Cabecera
        WHERE id_convocatoria IS NOT NULL
        GROUP BY id_convocatoria
        HAVING COUNT(*) > 1
        ORDER BY cantidad DESC
    """)
    duplicados = cursor.fetchall()
    
    print(f"\n📊 Total de IDs duplicados: {len(duplicados)}")
    
    # Calcular total de registros duplicados
    total_registros_duplicados = sum(cantidad - 1 for _, cantidad in duplicados)
    print(f"📊 Total de registros duplicados (extras): {total_registros_duplicados}")
    
    # Analizar primeros 5 casos
    print("\n" + "=" * 80)
    print(" ANÁLISIS DETALLADO DE LOS PRIMEROS 5 CASOS")
    print("=" * 80)
    
    for i, (id_conv, cantidad) in enumerate(duplicados[:5], 1):
        print(f"\n{'─' * 80}")
        print(f"CASO {i}: id_convocatoria = {id_conv} ({cantidad} registros)")
        print(f"{'─' * 80}")
        
        cursor.execute("""
            SELECT 
                ocid,
                nomenclatura,
                comprador,
                DATE_FORMAT(fecha_publicacion, '%Y-%m-%d') as fecha,
                estado_proceso,
                archivo_origen
            FROM Licitaciones_Cabecera
            WHERE id_convocatoria = %s
            ORDER BY fecha_publicacion
        """, (id_conv,))
        
        registros = cursor.fetchall()
        
        for j, (ocid, nomenclatura, comprador, fecha, estado, archivo) in enumerate(registros, 1):
            print(f"\n  Registro {j}:")
            print(f"    OCID:         {ocid}")
            print(f"    Nomenclatura: {nomenclatura[:60]}...")
            print(f"    Comprador:    {comprador[:60]}...")
            print(f"    Fecha:        {fecha}")
            print(f"    Estado:       {estado}")
            print(f"    Archivo:      {archivo}")
        
        # Verificar si los OCIDs son diferentes
        ocids = [r[0] for r in registros]
        if len(set(ocids)) == len(ocids):
            print(f"\n  ✅ Todos los OCIDs son DIFERENTES (duplicado legítimo)")
        else:
            print(f"\n  ⚠️ Hay OCIDs repetidos (posible error)")
    
    # Resumen de causas
    print("\n" + "=" * 80)
    print(" ANÁLISIS DE CAUSAS")
    print("=" * 80)
    
    # Verificar si los duplicados tienen OCIDs diferentes
    cursor.execute("""
        SELECT 
            id_convocatoria,
            COUNT(DISTINCT ocid) as ocids_unicos,
            COUNT(*) as total_registros
        FROM Licitaciones_Cabecera
        WHERE id_convocatoria IN (
            SELECT id_convocatoria
            FROM Licitaciones_Cabecera
            WHERE id_convocatoria IS NOT NULL
            GROUP BY id_convocatoria
            HAVING COUNT(*) > 1
        )
        GROUP BY id_convocatoria
        HAVING COUNT(DISTINCT ocid) = COUNT(*)
    """)
    
    duplicados_legitimos = cursor.fetchall()
    
    print(f"\n📊 Duplicados con OCIDs DIFERENTES (legítimos): {len(duplicados_legitimos)}")
    print(f"   Estos son casos donde el mismo id_convocatoria tiene múltiples OCIDs")
    print(f"   Esto puede ocurrir cuando una licitación se modifica o re-publica")
    
    # Verificar duplicados con mismo OCID
    cursor.execute("""
        SELECT 
            id_convocatoria,
            COUNT(DISTINCT ocid) as ocids_unicos,
            COUNT(*) as total_registros
        FROM Licitaciones_Cabecera
        WHERE id_convocatoria IN (
            SELECT id_convocatoria
            FROM Licitaciones_Cabecera
            WHERE id_convocatoria IS NOT NULL
            GROUP BY id_convocatoria
            HAVING COUNT(*) > 1
        )
        GROUP BY id_convocatoria
        HAVING COUNT(DISTINCT ocid) < COUNT(*)
    """)
    
    duplicados_problematicos = cursor.fetchall()
    
    print(f"\n📊 Duplicados con OCIDs REPETIDOS (problemáticos): {len(duplicados_problematicos)}")
    if duplicados_problematicos:
        print(f"   ⚠️ ESTOS SON VERDADEROS DUPLICADOS QUE DEBEN ELIMINARSE")
    
    # Recomendaciones
    print("\n" + "=" * 80)
    print(" RECOMENDACIONES")
    print("=" * 80)
    
    if len(duplicados_legitimos) == len(duplicados):
        print("\n✅ TODOS los duplicados son LEGÍTIMOS")
        print("   • Cada id_convocatoria tiene OCIDs únicos")
        print("   • Esto es normal en SEACE (modificaciones/re-publicaciones)")
        print("   • NO se requiere acción de limpieza")
    else:
        print(f"\n⚠️ Se encontraron {len(duplicados_problematicos)} duplicados problemáticos")
        print("   • Estos tienen el mismo OCID repetido")
        print("   • Se recomienda eliminar los duplicados")
        print("   • Mantener solo el registro más reciente")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    investigar_duplicados()
