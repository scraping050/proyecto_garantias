# Script para verificar el estado de la base de datos y limpiar control de cargas
import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='garantias_seace'
    )
    
    cursor = conn.cursor()
    
    # Verificar registros en tablas
    print("=" * 60)
    print("ESTADO ACTUAL DE LA BASE DE DATOS")
    print("=" * 60)
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
    count_cab = cursor.fetchone()[0]
    print(f"\nLicitaciones_Cabecera: {count_cab:,} registros")
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    count_adj = cursor.fetchone()[0]
    print(f"Licitaciones_Adjudicaciones: {count_adj:,} registros")
    
    cursor.execute("SELECT COUNT(*) FROM Detalle_Consorcios")
    count_con = cursor.fetchone()[0]
    print(f"Detalle_Consorcios: {count_con:,} registros")
    
    cursor.execute("SELECT COUNT(*) FROM control_cargas")
    count_ctrl = cursor.fetchone()[0]
    print(f"control_cargas: {count_ctrl:,} registros")
    
    # Mostrar archivos en control_cargas
    if count_ctrl > 0:
        print(f"\n{'=' * 60}")
        print("ARCHIVOS EN CONTROL DE CARGAS")
        print("=" * 60)
        cursor.execute("SELECT nombre_archivo, estado, registros_procesados FROM control_cargas LIMIT 10")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} ({row[2]} registros)")
    
    # Limpiar tabla de control para forzar recarga
    print(f"\n{'=' * 60}")
    print("LIMPIANDO CONTROL DE CARGAS...")
    print("=" * 60)
    
    cursor.execute("DELETE FROM control_cargas")
    conn.commit()
    print(f"OK - {cursor.rowcount} registros eliminados de control_cargas")
    print("\nAhora puedes ejecutar el proyecto nuevamente para cargar todos los datos")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
