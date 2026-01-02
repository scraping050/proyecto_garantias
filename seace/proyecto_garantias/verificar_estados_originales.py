# Script para verificar estados originales después de la recarga
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
    print("VERIFICACION: ESTADOS ORIGINALES (SIN TRADUCCIONES)")
    print("=" * 80)
    
    # 1. Contar registros
    print("\n1. RESUMEN DE DATOS")
    print("-" * 80)
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
    count_cab = cursor.fetchone()[0]
    print(f"Licitaciones: {count_cab:,}")
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    count_adj = cursor.fetchone()[0]
    print(f"Adjudicaciones: {count_adj:,}")
    
    # 2. Ver distribución de estados
    print("\n2. DISTRIBUCION DE ESTADOS (ORIGINALES)")
    print("-" * 80)
    
    sql = """
        SELECT estado_proceso, COUNT(*) as cantidad,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Licitaciones_Cabecera), 2) as porcentaje
        FROM Licitaciones_Cabecera
        GROUP BY estado_proceso
        ORDER BY cantidad DESC
    """
    cursor.execute(sql)
    
    print(f"\n{'Estado Proceso (Original)':<40} {'Cantidad':>10} {'Porcentaje':>12}")
    print("-" * 80)
    
    estados_ingles = 0
    estados_espanol = 0
    
    for row in cursor.fetchall():
        estado = row[0]
        cantidad = row[1]
        porcentaje = row[2]
        
        # Detectar si es inglés o español
        estados_ingles_lista = ['ACTIVE', 'COMPLETE', 'AWARDED', 'CANCELLED', 'UNSUCCESSFUL', 'WITHDRAWN', 'PLANNED']
        if estado in estados_ingles_lista:
            estados_ingles += cantidad
            marcador = "[EN]"
        else:
            estados_espanol += cantidad
            marcador = "[ES]"
        
        print(f"{estado:<40} {cantidad:>10,} {porcentaje:>11.2f}% {marcador}")
    
    print("-" * 80)
    print(f"{'TOTAL':<40} {count_cab:>10,}")
    
    # 3. Resumen de idiomas
    print("\n3. RESUMEN POR IDIOMA")
    print("-" * 80)
    print(f"Estados en INGLES: {estados_ingles:,} ({estados_ingles*100/count_cab:.2f}%)")
    print(f"Estados en ESPAÑOL: {estados_espanol:,} ({estados_espanol*100/count_cab:.2f}%)")
    
    # 4. Comparación antes/después
    print("\n4. COMPARACION: ANTES vs DESPUES")
    print("-" * 80)
    print("""
ANTES (Con Traducciones):
- CONVOCADO: ~1,770 (traducido de 'active')
- CONTRATADO: ~4,625 (traducido de 'complete')
- ADJUDICADO: ~164 (traducido de 'awarded')

DESPUES (Estados Originales):
- ACTIVE: (ver arriba)
- COMPLETE: (ver arriba)
- AWARDED: (ver arriba)
- Estados en español: Sin cambios
    """)
    
    # 5. Verificar que no hay traducciones
    print("\n5. VERIFICACION: NO HAY TRADUCCIONES")
    print("-" * 80)
    
    estados_traducidos = ['CONVOCADO', 'CONTRATADO', 'CANCELADO', 'DESIERTO', 'NULO', 'PROGRAMADO']
    
    for estado in estados_traducidos:
        cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE estado_proceso = %s", (estado,))
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"[!] ADVERTENCIA: Encontrados {count} registros con estado '{estado}' (traducido)")
        else:
            print(f"[OK] No hay registros con estado '{estado}' (traducido)")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("VERIFICACION COMPLETADA")
    print("=" * 80)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
