"""
Script para crear la tabla de auditoría del ETL de Consorcios
Ejecutar una sola vez antes de usar el ETL
"""

import mysql.connector
import sys
import os

# Agregar path de config
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'config'))
from secrets_manager import get_db_config

def crear_tabla_auditoria():
    """Crea la tabla ETL_Consorcios_Log para auditoría"""
    
    sql_tabla = """
    CREATE TABLE IF NOT EXISTS ETL_Consorcios_Log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_contrato VARCHAR(20) NOT NULL,
        fecha_proceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        estado ENUM('EXITO', 'ERROR', 'PARCIAL', 'SALTADO') NOT NULL,
        miembros_encontrados INT DEFAULT 0,
        miembros_guardados INT DEFAULT 0,
        error_tipo VARCHAR(100),
        error_mensaje TEXT,
        tokens_input INT DEFAULT 0,
        tokens_output INT DEFAULT 0,
        costo_usd DECIMAL(10,6) DEFAULT 0,
        tiempo_procesamiento_seg INT DEFAULT 0,
        metodo_extraccion ENUM('TEXTO_NORMAL', 'OCR', 'NINGUNO') DEFAULT 'NINGUNO',
        
        INDEX idx_contrato (id_contrato),
        INDEX idx_fecha (fecha_proceso),
        INDEX idx_estado (estado)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    sql_vista = """
    CREATE OR REPLACE VIEW v_etl_consorcios_resumen AS
    SELECT 
        DATE(fecha_proceso) as fecha,
        COUNT(*) as total_procesados,
        SUM(CASE WHEN estado = 'EXITO' THEN 1 ELSE 0 END) as exitosos,
        SUM(CASE WHEN estado = 'ERROR' THEN 1 ELSE 0 END) as errores,
        SUM(CASE WHEN estado = 'PARCIAL' THEN 1 ELSE 0 END) as parciales,
        SUM(CASE WHEN estado = 'SALTADO' THEN 1 ELSE 0 END) as saltados,
        ROUND(SUM(CASE WHEN estado = 'EXITO' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as tasa_exito,
        SUM(miembros_encontrados) as total_miembros,
        SUM(tokens_input) as total_tokens_in,
        SUM(tokens_output) as total_tokens_out,
        SUM(costo_usd) as costo_total,
        ROUND(AVG(tiempo_procesamiento_seg), 2) as tiempo_promedio_seg
    FROM ETL_Consorcios_Log
    GROUP BY DATE(fecha_proceso)
    ORDER BY fecha DESC
    """
    
    try:
        print("Conectando a la base de datos...")
        DB_CONFIG = get_db_config()
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Creando tabla ETL_Consorcios_Log...")
        cursor.execute(sql_tabla)
        print("✅ Tabla creada exitosamente")
        
        print("Creando vista v_etl_consorcios_resumen...")
        cursor.execute(sql_vista)
        print("✅ Vista creada exitosamente")
        
        conn.commit()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("="*60)
        print("La tabla de auditoría está lista para usar")
        print("\nAhora puedes ejecutar: python etl_consorcios_openai.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    crear_tabla_auditoria()
