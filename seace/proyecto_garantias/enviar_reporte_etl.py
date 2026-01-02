"""
Generador de Reportes ETL por Email
Envía el estado completo del monitoreo ETL a Gmail con formato HTML profesional
"""
import mysql.connector
import sys
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.insert(0, 'config')
from secrets_manager import get_db_config, config

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
        'icono': '📥',
        'frecuencia_esperada_dias': 30
    },
    'cargador.py': {
        'nombre': 'Cargador MySQL',
        'descripcion': 'Carga datos JSON a MySQL',
        'critico': True,
        'icono': '💾',
        'frecuencia_esperada_dias': 30
    },
    'spider_garantias.py': {
        'nombre': 'Spider Garantías',
        'descripcion': 'Enriquece con datos de entidades financieras',
        'critico': True,
        'icono': '🕷️',
        'frecuencia_esperada_dias': 7
    },
    'etl_consorcios_ai.py': {
        'nombre': 'ETL Consorcios (Gemini)',
        'descripcion': 'Procesa PDFs de consorcios con IA',
        'critico': False,
        'icono': '🤖',
        'frecuencia_esperada_dias': 90
    },
    'etl_consorcios_groq.py': {
        'nombre': 'ETL Consorcios (Groq)',
        'descripcion': 'Procesa PDFs de consorcios con IA (alternativo)',
        'critico': False,
        'icono': '🤖',
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

def obtener_datos_reporte():
    """Obtiene todos los datos necesarios para el reporte"""
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    datos = {}
    
    for script_file, info in SCRIPTS_ETL.items():
        # Última ejecución
        cursor.execute("""
            SELECT execution_start, execution_end, status, records_processed, 
                   error_message, execution_time_seconds
            FROM etl_execution_log
            WHERE script_name = %s
            ORDER BY execution_start DESC
            LIMIT 1
        """, (script_file,))
        
        ultima = cursor.fetchone()
        
        # Estadísticas últimos 7 días
        fecha_inicio = datetime.now() - timedelta(days=7)
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
        """, (script_file, fecha_inicio))
        
        stats = cursor.fetchone()
        
        datos[script_file] = {
            'info': info,
            'ultima': ultima,
            'stats': stats
        }
    
    cursor.close()
    conn.close()
    
    return datos

def generar_html_reporte(datos):
    """Genera el HTML del reporte"""
    
    # Calcular estado general
    alertas = []
    scripts_ok = 0
    scripts_warning = 0
    scripts_error = 0
    
    for script_file, data in datos.items():
        info = data['info']
        ultima = data['ultima']
        
        if ultima:
            fecha_exec, fecha_fin, estado, registros, error, tiempo = ultima
            dias_desde = (datetime.now() - fecha_exec).days
            
            if estado == 'FAILED':
                scripts_error += 1
                alertas.append(f"{info['nombre']}: Última ejecución FALLÓ")
            elif dias_desde > info['frecuencia_esperada_dias']:
                scripts_warning += 1
                if info['critico']:
                    alertas.append(f"{info['nombre']}: {dias_desde} días sin ejecutar")
            else:
                scripts_ok += 1
        else:
            scripts_warning += 1
            if info['critico']:
                alertas.append(f"{info['nombre']}: Nunca se ha ejecutado")
    
    # Determinar color del estado general
    if scripts_error > 0:
        estado_general = "CRÍTICO"
        color_estado = "#dc3545"
        icono_estado = "❌"
    elif scripts_warning > 0:
        estado_general = "ATENCIÓN"
        color_estado = "#ffc107"
        icono_estado = "⚠️"
    else:
        estado_general = "SALUDABLE"
        color_estado = "#28a745"
        icono_estado = "✅"
    
    # Generar HTML de scripts
    html_scripts = ""
    
    for script_file, data in datos.items():
        info = data['info']
        ultima = data['ultima']
        stats = data['stats']
        
        # Card de script
        if ultima:
            fecha_exec, fecha_fin, estado, registros, error, tiempo = ultima
            dias_desde = (datetime.now() - fecha_exec).days
            
            # Determinar color
            if estado == 'FAILED':
                color_card = "#ffebee"
                color_border = "#dc3545"
                estado_texto = "❌ FALLÓ"
            elif dias_desde > info['frecuencia_esperada_dias']:
                color_card = "#fff3cd"
                color_border = "#ffc107"
                estado_texto = f"⚠️ {dias_desde}d sin ejecutar"
            else:
                color_card = "#d4edda"
                color_border = "#28a745"
                estado_texto = "✅ OK"
            
            fecha_str = fecha_exec.strftime('%Y-%m-%d %H:%M')
            registros_str = f"{registros:,}" if registros else "0"
            tiempo_str = f"{tiempo:.1f}s" if tiempo else "N/A"
        else:
            color_card = "#fff3cd"
            color_border = "#ffc107"
            estado_texto = "⚠️ Nunca ejecutado"
            fecha_str = "N/A"
            registros_str = "0"
            tiempo_str = "N/A"
        
        # Estadísticas
        if stats and stats[0] > 0:
            total, exitosas, fallidas, tiempo_prom, total_reg = stats
            tasa_exito = (exitosas / total * 100) if total > 0 else 0
            stats_html = f"""
                <div style="margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                    <strong>Últimos 7 días:</strong><br>
                    Ejecuciones: {total} | Exitosas: {exitosas} | Fallidas: {fallidas}<br>
                    Tasa de éxito: {tasa_exito:.1f}% | Registros procesados: {total_reg:,}
                </div>
            """
        else:
            stats_html = """
                <div style="margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                    <em>Sin ejecuciones en los últimos 7 días</em>
                </div>
            """
        
        html_scripts += f"""
        <div style="margin-bottom: 20px; padding: 15px; background: {color_card}; border-left: 5px solid {color_border}; border-radius: 5px;">
            <h3 style="margin: 0 0 10px 0; color: #333;">
                {info['icono']} {info['nombre']}
                <span style="float: right; font-size: 14px;">{estado_texto}</span>
            </h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">{info['descripcion']}</p>
            <div style="margin-top: 10px; font-size: 13px; color: #555;">
                <strong>Última ejecución:</strong> {fecha_str}<br>
                <strong>Registros procesados:</strong> {registros_str}<br>
                <strong>Tiempo de ejecución:</strong> {tiempo_str}
            </div>
            {stats_html}
        </div>
        """
    
    # Generar HTML de alertas
    if alertas:
        html_alertas = "<ul style='margin: 10px 0; padding-left: 20px;'>"
        for alerta in alertas:
            html_alertas += f"<li style='margin: 5px 0; color: #721c24;'>{alerta}</li>"
        html_alertas += "</ul>"
    else:
        html_alertas = "<p style='color: #155724;'>✅ No hay alertas críticas</p>"
    
    # HTML completo
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
        
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
            <h1 style="margin: 0; font-size: 28px;">📊 Reporte ETL - Sistema SEACE</h1>
            <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">
                {datetime.now().strftime('%d de %B de %Y - %H:%M')}
            </p>
        </div>
        
        <!-- Estado General -->
        <div style="background: {color_card}; border: 2px solid {color_estado}; border-radius: 10px; padding: 20px; margin-bottom: 30px; text-align: center;">
            <h2 style="margin: 0 0 10px 0; color: {color_estado}; font-size: 24px;">
                {icono_estado} Estado General: {estado_general}
            </h2>
            <div style="display: flex; justify-content: space-around; margin-top: 20px; flex-wrap: wrap;">
                <div style="text-align: center; min-width: 100px; margin: 10px;">
                    <div style="font-size: 32px; font-weight: bold; color: #28a745;">{scripts_ok}</div>
                    <div style="font-size: 12px; color: #666;">Scripts OK</div>
                </div>
                <div style="text-align: center; min-width: 100px; margin: 10px;">
                    <div style="font-size: 32px; font-weight: bold; color: #ffc107;">{scripts_warning}</div>
                    <div style="font-size: 12px; color: #666;">Advertencias</div>
                </div>
                <div style="text-align: center; min-width: 100px; margin: 10px;">
                    <div style="font-size: 32px; font-weight: bold; color: #dc3545;">{scripts_error}</div>
                    <div style="font-size: 12px; color: #666;">Errores</div>
                </div>
            </div>
        </div>
        
        <!-- Alertas Críticas -->
        <div style="background: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; margin-bottom: 30px; border-radius: 5px;">
            <h3 style="margin: 0 0 10px 0; color: #856404;">⚠️ Alertas Críticas</h3>
            {html_alertas}
        </div>
        
        <!-- Scripts -->
        <h2 style="color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 20px;">
            📋 Estado de Scripts
        </h2>
        {html_scripts}
        
        <!-- Footer -->
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 12px;">
            <p>Este es un reporte automático generado por el Sistema de Monitoreo ETL</p>
            <p>Para más detalles, ejecuta: <code style="background: #f4f4f4; padding: 2px 6px; border-radius: 3px;">python monitor_etl.py</code></p>
        </div>
        
    </body>
    </html>
    """
    
    return html

def enviar_reporte_email(html_content, asunto=None):
    """Envía el reporte por email"""
    
    # Obtener configuración de email
    email_config = config.get_email_config()
    
    if not email_config.user or not email_config.password:
        print("❌ Error: No hay credenciales de email configuradas")
        print("   Configura las credenciales en el archivo .env")
        return False
    
    try:
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['From'] = email_config.user
        msg['To'] = email_config.to
        
        if asunto is None:
            asunto = f"[ETL] Reporte de Monitoreo - {datetime.now().strftime('%d/%m/%Y')}"
        
        msg['Subject'] = asunto
        
        # Adjuntar HTML
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Enviar
        print(f"📧 Enviando reporte a {email_config.to}...")
        
        server = smtplib.SMTP(email_config.host, email_config.port)
        server.starttls()
        server.login(email_config.user, email_config.password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Reporte enviado exitosamente a {email_config.to}")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        return False

def main():
    print("="*80)
    print("GENERADOR DE REPORTES ETL POR EMAIL")
    print("="*80)
    
    # Crear tabla si no existe
    try:
        crear_tabla_logs()
        print("✅ Tabla de logs verificada")
    except Exception as e:
        print(f"⚠️  Advertencia: {e}")
    
    # Obtener datos
    print("\n📊 Recopilando datos del monitoreo...")
    datos = obtener_datos_reporte()
    
    # Generar HTML
    print("📝 Generando reporte HTML...")
    html = generar_html_reporte(datos)
    
    # Guardar HTML localmente (opcional, para preview)
    with open('reporte_etl_preview.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("💾 Preview guardado en: reporte_etl_preview.html")
    
    # Enviar por email
    print("\n📧 Enviando reporte por email...")
    if enviar_reporte_email(html):
        print("\n✅ ¡Reporte enviado exitosamente!")
    else:
        print("\n❌ No se pudo enviar el reporte")
        print("   Puedes ver el preview en: reporte_etl_preview.html")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
