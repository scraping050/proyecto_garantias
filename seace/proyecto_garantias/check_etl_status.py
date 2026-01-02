import mysql.connector
from config.secrets_manager import get_db_config

try:
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    # Total en Detalle_Consorcios
    cursor.execute('SELECT COUNT(*) FROM Detalle_Consorcios')
    total_detalle = cursor.fetchone()[0]
    print(f'📊 Total registros en Detalle_Consorcios: {total_detalle}')
    
    # Estados en ETL_Consorcios_Log
    cursor.execute('SELECT estado, COUNT(*) FROM ETL_Consorcios_Log GROUP BY estado')
    print('\n📋 Estados ETL_Consorcios_Log:')
    for estado, cantidad in cursor.fetchall():
        print(f'   {estado}: {cantidad}')
    
    # Total procesados
    cursor.execute('SELECT COUNT(*) FROM ETL_Consorcios_Log')
    total_procesados = cursor.fetchone()[0]
    print(f'\n✅ Total contratos procesados: {total_procesados}')
    
    # Algunos ejemplos de consorcios encontrados
    cursor.execute('SELECT id_contrato, nombre_miembro, porcentaje_participacion FROM Detalle_Consorcios LIMIT 10')
    ejemplos = cursor.fetchall()
    if ejemplos:
        print('\n🎯 Ejemplos de consorcios encontrados:')
        for id_cont, nombre, porc in ejemplos:
            print(f'   Contrato {id_cont}: {nombre} ({porc}%)')
    
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')
