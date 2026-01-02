"""
Auditoría completa de la columna entidad_financiera
Verifica completitud, calidad de datos, y problemas de carga
"""
import mysql.connector
import sys
sys.path.insert(0, 'config')
from secrets_manager import get_db_config

def main():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("="*100)
    print("AUDITORÍA: Columna entidad_financiera")
    print("="*100)
    
    # 1. Estadísticas generales
    print("\n1. ESTADÍSTICAS GENERALES:")
    print("-"*100)
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    total = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE entidad_financiera IS NULL OR entidad_financiera = ''
    """)
    null_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE entidad_financiera IS NOT NULL AND entidad_financiera != ''
    """)
    with_value = cursor.fetchone()[0]
    
    print(f"Total adjudicaciones: {total:,}")
    print(f"Con entidad_financiera: {with_value:,} ({with_value*100/total:.2f}%)")
    print(f"Sin entidad_financiera (NULL/vacío): {null_count:,} ({null_count*100/total:.2f}%)")
    
    # 2. Distribución de valores
    print("\n\n2. DISTRIBUCIÓN DE VALORES (Top 20):")
    print("-"*100)
    cursor.execute("""
        SELECT entidad_financiera, COUNT(*) as total,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Licitaciones_Adjudicaciones), 2) as porcentaje
        FROM Licitaciones_Adjudicaciones
        WHERE entidad_financiera IS NOT NULL AND entidad_financiera != ''
        GROUP BY entidad_financiera
        ORDER BY total DESC
        LIMIT 20
    """)
    
    print(f"{'ENTIDAD_FINANCIERA':<50} {'TOTAL':<10} {'%':<10}")
    print("-"*100)
    for row in cursor.fetchall():
        print(f"{row[0]:<50} {row[1]:<10} {row[2]:<10}%")
    
    # 3. Análisis por estado_item
    print("\n\n3. COMPLETITUD POR estado_item:")
    print("-"*100)
    cursor.execute("""
        SELECT 
            estado_item,
            COUNT(*) as total,
            SUM(CASE WHEN entidad_financiera IS NULL OR entidad_financiera = '' THEN 1 ELSE 0 END) as sin_procesar,
            SUM(CASE WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' THEN 1 ELSE 0 END) as procesados,
            ROUND(SUM(CASE WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_procesado
        FROM Licitaciones_Adjudicaciones
        GROUP BY estado_item
        ORDER BY total DESC
    """)
    
    print(f"{'ESTADO':<20} {'TOTAL':<10} {'SIN PROCESAR':<15} {'PROCESADOS':<12} {'% PROCESADO':<12}")
    print("-"*100)
    for row in cursor.fetchall():
        print(f"{row[0] or 'NULL':<20} {row[1]:<10} {row[2]:<15} {row[3]:<12} {row[4]:<12}%")
    
    # 4. Valores especiales
    print("\n\n4. VALORES ESPECIALES:")
    print("-"*100)
    cursor.execute("""
        SELECT 
            CASE 
                WHEN entidad_financiera IS NULL OR entidad_financiera = '' THEN 'NULL/VACÍO'
                WHEN entidad_financiera = 'SIN_GARANTIA' THEN 'SIN_GARANTIA'
                WHEN entidad_financiera = 'NO_INFO' THEN 'NO_INFO'
                WHEN entidad_financiera LIKE 'ERROR%' THEN 'ERROR_*'
                WHEN entidad_financiera LIKE 'CONTRATO_NO%' THEN 'CONTRATO_NO_*'
                ELSE 'ENTIDAD_REAL'
            END as tipo_valor,
            COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        GROUP BY tipo_valor
        ORDER BY total DESC
    """)
    
    print(f"{'TIPO DE VALOR':<30} {'TOTAL':<10}")
    print("-"*100)
    for row in cursor.fetchall():
        print(f"{row[0]:<30} {row[1]:<10}")
    
    # 5. Ejemplos de registros sin procesar
    print("\n\n5. EJEMPLOS DE REGISTROS SIN PROCESAR (NULL):")
    print("-"*100)
    cursor.execute("""
        SELECT id_adjudicacion, id_convocatoria, estado_item, ganador_nombre
        FROM Licitaciones_Adjudicaciones
        WHERE entidad_financiera IS NULL OR entidad_financiera = ''
        LIMIT 10
    """)
    
    print(f"{'ID_ADJUDICACION':<25} {'ID_CONVOCATORIA':<20} {'ESTADO':<15} {'GANADOR':<40}")
    print("-"*100)
    for row in cursor.fetchall():
        ganador = (row[3] or '')[:37] + '...' if row[3] and len(row[3]) > 40 else (row[3] or 'NULL')
        print(f"{row[0]:<25} {row[1]:<20} {row[2] or 'NULL':<15} {ganador:<40}")
    
    # 6. Verificar si spider_garantias.py se ejecutó
    print("\n\n6. VERIFICACIÓN DE EJECUCIÓN DEL SPIDER:")
    print("-"*100)
    
    # Calcular cuántos ciclos se necesitan
    registros_pendientes = null_count
    registros_por_ciclo = 50
    ciclos_necesarios = (registros_pendientes + registros_por_ciclo - 1) // registros_por_ciclo
    
    print(f"Registros sin procesar: {registros_pendientes:,}")
    print(f"Registros por ciclo: {registros_por_ciclo}")
    print(f"Ciclos necesarios: {ciclos_necesarios}")
    print(f"Límite actual en spider_garantias.py: 50 ciclos")
    
    if ciclos_necesarios > 50:
        print(f"\n⚠️  PROBLEMA DETECTADO:")
        print(f"    Se necesitan {ciclos_necesarios} ciclos pero el límite es 50")
        print(f"    El spider solo puede procesar {50 * registros_por_ciclo:,} registros")
        print(f"    Faltan por procesar: {registros_pendientes:,} registros")
    
    # 7. Análisis temporal
    print("\n\n7. ANÁLISIS POR FECHA DE ADJUDICACIÓN:")
    print("-"*100)
    cursor.execute("""
        SELECT 
            DATE_FORMAT(fecha_adjudicacion, '%Y-%m') as mes,
            COUNT(*) as total,
            SUM(CASE WHEN entidad_financiera IS NULL OR entidad_financiera = '' THEN 1 ELSE 0 END) as sin_procesar,
            ROUND(SUM(CASE WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_procesado
        FROM Licitaciones_Adjudicaciones
        WHERE fecha_adjudicacion IS NOT NULL
        GROUP BY mes
        ORDER BY mes DESC
        LIMIT 12
    """)
    
    print(f"{'MES':<15} {'TOTAL':<10} {'SIN PROCESAR':<15} {'% PROCESADO':<12}")
    print("-"*100)
    for row in cursor.fetchall():
        print(f"{row[0] or 'NULL':<15} {row[1]:<10} {row[2]:<15} {row[3]:<12}%")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*100)
    print("FIN DE AUDITORÍA")
    print("="*100)

if __name__ == "__main__":
    main()
