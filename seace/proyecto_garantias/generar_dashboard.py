"""
Generador de Dashboard HTML con Filtros en Cascada
Versión corregida con JavaScript funcional
"""
import mysql.connector
import sys
import json
from datetime import datetime

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

# Configurar encoding UTF-8
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def obtener_estadisticas():
    """Obtiene estadísticas generales"""
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor(dictionary=True)
    
    stats = {}
    
    cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Cabecera")
    stats['total_licitaciones'] = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM Licitaciones_Adjudicaciones")
    stats['total_adjudicaciones'] = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN entidad_financiera IS NOT NULL AND entidad_financiera != '' 
                     AND entidad_financiera != 'SIN_GARANTIA' THEN 1 ELSE 0 END) as bancarias,
            SUM(CASE WHEN entidad_financiera = 'SIN_GARANTIA' THEN 1 ELSE 0 END) as retencion
        FROM Licitaciones_Adjudicaciones
        WHERE id_contrato IS NOT NULL AND id_contrato != ''
    """)
    garantias = cursor.fetchone()
    stats['garantias_bancarias'] = garantias['bancarias'] or 0
    stats['garantias_retencion'] = garantias['retencion'] or 0
    
    cursor.close()
    conn.close()
    
    return stats

def obtener_todas_licitaciones():
    """Obtiene TODAS las licitaciones"""
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor(dictionary=True)
    
    print("   Consultando base de datos...")
    cursor.execute("""
        SELECT 
            id_convocatoria,
            descripcion,
            comprador,
            categoria,
            departamento,
            provincia,
            distrito,
            estado_proceso,
            monto_estimado,
            fecha_publicacion,
            YEAR(fecha_publicacion) as anio
        FROM Licitaciones_Cabecera
        ORDER BY fecha_publicacion DESC
    """)
    
    licitaciones = cursor.fetchall()
    print(f"   Obtenidos {len(licitaciones)} registros")
    
    print("   Obteniendo adjudicaciones...")
    for i, lic in enumerate(licitaciones):
        if (i + 1) % 1000 == 0:
            print(f"   Procesando {i + 1}/{len(licitaciones)}...")
            
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN entidad_financiera IS NOT NULL 
                         AND entidad_financiera != '' 
                         AND entidad_financiera != 'SIN_GARANTIA' 
                    THEN 1 ELSE 0 END) as con_bancaria
            FROM Licitaciones_Adjudicaciones
            WHERE id_convocatoria = %s
        """, (lic['id_convocatoria'],))
        
        adj_data = cursor.fetchone()
        lic['total_adjudicaciones'] = adj_data['total'] if adj_data else 0
        lic['con_garantia_bancaria'] = adj_data['con_bancaria'] if adj_data else 0
    
    cursor.close()
    conn.close()
    
    return licitaciones

def generar_html_mejorado(stats, licitaciones):
    """Genera HTML con JavaScript funcional"""
    
    # Convertir datos a JSON para JavaScript
    datos_js = []
    for lic in licitaciones:
        # Convertir todos los valores a tipos nativos de Python
        datos_js.append({
            'id': str(lic['id_convocatoria']) if lic['id_convocatoria'] else '',
            'desc': str(lic['descripcion'] or '')[:100],
            'comp': str(lic['comprador'] or '')[:60],
            'cat': str(lic['categoria'] or ''),
            'dept': str(lic['departamento'] or ''),
            'prov': str(lic['provincia'] or ''),
            'dist': str(lic['distrito'] or ''),
            'est': str(lic['estado_proceso'] or ''),
            'monto': float(lic['monto_estimado']) if lic['monto_estimado'] is not None else 0.0,
            'fecha': lic['fecha_publicacion'].strftime('%Y-%m-%d') if lic['fecha_publicacion'] else '',
            'anio': str(lic['anio']) if lic['anio'] else '',
            'adj': int(lic['total_adjudicaciones']) if lic['total_adjudicaciones'] else 0,
            'gar': int(lic['con_garantia_bancaria']) if lic['con_garantia_bancaria'] else 0
        })
    
    datos_json = json.dumps(datos_js, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Garantías SEACE</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1800px; margin: 0 auto; }}
        .header {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 30px; text-align: center; }}
        .header h1 {{ color: #667eea; font-size: 32px; margin-bottom: 10px; }}
        .header p {{ color: #666; font-size: 14px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); text-align: center; transition: transform 0.3s; }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-card .icon {{ font-size: 40px; margin-bottom: 10px; }}
        .stat-card .value {{ font-size: 36px; font-weight: bold; color: #667eea; margin-bottom: 5px; }}
        .stat-card .label {{ color: #666; font-size: 14px; }}
        .filters {{ background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-bottom: 30px; }}
        .filters h3 {{ color: #333; margin-bottom: 20px; font-size: 20px; }}
        .filter-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .filter-group {{ display: flex; flex-direction: column; }}
        .filter-group label {{ color: #666; font-size: 13px; margin-bottom: 5px; font-weight: 500; }}
        .filter-group select, .filter-group input {{ padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 14px; }}
        .filter-group select:focus, .filter-group input:focus {{ outline: none; border-color: #667eea; }}
        .btn {{ padding: 10px 20px; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; }}
        .btn-primary {{ background: #667eea; color: white; }}
        .btn-primary:hover {{ background: #5568d3; }}
        .btn-secondary {{ background: #e0e0e0; color: #333; }}
        .table-container {{ background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); overflow-x: auto; }}
        .table-container h2 {{ color: #333; margin-bottom: 20px; font-size: 24px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        thead {{ background: #f8f9fa; }}
        th {{ padding: 15px; text-align: left; font-weight: 600; color: #333; font-size: 13px; text-transform: uppercase; border-bottom: 2px solid #667eea; }}
        td {{ padding: 15px; border-bottom: 1px solid #f0f0f0; font-size: 14px; color: #555; }}
        tr:hover {{ background: #f8f9fa; }}
        .badge {{ display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
        .badge-success {{ background: #d4edda; color: #155724; }}
        .badge-warning {{ background: #fff3cd; color: #856404; }}
        .badge-info {{ background: #d1ecf1; color: #0c5460; }}
        .badge-danger {{ background: #f8d7da; color: #721c24; }}
        .pagination {{ display: flex; justify-content: center; align-items: center; gap: 10px; margin-top: 20px; }}
        .pagination button {{ padding: 8px 15px; border: 2px solid #667eea; background: white; color: #667eea; border-radius: 8px; cursor: pointer; font-weight: 600; }}
        .pagination button:hover:not(:disabled) {{ background: #667eea; color: white; }}
        .pagination button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Dashboard de Garantías SEACE</h1>
            <p>Sistema de Análisis de Licitaciones Públicas del Perú</p>
            <p style="margin-top: 10px; color: #999; font-size: 12px;">Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="icon">📋</div>
                <div class="value">{stats['total_licitaciones']:,}</div>
                <div class="label">Total Licitaciones</div>
            </div>
            <div class="stat-card">
                <div class="icon">✅</div>
                <div class="value">{stats['total_adjudicaciones']:,}</div>
                <div class="label">Total Adjudicaciones</div>
            </div>
            <div class="stat-card">
                <div class="icon">🏦</div>
                <div class="value">{stats['garantias_bancarias']:,}</div>
                <div class="label">Garantías Bancarias</div>
            </div>
            <div class="stat-card">
                <div class="icon">💰</div>
                <div class="value">{stats['garantias_retencion']:,}</div>
                <div class="label">Retención (10%)</div>
            </div>
        </div>

        <div class="filters">
            <h3>🔍 Filtros de Búsqueda</h3>
            <div class="filter-grid">
                <div class="filter-group">
                    <label>Buscar (ID o Descripción)</label>
                    <input type="text" id="searchText" placeholder="Escribe para buscar...">
                </div>
                <div class="filter-group">
                    <label>Categoría</label>
                    <select id="filterCategoria">
                        <option value="">Todas</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Departamento</label>
                    <select id="filterDepartamento" onchange="actualizarProvincias()">
                        <option value="">Todos</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Provincia</label>
                    <select id="filterProvincia" onchange="actualizarDistritos()">
                        <option value="">Todas</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Distrito</label>
                    <select id="filterDistrito">
                        <option value="">Todos</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Año</label>
                    <select id="filterAnio">
                        <option value="">Todos</option>
                    </select>
                </div>
            </div>
            <div style="display: flex; gap: 10px;">
                <button class="btn btn-primary" onclick="aplicarFiltros()">Buscar</button>
                <button class="btn btn-secondary" onclick="limpiarFiltros()">Limpiar</button>
            </div>
            <div style="margin-top: 15px; color: #666; font-size: 14px;">
                <strong>Resultados:</strong> <span id="resultCount">0</span> licitaciones encontradas
            </div>
        </div>

        <div class="table-container">
            <h2>📋 Licitaciones</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Descripción</th>
                        <th>Comprador</th>
                        <th>Categoría</th>
                        <th>Departamento</th>
                        <th>Provincia</th>
                        <th>Estado</th>
                        <th>Monto</th>
                        <th>Fecha</th>
                        <th>Adj.</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                </tbody>
            </table>
            <div class="pagination">
                <button onclick="cambiarPagina(-1)" id="btnPrev">← Anterior</button>
                <span id="pageInfo">Página 1</span>
                <button onclick="cambiarPagina(1)" id="btnNext">Siguiente →</button>
            </div>
        </div>
    </div>

    <script>
        // Datos completos
        const allData = {datos_json};
        let filteredData = [...allData];
        let currentPage = 1;
        const itemsPerPage = 50;

        // Inicializar filtros
        function inicializarFiltros() {{
            // Categorías únicas
            const categorias = [...new Set(allData.map(item => item.cat).filter(Boolean))];
            const selectCat = document.getElementById('filterCategoria');
            categorias.forEach(cat => {{
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                selectCat.appendChild(option);
            }});

            // Departamentos únicos
            const departamentos = [...new Set(allData.map(item => item.dept).filter(Boolean))].sort();
            const selectDept = document.getElementById('filterDepartamento');
            departamentos.forEach(dept => {{
                const option = document.createElement('option');
                option.value = dept;
                option.textContent = dept;
                selectDept.appendChild(option);
            }});

            // Años únicos
            const anios = [...new Set(allData.map(item => item.anio).filter(Boolean))].sort().reverse();
            const selectAnio = document.getElementById('filterAnio');
            anios.forEach(anio => {{
                const option = document.createElement('option');
                option.value = anio;
                option.textContent = anio;
                selectAnio.appendChild(option);
            }});
        }}

        // Actualizar provincias según departamento seleccionado
        function actualizarProvincias() {{
            const deptSeleccionado = document.getElementById('filterDepartamento').value;
            const selectProv = document.getElementById('filterProvincia');
            const selectDist = document.getElementById('filterDistrito');
            
            // Limpiar provincias y distritos
            selectProv.innerHTML = '<option value="">Todas</option>';
            selectDist.innerHTML = '<option value="">Todos</option>';
            
            if (deptSeleccionado) {{
                // Filtrar provincias del departamento seleccionado
                const provincias = [...new Set(
                    allData
                        .filter(item => item.dept === deptSeleccionado)
                        .map(item => item.prov)
                        .filter(Boolean)
                )].sort();
                
                provincias.forEach(prov => {{
                    const option = document.createElement('option');
                    option.value = prov;
                    option.textContent = prov;
                    selectProv.appendChild(option);
                }});
            }}
        }}

        // Actualizar distritos según provincia seleccionada
        function actualizarDistritos() {{
            const deptSeleccionado = document.getElementById('filterDepartamento').value;
            const provSeleccionada = document.getElementById('filterProvincia').value;
            const selectDist = document.getElementById('filterDistrito');
            
            // Limpiar distritos
            selectDist.innerHTML = '<option value="">Todos</option>';
            
            if (provSeleccionada) {{
                // Filtrar distritos de la provincia seleccionada
                const distritos = [...new Set(
                    allData
                        .filter(item => item.dept === deptSeleccionado && item.prov === provSeleccionada)
                        .map(item => item.dist)
                        .filter(Boolean)
                )].sort();
                
                distritos.forEach(dist => {{
                    const option = document.createElement('option');
                    option.value = dist;
                    option.textContent = dist;
                    selectDist.appendChild(option);
                }});
            }}
        }}

        // Aplicar filtros
        function aplicarFiltros() {{
            const search = document.getElementById('searchText').value.toLowerCase();
            const categoria = document.getElementById('filterCategoria').value;
            const departamento = document.getElementById('filterDepartamento').value;
            const provincia = document.getElementById('filterProvincia').value;
            const distrito = document.getElementById('filterDistrito').value;
            const anio = document.getElementById('filterAnio').value;

            filteredData = allData.filter(item => {{
                const matchSearch = !search || 
                    item.id.toLowerCase().includes(search) || 
                    item.desc.toLowerCase().includes(search);
                const matchCategoria = !categoria || item.cat === categoria;
                const matchDepartamento = !departamento || item.dept === departamento;
                const matchProvincia = !provincia || item.prov === provincia;
                const matchDistrito = !distrito || item.dist === distrito;
                const matchAnio = !anio || item.anio === anio;

                return matchSearch && matchCategoria && matchDepartamento && 
                       matchProvincia && matchDistrito && matchAnio;
            }});

            currentPage = 1;
            mostrarResultados();
        }}

        // Limpiar filtros
        function limpiarFiltros() {{
            document.getElementById('searchText').value = '';
            document.getElementById('filterCategoria').value = '';
            document.getElementById('filterDepartamento').value = '';
            document.getElementById('filterProvincia').value = '';
            document.getElementById('filterDistrito').value = '';
            document.getElementById('filterAnio').value = '';
            
            // Restaurar opciones de provincia y distrito
            document.getElementById('filterProvincia').innerHTML = '<option value="">Todas</option>';
            document.getElementById('filterDistrito').innerHTML = '<option value="">Todos</option>';
            
            filteredData = [...allData];
            currentPage = 1;
            mostrarResultados();
        }}

        // Mostrar resultados
        function mostrarResultados() {{
            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            const pageData = filteredData.slice(start, end);

            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            pageData.forEach(item => {{
                const badgeClass = {{
                    'CONTRATADO': 'badge-success',
                    'ADJUDICADO': 'badge-info',
                    'CONSENTIDO': 'badge-warning',
                    'CANCELADO': 'badge-danger'
                }}[item.est] || 'badge-info';

                const row = `
                    <tr>
                        <td><strong>${{item.id}}</strong></td>
                        <td>${{item.desc}}</td>
                        <td>${{item.comp}}</td>
                        <td>${{item.cat || 'N/A'}}</td>
                        <td>${{item.dept || 'N/A'}}</td>
                        <td>${{item.prov || 'N/A'}}</td>
                        <td><span class="badge ${{badgeClass}}">${{item.est || 'N/A'}}</span></td>
                        <td>S/ ${{item.monto.toLocaleString()}}</td>
                        <td>${{item.fecha}}</td>
                        <td>${{item.adj}}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            }});

            document.getElementById('resultCount').textContent = filteredData.length.toLocaleString();
            const totalPages = Math.ceil(filteredData.length / itemsPerPage);
            document.getElementById('pageInfo').textContent = `Página ${{currentPage}} de ${{totalPages || 1}}`;
            document.getElementById('btnPrev').disabled = currentPage === 1;
            document.getElementById('btnNext').disabled = currentPage === totalPages || totalPages === 0;
        }}

        // Cambiar página
        function cambiarPagina(direction) {{
            const totalPages = Math.ceil(filteredData.length / itemsPerPage);
            const newPage = currentPage + direction;
            if (newPage >= 1 && newPage <= totalPages) {{
                currentPage = newPage;
                mostrarResultados();
            }}
        }}

        // Inicializar al cargar
        window.addEventListener('DOMContentLoaded', () => {{
            inicializarFiltros();
            filteredData = [...allData];
            mostrarResultados();
        }});
    </script>
</body>
</html>
"""
    
    return html

def main():
    print("="*80)
    print("GENERADOR DE DASHBOARD HTML CON FILTROS EN CASCADA")
    print("="*80)
    
    print("\n1. Obteniendo estadísticas...")
    stats = obtener_estadisticas()
    print(f"   - Licitaciones: {stats['total_licitaciones']:,}")
    print(f"   - Adjudicaciones: {stats['total_adjudicaciones']:,}")
    
    print("\n2. Obteniendo TODAS las licitaciones...")
    licitaciones = obtener_todas_licitaciones()
    
    print("\n3. Generando HTML con filtros en cascada...")
    html = generar_html_mejorado(stats, licitaciones)
    
    print("\n4. Guardando archivo...")
    with open('dashboard_visual.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("\n" + "="*80)
    print("✅ DASHBOARD CON FILTROS EN CASCADA GENERADO")
    print("="*80)
    print(f"\nArchivo creado: dashboard_visual.html")
    print(f"Total de registros: {len(licitaciones):,}")
    print("\nCaracterísticas:")
    print("  ✅ Filtros en cascada (Depto → Prov → Dist)")
    print("  ✅ Búsqueda por texto")
    print("  ✅ Filtro por categoría y año")
    print("  ✅ Paginación (50 registros por página)")
    print("  ✅ Contador de resultados")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
