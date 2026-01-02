"""
Generador de Reporte Visual HTML para ETL de Consorcios
Crea un dashboard interactivo con gráficos y tablas
"""

import mysql.connector
import sys
import os
from datetime import datetime
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from secrets_manager import get_db_config

def generar_reporte_html():
    """Genera un reporte HTML visual del ETL"""
    
    try:
        DB_CONFIG = get_db_config()
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 1. Resumen general
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN estado = 'EXITO' THEN 1 ELSE 0 END) as exitosos,
                SUM(CASE WHEN estado = 'ERROR' THEN 1 ELSE 0 END) as errores,
                SUM(CASE WHEN estado = 'PARCIAL' THEN 1 ELSE 0 END) as parciales,
                SUM(CASE WHEN estado = 'SALTADO' THEN 1 ELSE 0 END) as saltados,
                SUM(miembros_encontrados) as total_miembros,
                SUM(costo_usd) as costo_total,
                SUM(tokens_input + tokens_output) as tokens_totales
            FROM ETL_Consorcios_Log
        """)
        resumen = cursor.fetchone()
        
        # 2. Últimos 50 procesados
        cursor.execute("""
            SELECT id_contrato, fecha_proceso, estado, miembros_encontrados,
                   error_tipo, error_mensaje, costo_usd, metodo_extraccion
            FROM ETL_Consorcios_Log
            ORDER BY fecha_proceso DESC
            LIMIT 50
        """)
        ultimos = cursor.fetchall()
        
        # 3. Errores agrupados
        cursor.execute("""
            SELECT error_tipo, COUNT(*) as cantidad
            FROM ETL_Consorcios_Log
            WHERE estado = 'ERROR'
            GROUP BY error_tipo
            ORDER BY cantidad DESC
        """)
        errores_agrupados = cursor.fetchall()
        
        # 4. Resumen por día
        cursor.execute("SELECT * FROM v_etl_consorcios_resumen LIMIT 30")
        resumen_diario = cursor.fetchall()
        
        conn.close()
        
        # Generar HTML
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte ETL Consorcios - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #667eea;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .header .timestamp {{
            color: #666;
            font-size: 14px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}
        .stat-card .label {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .stat-card .value {{
            font-size: 36px;
            font-weight: bold;
            color: #333;
        }}
        .stat-card.success .value {{ color: #10b981; }}
        .stat-card.error .value {{ color: #ef4444; }}
        .stat-card.warning .value {{ color: #f59e0b; }}
        .stat-card.info .value {{ color: #3b82f6; }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 24px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}
        th {{
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}
        tr:hover {{
            background: #f9fafb;
        }}
        .badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }}
        .badge.success {{ background: #d1fae5; color: #065f46; }}
        .badge.error {{ background: #fee2e2; color: #991b1b; }}
        .badge.warning {{ background: #fef3c7; color: #92400e; }}
        .badge.info {{ background: #dbeafe; color: #1e40af; }}
        
        .error-msg {{
            font-size: 12px;
            color: #666;
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .cost {{
            font-weight: 600;
            color: #10b981;
        }}
        .chart-container {{
            margin: 20px 0;
            padding: 20px;
            background: #f9fafb;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Reporte ETL Consorcios</h1>
            <div class="timestamp">Generado: {datetime.now().strftime('%d de %B de %Y a las %H:%M:%S')}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card info">
                <div class="label">Total Procesados</div>
                <div class="value">{resumen['total'] or 0:,}</div>
            </div>
            <div class="stat-card success">
                <div class="label">Exitosos</div>
                <div class="value">{resumen['exitosos'] or 0:,}</div>
            </div>
            <div class="stat-card error">
                <div class="label">Errores</div>
                <div class="value">{resumen['errores'] or 0:,}</div>
            </div>
            <div class="stat-card warning">
                <div class="label">Tasa de Éxito</div>
                <div class="value">{(resumen['exitosos'] / resumen['total'] * 100) if resumen['total'] > 0 else 0:.1f}%</div>
            </div>
            <div class="stat-card info">
                <div class="label">Miembros Extraídos</div>
                <div class="value">{resumen['total_miembros'] or 0:,}</div>
            </div>
            <div class="stat-card success">
                <div class="label">Costo Total</div>
                <div class="value">${resumen['costo_total'] or 0:.4f}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔴 Errores por Tipo</h2>
            <table>
                <thead>
                    <tr>
                        <th>Tipo de Error</th>
                        <th>Cantidad</th>
                        <th>Porcentaje</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        total_errores = sum(e['cantidad'] for e in errores_agrupados)
        for error in errores_agrupados:
            porcentaje = (error['cantidad'] / total_errores * 100) if total_errores > 0 else 0
            html += f"""
                    <tr>
                        <td><span class="badge error">{error['error_tipo'] or 'DESCONOCIDO'}</span></td>
                        <td>{error['cantidad']}</td>
                        <td>{porcentaje:.1f}%</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>📋 Últimos 50 Contratos Procesados</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID Contrato</th>
                        <th>Fecha</th>
                        <th>Estado</th>
                        <th>Miembros</th>
                        <th>Método</th>
                        <th>Costo</th>
                        <th>Error</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for item in ultimos:
            estado_class = {
                'EXITO': 'success',
                'ERROR': 'error',
                'PARCIAL': 'warning',
                'SALTADO': 'info'
            }.get(item['estado'], 'info')
            
            fecha = item['fecha_proceso'].strftime('%Y-%m-%d %H:%M')
            error_msg = item['error_mensaje'][:50] + '...' if item['error_mensaje'] else '-'
            
            html += f"""
                    <tr>
                        <td><strong>{item['id_contrato']}</strong></td>
                        <td>{fecha}</td>
                        <td><span class="badge {estado_class}">{item['estado']}</span></td>
                        <td>{item['miembros_encontrados']}</td>
                        <td>{item['metodo_extraccion'] or '-'}</td>
                        <td class="cost">${item['costo_usd']:.4f}</td>
                        <td><div class="error-msg" title="{item['error_mensaje'] or ''}">{error_msg}</div></td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>📅 Resumen por Día</h2>
            <table>
                <thead>
                    <tr>
                        <th>Fecha</th>
                        <th>Procesados</th>
                        <th>Exitosos</th>
                        <th>Errores</th>
                        <th>Tasa Éxito</th>
                        <th>Miembros</th>
                        <th>Costo</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for dia in resumen_diario:
            html += f"""
                    <tr>
                        <td><strong>{dia['fecha']}</strong></td>
                        <td>{dia['total_procesados']}</td>
                        <td><span class="badge success">{dia['exitosos']}</span></td>
                        <td><span class="badge error">{dia['errores']}</span></td>
                        <td>{dia['tasa_exito']}%</td>
                        <td>{dia['total_miembros']}</td>
                        <td class="cost">${dia['costo_total']:.4f}</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
        
        # Guardar HTML
        output_file = 'reporte_etl_consorcios.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Reporte generado: {output_file}")
        print(f"\nAbre el archivo en tu navegador para ver el reporte visual")
        
        # Abrir automáticamente en el navegador
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(output_file)}')
        
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generar_reporte_html()
