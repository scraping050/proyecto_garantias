"""
Script para probar el ETL modificado con un archivo pequeño
"""
import sys
import os

# Agregar path del motor ETL
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '1_motor_etl'))

from cargador import procesar_archivo, obtener_conexion
import mysql.connector

print("=" * 100)
print("PRUEBA: ETL con Tabla Contratos")
print("=" * 100)

# Obtener conexión
conn = obtener_conexion()

# Procesar solo el primer archivo (más pequeño)
archivo_prueba = r"c:\laragon\www\proyecto_garantias\1_database\2024-01_seace_v3.json"

print(f"\nProcesando archivo de prueba: {os.path.basename(archivo_prueba)}")
print("-" * 100)

try:
    registros = procesar_archivo(archivo_prueba, conn, os.path.basename(archivo_prueba))
    print(f"\nOK - Procesados {registros} registros")
    
    # Verificar contratos insertados
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM Contratos")
    total_contratos = cursor.fetchone()[0]
    print(f"\nContratos en BD: {total_contratos}")
    
    # Mostrar ejemplos
    cursor.execute("""
        SELECT c.id_contrato, c.id_adjudicacion, c.fecha_firma, c.estado_contrato
        FROM Contratos c
        LIMIT 10
    """)
    
    print("\nEjemplos de contratos:")
    print("-" * 100)
    for row in cursor.fetchall():
        print(f"  Contrato: {row[0]:15} | Adjudicacion: {row[1]:20} | Fecha: {row[2]} | Estado: {row[3]}")
    
    # Verificar adjudicaciones con contrato
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        WHERE id_contrato IS NOT NULL AND id_contrato != ''
    """)
    adj_con_contrato = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Adjudicaciones")
    total_adj = cursor.fetchone()[0]
    
    print(f"\nAdjudicaciones con id_contrato: {adj_con_contrato} de {total_adj}")
    
    cursor.close()
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    if conn.is_connected():
        conn.close()

print("\n" + "=" * 100)
print("PRUEBA COMPLETADA")
print("=" * 100)
