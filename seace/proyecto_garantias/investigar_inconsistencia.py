# Script para investigar la inconsistencia de estados
import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='garantias_seace'
    )
    
    cursor = conn.cursor()
    
    print("=" * 80)
    print("INVESTIGACION: INCONSISTENCIA DE ESTADOS")
    print("=" * 80)
    
    # 1. Buscar registros con estado_proceso = "ADJUDICADO"
    print("\n1. REGISTROS CON estado_proceso = 'ADJUDICADO'")
    print("-" * 80)
    
    sql = """
        SELECT c.id_convocatoria, c.nomenclatura, c.estado_proceso, 
               c.fecha_publicacion, c.archivo_origen,
               COUNT(a.id_adjudicacion) as num_adjudicaciones
        FROM Licitaciones_Cabecera c
        LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
        WHERE c.estado_proceso = 'ADJUDICADO'
        GROUP BY c.id_convocatoria, c.nomenclatura, c.estado_proceso, c.fecha_publicacion, c.archivo_origen
        LIMIT 10
    """
    cursor.execute(sql)
    
    print(f"\n{'ID Convocatoria':<20} {'Nomenclatura':<30} {'Fecha':<12} {'# Adj':>6} {'Archivo':<20}")
    print("-" * 80)
    
    adjudicados = []
    for row in cursor.fetchall():
        print(f"{row[0]:<20} {row[1][:28]:<30} {str(row[3]):<12} {row[5]:>6} {row[4]:<20}")
        adjudicados.append(row[0])
    
    # 2. Ver el JSON original de uno de estos registros
    if adjudicados:
        print(f"\n2. ANALIZANDO ARCHIVO ORIGEN DEL PRIMER REGISTRO")
        print("-" * 80)
        
        sql = """
            SELECT archivo_origen, fecha_publicacion, last_update
            FROM Licitaciones_Cabecera
            WHERE id_convocatoria = %s
        """
        cursor.execute(sql, (adjudicados[0],))
        row = cursor.fetchone()
        
        print(f"\nID Convocatoria: {adjudicados[0]}")
        print(f"Archivo origen: {row[0]}")
        print(f"Fecha publicacion: {row[1]}")
        print(f"Ultima actualizacion: {row[2]}")
        
        # Extraer fecha del archivo
        archivo = row[0]
        if archivo:
            fecha_archivo = archivo.split('_')[0]  # Ejemplo: 2024-01_seace_v3.json
            print(f"Fecha del archivo: {fecha_archivo}")
    
    # 3. Comparar estados entre archivos
    print(f"\n3. DISTRIBUCION DE ESTADOS POR ARCHIVO")
    print("-" * 80)
    
    sql = """
        SELECT archivo_origen, estado_proceso, COUNT(*) as cantidad
        FROM Licitaciones_Cabecera
        WHERE estado_proceso IN ('ADJUDICADO', 'CONSENTIDO', 'CONTRATADO')
        GROUP BY archivo_origen, estado_proceso
        ORDER BY archivo_origen, cantidad DESC
        LIMIT 30
    """
    cursor.execute(sql)
    
    print(f"\n{'Archivo':<25} {'Estado':<20} {'Cantidad':>10}")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"{row[0]:<25} {row[1]:<20} {row[2]:>10,}")
    
    # 4. Verificar si hay actualizaciones
    print(f"\n4. VERIFICANDO LOGICA DE ACTUALIZACION")
    print("-" * 80)
    
    sql = """
        SELECT 
            estado_proceso,
            COUNT(*) as total,
            COUNT(DISTINCT archivo_origen) as num_archivos,
            MIN(fecha_publicacion) as fecha_min,
            MAX(fecha_publicacion) as fecha_max
        FROM Licitaciones_Cabecera
        WHERE estado_proceso IN ('ADJUDICADO', 'CONSENTIDO', 'CONTRATADO')
        GROUP BY estado_proceso
    """
    cursor.execute(sql)
    
    print(f"\n{'Estado':<20} {'Total':>8} {'Archivos':>10} {'Fecha Min':<12} {'Fecha Max':<12}")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"{row[0]:<20} {row[1]:>8,} {row[2]:>10} {str(row[3]):<12} {str(row[4]):<12}")
    
    # 5. Buscar duplicados (mismo id_convocatoria en múltiples archivos)
    print(f"\n5. VERIFICANDO DUPLICADOS EN MULTIPLES ARCHIVOS")
    print("-" * 80)
    
    sql = """
        SELECT id_convocatoria, COUNT(DISTINCT archivo_origen) as num_archivos
        FROM Licitaciones_Cabecera
        GROUP BY id_convocatoria
        HAVING num_archivos > 1
        LIMIT 5
    """
    cursor.execute(sql)
    
    duplicados = cursor.fetchall()
    if duplicados:
        print(f"\nSe encontraron {len(duplicados)} registros en múltiples archivos")
        print("Esto indica que NO se están actualizando los estados")
    else:
        print("\nNo se encontraron duplicados - Los registros se actualizan correctamente")
    
    # 6. Analizar la lógica ON DUPLICATE KEY UPDATE
    print(f"\n6. PROBLEMA IDENTIFICADO")
    print("-" * 80)
    print("""
El problema es que:

1. Los archivos JSON del SEACE son SNAPSHOTS mensuales
2. Cada archivo contiene el estado ACTUAL de las licitaciones en ese mes
3. Una licitación puede estar:
   - Enero 2024: ADJUDICADO
   - Febrero 2024: CONSENTIDO  
   - Marzo 2024: CONTRATADO

4. La cláusula ON DUPLICATE KEY UPDATE en cargador.py (línea 218-220):
   - SÍ actualiza: categoria, tipo_procedimiento, monto_estimado
   - NO actualiza: estado_proceso
   
5. Por eso los registros quedan con el estado del PRIMER archivo procesado
   y no se actualizan con archivos posteriores.

SOLUCION: Modificar ON DUPLICATE KEY UPDATE para actualizar estado_proceso
    """)
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("INVESTIGACION COMPLETADA")
    print("=" * 80)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
