"""
Sistema de Monitoreo ETL
Muestra el estado actual de todos los scripts de scraping/carga
"""
import mysql.connector
import sys
from datetime import datetime, timedelta

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

# Configurar encoding UTF-8 para Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Scripts a monitorear
SCRIPTS_ETL = {
    'descargador.py': {
        'nombre': 'Descargador SEACE',
        'descripcion': 'Descarga archivos JSON de SEACE',
        'critico': True,
        'frecuencia_esperada_dias': 30  # Se espera que se ejecute al menos una vez al mes
    },
    'cargador.py': {
        'nombre': 'Cargador MySQL',
        'descripcion': 'Carga datos JSON a MySQL',
        'critico': True,
        'frecuencia_esperada_dias': 30
    },
    'spider_garantias.py': {
        'nombre': 'Spider Garantías',
        'descripcion': 'Enriquece con datos de entidades financieras',
        'critico': True,
        'frecuencia_esperada_dias': 7
    },
    'etl_consorcios_ai.py': {
        'nombre': 'ETL Consorcios (Gemini)',
        'descripcion': 'Procesa PDFs de consorcios con IA',
        'critico': False,
        'frecuencia_esperada_dias': 90
    },
    'etl_consorcios_groq.py': {
        'nombre': 'ETL Consorcios (Groq)',
        'descripcion': 'Procesa PDFs de consorcios con IA (alternativo)',
        'critico': False,
        'frecuencia_esperada_dias': 90
    }
}

def crear_tabla_logs():
    """Crea la tabla de logs si no existe"""
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS etl_execution_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            script_name VARCHAR(100) NOT NULL,
            execution_start DATETIME NOT NULL,
            execution_end DATETIME,
            status ENUM('RUNNING', 'SUCCESS', 'FAILED') NOT NULL,
            records_processed INT DEFAULT 0,
            error_message TEXT,
            execution_time_seconds DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_script_start (script_name, execution_start),
            INDEX idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def obtener_ultima_ejecucion(script_name):
    """Obtiene la última ejecución de un script"""
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT execution_start, execution_end, status, records_processed, 
               error_message, execution_time_seconds
        FROM etl_execution_log
        WHERE script_name = %s
        ORDER BY execution_start DESC
        LIMIT 1
    """, (script_name,))
    
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return resultado

def obtener_estadisticas(script_name, dias=7):
    """Obtiene estadísticas de ejecuciones recientes"""
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    fecha_inicio = datetime.now() - timedelta(days=dias)
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total_ejecuciones,
            SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as exitosas,
            SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as fallidas,
            AVG(execution_time_seconds) as tiempo_promedio,
            SUM(records_processed) as total_registros
        FROM etl_execution_log
        WHERE script_name = %s
          AND execution_start >= %s
    """, (script_name, fecha_inicio))
    
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return resultado

def main():
    print("="*120)
    print("MONITOR ETL - Estado de Scripts de Scraping/Carga")
    print("="*120)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Crear tabla si no existe
    try:
        crear_tabla_logs()
    except Exception as e:
        print(f"\n⚠️  Advertencia: No se pudo crear tabla de logs: {e}")
        print("   Continuando con información limitada...\n")
    
    # Estado de cada script
    print("\n1. ESTADO ACTUAL DE SCRIPTS:")
    print("-"*120)
    print(f"{'SCRIPT':<30} {'ÚLTIMA EJECUCIÓN':<20} {'ESTADO':<15} {'REGISTROS':<12} {'TIEMPO':<10} {'ALERTA':<20}")
    print("-"*120)
    
    alertas = []
    
    for script_file, info in SCRIPTS_ETL.items():
        try:
            ultima = obtener_ultima_ejecucion(script_file)
            
            if ultima:
                fecha_exec, fecha_fin, estado, registros, error, tiempo = ultima
                
                # Calcular días desde última ejecución
                dias_desde = (datetime.now() - fecha_exec).days
                
                # Determinar alerta
                alerta = ""
                if estado == 'FAILED':
                    alerta = "❌ FALLÓ"
                    alertas.append(f"{info['nombre']}: Última ejecución FALLÓ")
                elif dias_desde > info['frecuencia_esperada_dias']:
                    alerta = f"⚠️  {dias_desde}d sin ejecutar"
                    if info['critico']:
                        alertas.append(f"{info['nombre']}: {dias_desde} días sin ejecutar (crítico)")
                else:
                    alerta = "✅ OK"
                
                # Formatear salida
                fecha_str = fecha_exec.strftime('%Y-%m-%d %H:%M')
                estado_str = estado
                registros_str = f"{registros:,}" if registros else "0"
                tiempo_str = f"{tiempo:.1f}s" if tiempo else "N/A"
                
                print(f"{info['nombre']:<30} {fecha_str:<20} {estado_str:<15} {registros_str:<12} {tiempo_str:<10} {alerta:<20}")
            else:
                alerta_msg = "⚠️  Nunca ejecutado"
                if info['critico']:
                    alertas.append(f"{info['nombre']}: Nunca se ha ejecutado (crítico)")
                print(f"{info['nombre']:<30} {'N/A':<20} {'N/A':<15} {'0':<12} {'N/A':<10} {alerta_msg:<20}")
                
        except Exception as e:
            print(f"{info['nombre']:<30} {'ERROR':<20} {'ERROR':<15} {'0':<12} {'N/A':<10} {str(e)[:20]:<20}")
    
    # Estadísticas de los últimos 7 días
    print("\n2. ESTADÍSTICAS (Últimos 7 días):")
    print("-"*120)
    print(f"{'SCRIPT':<30} {'EJECUCIONES':<15} {'EXITOSAS':<12} {'FALLIDAS':<12} {'TIEMPO PROM.':<15} {'REGISTROS':<15}")
    print("-"*120)
    
    for script_file, info in SCRIPTS_ETL.items():
        try:
            stats = obtener_estadisticas(script_file, dias=7)
            
            if stats and stats[0] > 0:
                total, exitosas, fallidas, tiempo_prom, total_reg = stats
                
                tiempo_str = f"{tiempo_prom:.1f}s" if tiempo_prom else "N/A"
                reg_str = f"{total_reg:,}" if total_reg else "0"
                
                print(f"{info['nombre']:<30} {total:<15} {exitosas:<12} {fallidas:<12} {tiempo_str:<15} {reg_str:<15}")
            else:
                print(f"{info['nombre']:<30} {'0':<15} {'0':<12} {'0':<12} {'N/A':<15} {'0':<15}")
                
        except Exception as e:
            print(f"{info['nombre']:<30} {'ERROR':<15} {'-':<12} {'-':<12} {'-':<15} {str(e)[:15]:<15}")
    
    # Alertas críticas
    if alertas:
        print("\n3. ALERTAS CRÍTICAS:")
        print("-"*120)
        for alerta in alertas:
            print(f"  ⚠️  {alerta}")
    else:
        print("\n3. ALERTAS CRÍTICAS:")
        print("-"*120)
        print("  ✅ No hay alertas críticas")
    
    # Resumen
    print("\n4. RESUMEN:")
    print("-"*120)
    total_scripts = len(SCRIPTS_ETL)
    scripts_criticos = sum(1 for info in SCRIPTS_ETL.values() if info['critico'])
    
    print(f"Total de scripts monitoreados: {total_scripts}")
    print(f"Scripts críticos: {scripts_criticos}")
    print(f"Alertas activas: {len(alertas)}")
    
    if len(alertas) == 0:
        print("\n✅ ESTADO GENERAL: SALUDABLE")
    elif len(alertas) <= 2:
        print("\n⚠️  ESTADO GENERAL: ATENCIÓN REQUERIDA")
    else:
        print("\n❌ ESTADO GENERAL: CRÍTICO")
    
    print("\n" + "="*120)
    print("FIN DEL REPORTE")
    print("="*120)

if __name__ == "__main__":
    main()
