"""
Diagnóstico Exhaustivo de entidad_financiera
Verifica si la columna se está cargando correctamente y completamente
"""
import mysql.connector
import sys
import json
import os

# Configurar encoding UTF-8 para Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

def main():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("="*120)
    print("DIAGNÓSTICO EXHAUSTIVO: Columna entidad_financiera")
    print("="*120)
    
    # ========================================
    # 1. ESTADÍSTICAS GENERALES
    # ========================================
    print("\n" + "="*120)
    print("1. ESTADÍSTICAS GENERALES")
    print("="*120)
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    total_adj = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE entidad_financiera IS NOT NULL AND entidad_financiera != ''
    """)
    con_entidad = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE entidad_financiera IS NULL OR entidad_financiera = ''
    """)
    sin_entidad = cursor.fetchone()[0]
    
    print(f"\nTotal adjudicaciones: {total_adj:,}")
    print(f"Con entidad_financiera: {con_entidad:,} ({con_entidad*100/total_adj:.2f}%)")
    print(f"Sin entidad_financiera: {sin_entidad:,} ({sin_entidad*100/total_adj:.2f}%)")
    
    # ========================================
    # 2. ANÁLISIS POR id_contrato
    # ========================================
    print("\n" + "="*120)
    print("2. ANÁLISIS POR id_contrato (CRÍTICO)")
    print("="*120)
    print("El spider SOLO puede procesar registros que tengan id_contrato")
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE id_contrato IS NOT NULL AND id_contrato != ''
    """)
    con_id_contrato = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE id_contrato IS NULL OR id_contrato = ''
    """)
    sin_id_contrato = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE (id_contrato IS NOT NULL AND id_contrato != '')
          AND (entidad_financiera IS NOT NULL AND entidad_financiera != '')
    """)
    procesados = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE (id_contrato IS NOT NULL AND id_contrato != '')
          AND (entidad_financiera IS NULL OR entidad_financiera = '')
    """)
    pendientes = cursor.fetchone()[0]
    
    print(f"\n{'CATEGORÍA':<40} {'CANTIDAD':<15} {'%':<10}")
    print("-"*120)
    print(f"{'Con id_contrato (PROCESABLES)':<40} {con_id_contrato:,<15} {con_id_contrato*100/total_adj:.2f}%")
    print(f"{'Sin id_contrato (NO PROCESABLES)':<40} {sin_id_contrato:,<15} {sin_id_contrato*100/total_adj:.2f}%")
    print("-"*120)
    print(f"{'De los PROCESABLES:':<40}")
    print(f"{'  - Ya procesados (con entidad)':<40} {procesados:,<15} {procesados*100/con_id_contrato if con_id_contrato > 0 else 0:.2f}%")
    print(f"{'  - Pendientes (sin entidad)':<40} {pendientes:,<15} {pendientes*100/con_id_contrato if con_id_contrato > 0 else 0:.2f}%")
    
    if pendientes > 0:
        print(f"\n⚠️  PROBLEMA DETECTADO: Hay {pendientes:,} registros CON id_contrato pero SIN entidad_financiera")
        print(f"    Esto indica que el spider NO ha procesado todos los registros procesables.")
    else:
        print(f"\n✅ EXCELENTE: Todos los registros procesables han sido procesados.")
    
    # ========================================
    # 3. ANÁLISIS POR estado_item
    # ========================================
    print("\n" + "="*120)
    print("3. ANÁLISIS POR estado_item")
    print("="*120)
    
    cursor.execute("""
        SELECT 
            estado_item,
            COUNT(*) as total,
            SUM(CASE WHEN id_contrato IS NULL OR id_contrato = '' THEN 1 ELSE 0 END) as sin_id_contrato,
            SUM(CASE WHEN (id_contrato IS NOT NULL AND id_contrato != '') 
                     AND (entidad_financiera IS NULL OR entidad_financiera = '') THEN 1 ELSE 0 END) as pendientes,
            SUM(CASE WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' THEN 1 ELSE 0 END) as procesados,
            ROUND(SUM(CASE WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_procesado
        FROM Licitaciones_Adjudicaciones
        GROUP BY estado_item
        ORDER BY total DESC
    """)
    
    print(f"\n{'ESTADO':<20} {'TOTAL':<10} {'SIN_ID':<12} {'PENDIENTES':<12} {'PROCESADOS':<12} {'% PROC':<10}")
    print("-"*120)
    for row in cursor.fetchall():
        estado = row[0] or 'NULL'
        print(f"{estado:<20} {row[1]:<10} {row[2]:<12} {row[3]:<12} {row[4]:<12} {row[5]:<10}%")
    
    # ========================================
    # 4. DISTRIBUCIÓN DE VALORES
    # ========================================
    print("\n" + "="*120)
    print("4. DISTRIBUCIÓN DE VALORES DE entidad_financiera")
    print("="*120)
    
    cursor.execute("""
        SELECT entidad_financiera, COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        WHERE entidad_financiera IS NOT NULL AND entidad_financiera != ''
        GROUP BY entidad_financiera
        ORDER BY total DESC
        LIMIT 30
    """)
    
    print(f"\n{'ENTIDAD_FINANCIERA':<60} {'CANTIDAD':<15}")
    print("-"*120)
    for row in cursor.fetchall():
        print(f"{row[0]:<60} {row[1]:,<15}")
    
    # ========================================
    # 5. VALORES ESPECIALES Y ERRORES
    # ========================================
    print("\n" + "="*120)
    print("5. VALORES ESPECIALES Y ERRORES")
    print("="*120)
    
    cursor.execute("""
        SELECT 
            CASE 
                WHEN entidad_financiera IS NULL OR entidad_financiera = '' THEN 'NULL/VACÍO'
                WHEN entidad_financiera = 'SIN_GARANTIA' THEN 'SIN_GARANTIA'
                WHEN entidad_financiera = 'NO_INFO' THEN 'NO_INFO'
                WHEN entidad_financiera LIKE 'ERROR%' THEN 'ERROR_*'
                WHEN entidad_financiera LIKE 'CONTRATO_NO%' THEN 'CONTRATO_NO_ENCONTRADO'
                ELSE 'ENTIDAD_REAL'
            END as tipo_valor,
            COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        GROUP BY tipo_valor
        ORDER BY total DESC
    """)
    
    print(f"\n{'TIPO DE VALOR':<40} {'CANTIDAD':<15}")
    print("-"*120)
    for row in cursor.fetchall():
        print(f"{row[0]:<40} {row[1]:,<15}")
    
    # ========================================
    # 6. EJEMPLOS DE REGISTROS PENDIENTES
    # ========================================
    print("\n" + "="*120)
    print("6. EJEMPLOS DE REGISTROS PENDIENTES (Con id_contrato pero sin entidad)")
    print("="*120)
    
    cursor.execute("""
        SELECT id_adjudicacion, id_contrato, estado_item, ganador_nombre
        FROM Licitaciones_Adjudicaciones
        WHERE (id_contrato IS NOT NULL AND id_contrato != '')
          AND (entidad_financiera IS NULL OR entidad_financiera = '')
        LIMIT 20
    """)
    
    ejemplos = cursor.fetchall()
    
    if ejemplos:
        print(f"\n{'ID_ADJUDICACION':<30} {'ID_CONTRATO':<20} {'ESTADO':<15} {'GANADOR':<55}")
        print("-"*120)
        for row in ejemplos:
            ganador = (row[3] or '')[:52] + '...' if row[3] and len(row[3]) > 55 else (row[3] or 'NULL')
            print(f"{row[0]:<30} {row[1]:<20} {row[2] or 'NULL':<15} {ganador:<55}")
        
        print(f"\n⚠️  Estos {len(ejemplos)} registros DEBERÍAN haber sido procesados por el spider.")
        print(f"    Tienen id_contrato pero NO tienen entidad_financiera.")
    else:
        print("\n✅ No hay registros pendientes. Todos los procesables han sido procesados.")
    
    # ========================================
    # 7. VERIFICACIÓN DE CONSISTENCIA CON JSON
    # ========================================
    print("\n" + "="*120)
    print("7. VERIFICACIÓN CON ARCHIVOS JSON (Muestra)")
    print("="*120)
    print("Verificando si los datos en BD coinciden con los JSON originales...")
    
    # Tomamos 5 ejemplos aleatorios de registros procesados
    cursor.execute("""
        SELECT id_adjudicacion, id_convocatoria, id_contrato, entidad_financiera
        FROM Licitaciones_Adjudicaciones
        WHERE entidad_financiera IS NOT NULL 
          AND entidad_financiera != ''
          AND entidad_financiera NOT IN ('SIN_GARANTIA', 'NO_INFO', 'ERROR_CONEXION')
        ORDER BY RAND()
        LIMIT 5
    """)
    
    muestras = cursor.fetchall()
    
    if muestras:
        print(f"\nVerificando {len(muestras)} registros aleatorios con entidad financiera...")
        
        for id_adj, id_conv, id_cont, entidad_bd in muestras:
            # Buscar en JSON
            json_encontrado = False
            
            # Buscar el archivo JSON correspondiente
            for archivo in os.listdir('1_database'):
                if archivo.endswith('_seace_v3.json'):
                    ruta_json = os.path.join('1_database', archivo)
                    try:
                        with open(ruta_json, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        # Buscar el OCID correspondiente
                        for release in data.get('releases', []):
                            tender = release.get('tender', {})
                            if tender.get('id') == id_conv:
                                # Encontramos la licitación
                                awards = release.get('awards', [])
                                for award in awards:
                                    if award.get('id') == id_adj:
                                        # Encontramos la adjudicación
                                        contratos = award.get('contracts', [])
                                        for contrato in contratos:
                                            if contrato.get('id') == id_cont:
                                                # Verificar garantías
                                                garantias = contrato.get('guarantees', [])
                                                if garantias:
                                                    print(f"\n✅ {id_adj[:30]}")
                                                    print(f"   BD: {entidad_bd}")
                                                    print(f"   JSON: {len(garantias)} garantía(s) encontrada(s)")
                                                    for g in garantias[:2]:  # Mostrar máximo 2
                                                        print(f"        - {g.get('guarantor', {}).get('name', 'N/A')}")
                                                else:
                                                    print(f"\n⚠️  {id_adj[:30]}")
                                                    print(f"   BD: {entidad_bd}")
                                                    print(f"   JSON: Sin garantías en JSON (posible SIN_GARANTIA)")
                                                json_encontrado = True
                                                break
                                        if json_encontrado:
                                            break
                                if json_encontrado:
                                    break
                        if json_encontrado:
                            break
                    except:
                        continue
            
            if not json_encontrado:
                print(f"\n❌ {id_adj[:30]} - No encontrado en JSON")
    
    # ========================================
    # 8. DIAGNÓSTICO FINAL
    # ========================================
    print("\n" + "="*120)
    print("8. DIAGNÓSTICO FINAL")
    print("="*120)
    
    if pendientes > 0:
        print(f"\n❌ PROBLEMA CONFIRMADO:")
        print(f"   Hay {pendientes:,} registros que DEBERÍAN estar procesados pero NO lo están.")
        print(f"\n📋 POSIBLES CAUSAS:")
        print(f"   1. El spider_garantias.py NO se ha ejecutado completamente")
        print(f"   2. El spider se detuvo antes de terminar")
        print(f"   3. Hubo errores de conexión durante la ejecución")
        print(f"\n💡 SOLUCIÓN RECOMENDADA:")
        print(f"   Ejecutar: cd 1_motor_etl && python spider_garantias.py")
        print(f"   Esto procesará los {pendientes:,} registros pendientes.")
    else:
        print(f"\n✅ TODO CORRECTO:")
        print(f"   Todos los registros procesables ({con_id_contrato:,}) han sido procesados.")
        print(f"   Los {sin_id_contrato:,} registros sin entidad_financiera NO tienen id_contrato,")
        print(f"   por lo tanto es NORMAL que no tengan entidad financiera.")
    
    # Verificar calidad de los datos procesados
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE entidad_financiera LIKE 'ERROR%'
    """)
    errores = cursor.fetchone()[0]
    
    if errores > 0:
        print(f"\n⚠️  ADVERTENCIA: Hay {errores:,} registros con ERROR en entidad_financiera")
        print(f"   Esto indica problemas de conexión o API durante el procesamiento.")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*120)
    print("FIN DEL DIAGNÓSTICO")
    print("="*120)

if __name__ == "__main__":
    main()
