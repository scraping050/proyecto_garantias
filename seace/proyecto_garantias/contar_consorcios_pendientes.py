import mysql.connector
import sys
import os

# Usar configuración del proyecto
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'config'))
from secrets_manager import get_db_config

try:
    DB_CONFIG = get_db_config()
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Total de consorcios
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE ganador_nombre LIKE '%CONSORCIO%' 
          AND id_contrato IS NOT NULL 
          AND id_contrato != ''
    """)
    total = cursor.fetchone()[0]
    
    # Ya procesados
    cursor.execute("SELECT COUNT(DISTINCT id_contrato) FROM Detalle_Consorcios")
    procesados = cursor.fetchone()[0]
    
    # Pendientes
    pendientes = total - procesados
    
    print("=" * 60)
    print("REPORTE DE CONSORCIOS")
    print("=" * 60)
    print(f"Total consorcios en BD:      {total:,}")
    print(f"Ya procesados con OCR:       {procesados:,}")
    print(f"Pendientes de procesar:      {pendientes:,}")
    print("=" * 60)
    
    # Cálculo de costos
    costo_primera_pasada = pendientes * 0.0154
    costo_segunda_pasada = (pendientes * 0.02) * 0.0308  # 2% fallan
    costo_total = costo_primera_pasada + costo_segunda_pasada
    
    print("\nESTIMACIÓN DE COSTOS:")
    print("=" * 60)
    print(f"Primera pasada (10 pág):     ${costo_primera_pasada:.2f} USD")
    print(f"Segunda pasada (20 pág):     ${costo_segunda_pasada:.2f} USD")
    print(f"COSTO TOTAL ESTIMADO:        ${costo_total:.2f} USD")
    print("=" * 60)
    
    # Tiempo estimado
    tiempo_horas = (pendientes * 30) / 3600  # 30 seg por contrato, convertir a horas
    print(f"\nTiempo estimado:             {tiempo_horas:.1f} horas (~{tiempo_horas/24:.1f} días)")
    print("=" * 60)
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
