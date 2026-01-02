"""
API Backend para Dashboard de Garantias SEACE
Proporciona endpoints REST para consultar datos
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import sys
from datetime import datetime

# Configurar encoding UTF-8 para Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

app = Flask(__name__)
CORS(app)  # Permitir CORS para desarrollo

def get_connection():
    """Obtiene conexion a la base de datos"""
    return mysql.connector.connect(**get_db_config())

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas generales"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Total de licitaciones
    cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Cabecera")
    total_licitaciones = cursor.fetchone()['total']
    
    # Total monto (suma de montos estimados)
    cursor.execute("""
        SELECT SUM(monto_estimado) as total_monto
        FROM Licitaciones_Cabecera
        WHERE monto_estimado IS NOT NULL
    """)
    total_monto = cursor.fetchone()['total_monto'] or 0
    
    # Garantías bancarias vs retención
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' 
                     AND entidad_financiera != 'SIN_GARANTIA' THEN 1 ELSE 0 END) as bancarias,
            SUM(CASE WHEN entidad_financiera = 'SIN_GARANTIA' THEN 1 ELSE 0 END) as retencion
        FROM Licitaciones_Adjudicaciones
        WHERE id_contrato IS NOT NULL AND id_contrato != ''
    """)
    garantias = cursor.fetchone()
    
    # Top 5 departamentos
    cursor.execute("""
        SELECT departamento, COUNT(*) as total
        FROM Licitaciones_Cabecera
        WHERE departamento IS NOT NULL
        GROUP BY departamento
        ORDER BY total DESC
        LIMIT 5
    """)
    top_departamentos = cursor.fetchall()
    
    # Top 5 entidades financieras
    cursor.execute("""
        SELECT entidad_financiera, COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        WHERE entidad_financiera IS NOT NULL 
          AND entidad_financiera != ''
          AND entidad_financiera != 'SIN_GARANTIA'
          AND entidad_financiera NOT LIKE 'ERROR%'
        GROUP BY entidad_financiera
        ORDER BY total DESC
        LIMIT 5
    """)
    top_bancos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'total_licitaciones': total_licitaciones,
        'total_monto': float(total_monto),
        'garantias_bancarias': garantias['bancarias'] or 0,
        'garantias_retencion': garantias['retencion'] or 0,
        'top_departamentos': top_departamentos,
        'top_bancos': top_bancos
    })

@app.route('/api/licitaciones', methods=['GET'])
def get_licitaciones():
    """Obtiene lista de licitaciones con filtros"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Parámetros de filtro
    search = request.args.get('search', '')
    departamento = request.args.get('departamento', '')
    provincia = request.args.get('provincia', '')
    distrito = request.args.get('distrito', '')
    estado = request.args.get('estado', '')
    estado_item = request.args.get('estado_item', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    # Construir query
    where_clauses = []
    params = []
    
    if search:
        where_clauses.append("""
            (c.id_convocatoria LIKE %s 
             OR c.descripcion LIKE %s 
             OR c.comprador LIKE %s)
        """)
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])
    
    if departamento:
        where_clauses.append("c.departamento = %s")
        params.append(departamento)
    
    if provincia:
        where_clauses.append("c.provincia = %s")
        params.append(provincia)
    
    if distrito:
        where_clauses.append("c.distrito = %s")
        params.append(distrito)
    
    if estado:
        where_clauses.append("c.estado_proceso = %s")
        params.append(estado)
    
    if estado_item:
        where_clauses.append("a.estado_item = %s")
        params.append(estado_item)
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Contar total
    count_sql = f"""
        SELECT COUNT(DISTINCT c.id_convocatoria) as total
        FROM Licitaciones_Cabecera c
        LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
        WHERE {where_sql}
    """
    cursor.execute(count_sql, params)
    total = cursor.fetchone()['total']
    
    # Obtener datos paginados
    offset = (page - 1) * per_page
    data_sql = f"""
        SELECT 
            c.id_convocatoria,
            c.descripcion,
            c.comprador,
            c.departamento,
            c.provincia,
            c.monto_estimado,
            c.fecha_publicacion,
            c.estado_proceso,
            COALESCE(SUM(a.monto_adjudicado), 0) as monto_total_adjudicado,
            SUM(CASE WHEN a.entidad_financiera IS NOT NULL 
                     AND a.entidad_financiera != '' 
                     AND a.entidad_financiera != 'SIN_GARANTIA' 
                THEN 1 ELSE 0 END) as con_garantia_bancaria,
            GROUP_CONCAT(DISTINCT a.entidad_financiera SEPARATOR ', ') as entidades_financieras
        FROM Licitaciones_Cabecera c
        LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
        WHERE {where_sql}
        GROUP BY c.id_convocatoria
        ORDER BY c.fecha_publicacion DESC
        LIMIT %s OFFSET %s
    """
    cursor.execute(data_sql, params + [per_page, offset])
    licitaciones = cursor.fetchall()
    
    # Formatear fechas y montos
    for lic in licitaciones:
        if lic['fecha_publicacion']:
            lic['fecha_publicacion'] = lic['fecha_publicacion'].strftime('%Y-%m-%d')
        if lic['monto_estimado']:
            lic['monto_estimado'] = float(lic['monto_estimado'])
        if lic['monto_total_adjudicado']:
            lic['monto_total_adjudicado'] = float(lic['monto_total_adjudicado'])
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page,
        'data': licitaciones
    })

@app.route('/api/licitacion/<id_convocatoria>', methods=['GET'])
def get_licitacion_detalle(id_convocatoria):
    """Obtiene detalle de una licitación específica"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Datos de la licitación
    cursor.execute("""
        SELECT * FROM Licitaciones_Cabecera
        WHERE id_convocatoria = %s
    """, (id_convocatoria,))
    licitacion = cursor.fetchone()
    
    if not licitacion:
        return jsonify({'error': 'Licitación no encontrada'}), 404
    
    # Adjudicaciones
    cursor.execute("""
        SELECT * FROM Licitaciones_Adjudicaciones
        WHERE id_convocatoria = %s
    """, (id_convocatoria,))
    adjudicaciones = cursor.fetchall()
    
    # Formatear fechas
    if licitacion['fecha_publicacion']:
        licitacion['fecha_publicacion'] = licitacion['fecha_publicacion'].strftime('%Y-%m-%d')
    if licitacion['monto_estimado']:
        licitacion['monto_estimado'] = float(licitacion['monto_estimado'])
    
    for adj in adjudicaciones:
        if adj['fecha_adjudicacion']:
            adj['fecha_adjudicacion'] = adj['fecha_adjudicacion'].strftime('%Y-%m-%d')
        if adj['monto_adjudicado']:
            adj['monto_adjudicado'] = float(adj['monto_adjudicado'])
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'licitacion': licitacion,
        'adjudicaciones': adjudicaciones
    })

@app.route('/api/filtros', methods=['GET'])
def get_filtros():
    """Obtiene opciones para filtros"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Departamentos
    cursor.execute("""
        SELECT DISTINCT departamento
        FROM Licitaciones_Cabecera
        WHERE departamento IS NOT NULL
        ORDER BY departamento
    """)
    departamentos = [row['departamento'] for row in cursor.fetchall()]
    
    # Estados
    cursor.execute("""
        SELECT DISTINCT estado_proceso
        FROM Licitaciones_Cabecera
        WHERE estado_proceso IS NOT NULL
        ORDER BY estado_proceso
    """)
    estados = [row['estado_proceso'] for row in cursor.fetchall()]
    
    # Estados de items
    cursor.execute("""
        SELECT DISTINCT estado_item
        FROM Licitaciones_Adjudicaciones
        WHERE estado_item IS NOT NULL
        ORDER BY estado_item
    """)
    estados_item = [row['estado_item'] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'departamentos': departamentos,
        'estados': estados,
        'estados_item': estados_item
    })

@app.route('/api/filtros/provincias', methods=['GET'])
def get_provincias():
    """Obtiene provincias filtradas por departamento"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    departamento = request.args.get('departamento', '')
    
    if departamento:
        cursor.execute("""
            SELECT DISTINCT provincia
            FROM Licitaciones_Cabecera
            WHERE departamento = %s AND provincia IS NOT NULL
            ORDER BY provincia
        """, (departamento,))
    else:
        cursor.execute("""
            SELECT DISTINCT provincia
            FROM Licitaciones_Cabecera
            WHERE provincia IS NOT NULL
            ORDER BY provincia
        """)
    
    provincias = [row['provincia'] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return jsonify({'provincias': provincias})

@app.route('/api/filtros/distritos', methods=['GET'])
def get_distritos():
    """Obtiene distritos filtrados por departamento y provincia"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    departamento = request.args.get('departamento', '')
    provincia = request.args.get('provincia', '')
    
    where_clauses = []
    params = []
    
    if departamento:
        where_clauses.append("departamento = %s")
        params.append(departamento)
    
    if provincia:
        where_clauses.append("provincia = %s")
        params.append(provincia)
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    cursor.execute(f"""
        SELECT DISTINCT distrito
        FROM Licitaciones_Cabecera
        WHERE {where_sql} AND distrito IS NOT NULL
        ORDER BY distrito
    """, params)
    
    distritos = [row['distrito'] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return jsonify({'distritos': distritos})

@app.route('/api/charts/garantias', methods=['GET'])
def get_chart_garantias():
    """Obtiene datos para gráfico de garantías"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN entidad_financiera IS NOT NULL 
                     AND entidad_financiera != '' 
                     AND entidad_financiera != 'SIN_GARANTIA' 
                THEN 1 ELSE 0 END) as bancarias,
            SUM(CASE WHEN entidad_financiera = 'SIN_GARANTIA' 
                     OR entidad_financiera IS NULL 
                     OR entidad_financiera = '' 
                THEN 1 ELSE 0 END) as retencion
        FROM Licitaciones_Adjudicaciones
        WHERE id_contrato IS NOT NULL AND id_contrato != ''
    """)
    data = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'labels': ['Garantía Bancaria', 'Retención'],
        'values': [data['bancarias'] or 0, data['retencion'] or 0]
    })

@app.route('/api/charts/departamentos', methods=['GET'])
def get_chart_departamentos():
    """Obtiene top 10 departamentos"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT departamento, COUNT(*) as total
        FROM Licitaciones_Cabecera
        WHERE departamento IS NOT NULL
        GROUP BY departamento
        ORDER BY total DESC
        LIMIT 10
    """)
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'labels': [row['departamento'] for row in data],
        'values': [row['total'] for row in data]
    })

@app.route('/api/charts/timeline', methods=['GET'])
def get_chart_timeline():
    """Obtiene licitaciones por mes"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            DATE_FORMAT(fecha_publicacion, '%Y-%m') as mes,
            COUNT(*) as total
        FROM Licitaciones_Cabecera
        WHERE fecha_publicacion IS NOT NULL
        GROUP BY mes
        ORDER BY mes DESC
        LIMIT 12
    """)
    data = cursor.fetchall()
    data.reverse()  # Ordenar cronológicamente
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'labels': [row['mes'] for row in data],
        'values': [row['total'] for row in data]
    })

@app.route('/api/charts/bancos', methods=['GET'])
def get_chart_bancos():
    """Obtiene top 10 entidades financieras"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT entidad_financiera, COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        WHERE entidad_financiera IS NOT NULL 
          AND entidad_financiera != ''
          AND entidad_financiera != 'SIN_GARANTIA'
          AND entidad_financiera NOT LIKE 'ERROR%'
        GROUP BY entidad_financiera
        ORDER BY total DESC
        LIMIT 10
    """)
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'labels': [row['entidad_financiera'] for row in data],
        'values': [row['total'] for row in data]
    })

if __name__ == '__main__':
    print("Iniciando API del Dashboard...")
    print("API disponible en: http://localhost:5000")
    print("Endpoints:")
    print("   - GET /api/stats")
    print("   - GET /api/licitaciones")
    print("   - GET /api/licitacion/<id>")
    print("   - GET /api/filtros")
    app.run(debug=True, port=5000, host='127.0.0.1')
