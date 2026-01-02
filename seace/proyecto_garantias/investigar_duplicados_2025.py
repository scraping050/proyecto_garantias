"""
Investigar los 6 registros duplicados en 2025
Identificar exactamente cuáles son y por qué están duplicados
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

def investigar_duplicados_2025():
    """Investiga los 6 registros extra en 2025"""
    
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("=" * 100)
    print(" INVESTIGACIÓN DE 6 REGISTROS EXTRA EN 2025")
    print("=" * 100)
    
    # Meses con diferencias
    meses_problema = {
        6: (329, 330, 1),   # Junio: OECE=329, BD=330, diff=+1
        8: (416, 418, 2),   # Agosto: OECE=416, BD=418, diff=+2
        10: (634, 636, 2),  # Octubre: OECE=634, BD=636, diff=+2
        11: (377, 378, 1)   # Noviembre: OECE=377, BD=378, diff=+1
    }
    
    total_duplicados_encontrados = 0
    duplicados_por_mes = {}
    
    for mes, (oece, bd, diff) in meses_problema.items():
        print(f"\n{'='*100}")
        print(f" MES: 2025-{mes:02d} | OECE={oece} | BD={bd} | Diferencia=+{diff}")
        print(f"{'='*100}")
        
        # Buscar duplicados por id_convocatoria en este mes
        cursor.execute("""
            SELECT 
                id_convocatoria,
                COUNT(*) as cantidad,
                GROUP_CONCAT(ocid ORDER BY ocid SEPARATOR ', ') as ocids
            FROM Licitaciones_Cabecera
            WHERE YEAR(fecha_publicacion) = 2025
              AND MONTH(fecha_publicacion) = %s
            GROUP BY id_convocatoria
            HAVING COUNT(*) > 1
            ORDER BY cantidad DESC
        """, (mes,))
        
        duplicados = cursor.fetchall()
        
        if duplicados:
            print(f"\n  ✅ Encontrados {len(duplicados)} id_convocatoria duplicados:")
            
            for id_conv, cantidad, ocids in duplicados:
                print(f"\n  📋 id_convocatoria: {id_conv} ({cantidad} registros)")
                print(f"     OCIDs: {ocids[:100]}...")
                
                # Obtener detalles de cada registro
                cursor.execute("""
                    SELECT 
                        ocid,
                        nomenclatura,
                        DATE_FORMAT(fecha_publicacion, '%%Y-%%m-%%d') as fecha,
                        estado_proceso,
                        DATE_FORMAT(last_update, '%%Y-%%m-%%d %%H:%%i:%%s') as ultima_actualizacion
                    FROM Licitaciones_Cabecera
                    WHERE id_convocatoria = %s
                    ORDER BY last_update DESC
                """, (id_conv,))
                
                registros = cursor.fetchall()
                
                for i, (ocid, nomenclatura, fecha, estado, last_update) in enumerate(registros, 1):
                    print(f"\n     Registro {i}:")
                    print(f"       OCID:         {ocid}")
                    print(f"       Nomenclatura: {nomenclatura[:60]}...")
                    print(f"       Fecha:        {fecha}")
                    print(f"       Estado:       {estado}")
                    print(f"       Actualizado:  {last_update}")
                
                # Identificar cuál eliminar (el más antiguo)
                if len(registros) > 1:
                    ocid_eliminar = registros[-1][0]  # El último (más antiguo)
                    print(f"\n     ⚠️ CANDIDATO A ELIMINAR: {ocid_eliminar} (más antiguo)")
                    
                    if mes not in duplicados_por_mes:
                        duplicados_por_mes[mes] = []
                    duplicados_por_mes[mes].append({
                        'id_convocatoria': id_conv,
                        'ocid_eliminar': ocid_eliminar,
                        'total_registros': cantidad
                    })
                    
                    total_duplicados_encontrados += (cantidad - 1)
        else:
            print(f"\n  ❌ No se encontraron duplicados por id_convocatoria")
            print(f"  ⚠️ Puede ser un problema de filtrado o criterio diferente")
    
    # Resumen
    print(f"\n{'='*100}")
    print(" RESUMEN DE DUPLICADOS ENCONTRADOS")
    print(f"{'='*100}")
    
    print(f"\n📊 Total de registros duplicados a eliminar: {total_duplicados_encontrados}")
    print(f"📊 Diferencia esperada con OECE: {sum(d for _, (_, _, d) in meses_problema.items())}")
    
    if total_duplicados_encontrados == sum(d for _, (_, _, d) in meses_problema.items()):
        print(f"\n✅ PERFECTO: Encontramos exactamente los {total_duplicados_encontrados} duplicados esperados")
    else:
        print(f"\n⚠️ ATENCIÓN: Encontramos {total_duplicados_encontrados} duplicados, esperábamos {sum(d for _, (_, _, d) in meses_problema.items())}")
    
    # Generar script de eliminación
    if duplicados_por_mes:
        print(f"\n{'='*100}")
        print(" SCRIPT DE ELIMINACIÓN")
        print(f"{'='*100}")
        
        print("\n-- SQL para eliminar duplicados:")
        for mes, dups in duplicados_por_mes.items():
            print(f"\n-- Mes: 2025-{mes:02d}")
            for dup in dups:
                print(f"DELETE FROM Licitaciones_Cabecera WHERE ocid = '{dup['ocid_eliminar']}';")
                print(f"-- (id_convocatoria: {dup['id_convocatoria']}, total registros: {dup['total_registros']})")
    
    cursor.close()
    conn.close()
    
    return duplicados_por_mes

if __name__ == "__main__":
    duplicados_por_mes = investigar_duplicados_2025()
