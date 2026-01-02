from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case, text
from typing import Optional, List, Any
from pydantic import BaseModel
from app.database import get_db
from app.models.seace import LicitacionesCabecera, LicitacionesAdjudicaciones
from datetime import datetime

router = APIRouter(prefix="/api/reportes", tags=["Reportes"])

class ReporteFiltros(BaseModel):
    search: Optional[str] = None
    departamento: Optional[str] = None
    provincia: Optional[str] = None
    distrito: Optional[str] = None
    estado_proceso: Optional[str] = None
    categoria: Optional[str] = None
    comprador: Optional[str] = None
    aseguradora: Optional[str] = None
    year: Optional[str] = None
    mes: Optional[str] = None

class GenerarReporteRequest(BaseModel):
    tipo: str  # 'entidad', 'departamento', 'categoria', 'estado', 'personalizado'
    filtros: ReporteFiltros

@router.post("/generar")
def generar_reporte(request: GenerarReporteRequest, db: Session = Depends(get_db)):
    """
    Genera reportes agrupados según el tipo seleccionado y filtros aplicados.
    """
    tipo = request.tipo
    filtros = request.filtros
    
    # Base query components
    query = db.query()
    
    # Define columns based on report type
    if tipo == 'entidad':
        # Logic to group by entidad_financiera cleaned
        # In SQLAlchemy we might need raw SQL expression for the CASE statement if it's complex
        # or use python-side processing if valid.
        pass # Will implement below
        
    # Since SQLAlchemy + massive string manipulation is tricky, we'll build a base query object
    # But for complex grouping like the 'entidad' logic (cleaning names), raw SQL or specific expressions are better.
    
    # Common joins
    # Most reports need headers + adjudications
    
    params = {}
    where_clauses = ["a.entidad_financiera IS NOT NULL", "a.entidad_financiera != ''", "a.entidad_financiera != 'SIN_GARANTIA'"] if tipo == 'entidad' else ["1=1"]
    
    # Apply filters to WHERE
    if filtros.departamento:
        where_clauses.append("UPPER(c.departamento) = UPPER(:departamento)")
        params['departamento'] = filtros.departamento
    if filtros.provincia:
        where_clauses.append("UPPER(c.provincia) = UPPER(:provincia)")
        params['provincia'] = filtros.provincia
    if filtros.distrito:
        where_clauses.append("UPPER(c.distrito) = UPPER(:distrito)")
        params['distrito'] = filtros.distrito
    if filtros.estado_proceso:
        where_clauses.append("UPPER(c.estado_proceso) = UPPER(:estado_proceso)")
        params['estado_proceso'] = filtros.estado_proceso
    if filtros.categoria:
        where_clauses.append("UPPER(c.categoria) = UPPER(:categoria)")
        params['categoria'] = filtros.categoria
    if filtros.comprador:
        where_clauses.append("UPPER(c.comprador) LIKE UPPER(:comprador)")
        params['comprador'] = f"%{filtros.comprador}%"
    if filtros.year:
        where_clauses.append("YEAR(c.fecha_publicacion) = :year")
        params['year'] = filtros.year
    if filtros.mes:
        where_clauses.append("MONTH(c.fecha_publicacion) = :mes")
        params['mes'] = filtros.mes
        
    # Additional specific filters
    if filtros.aseguradora and tipo != 'entidad': # If filtering by insurer
        where_clauses.append("UPPER(a.entidad_financiera) LIKE UPPER(:aseguradora)")
        params['aseguradora'] = f"%{filtros.aseguradora}%"

    where_str = " AND ".join(where_clauses)
    
    sql = ""
    
    if tipo == 'entidad':
        sql = f"""
            SELECT 
                CASE 
                    WHEN a.entidad_financiera IN ('ERROR_API_500', 'FINANCIERO') THEN 'OTROS'
                    WHEN a.entidad_financiera LIKE '%|%' 
                    THEN TRIM(SUBSTRING_INDEX(a.entidad_financiera, '|', 1))
                    ELSE a.entidad_financiera
                END as nombre,
                COUNT(*) as garantias,
                SUM(COALESCE(a.monto_adjudicado, 0)) as monto,
                COUNT(DISTINCT c.departamento) as departamentos
            FROM licitaciones_adjudicaciones a
            LEFT JOIN licitaciones_cabecera c ON a.id_convocatoria = c.id_convocatoria
            WHERE {where_str}
            GROUP BY 
                CASE 
                    WHEN a.entidad_financiera IN ('ERROR_API_500', 'FINANCIERO') THEN 'OTROS'
                    WHEN a.entidad_financiera LIKE '%|%' 
                    THEN TRIM(SUBSTRING_INDEX(a.entidad_financiera, '|', 1))
                    ELSE a.entidad_financiera
                END
            ORDER BY garantias DESC
            LIMIT 100
        """
    
    elif tipo == 'departamento':
        where_str += " AND c.departamento IS NOT NULL "
        sql = f"""
            SELECT 
                c.departamento as nombre,
                COUNT(DISTINCT c.id_convocatoria) as garantias,
                SUM(COALESCE(a.monto_adjudicado, 0)) as monto,
                COUNT(DISTINCT c.categoria) as categorias
            FROM licitaciones_cabecera c
            LEFT JOIN licitaciones_adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
            WHERE {where_str}
            GROUP BY c.departamento
            ORDER BY garantias DESC
        """
        
    elif tipo == 'categoria':
        where_str += " AND c.categoria IS NOT NULL "
        sql = f"""
            SELECT 
                c.categoria as nombre,
                COUNT(DISTINCT c.id_convocatoria) as garantias,
                SUM(COALESCE(a.monto_adjudicado, 0)) as monto,
                COUNT(DISTINCT c.departamento) as departamentos
            FROM licitaciones_cabecera c
            LEFT JOIN licitaciones_adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
            WHERE {where_str}
            GROUP BY c.categoria
            ORDER BY garantias DESC
        """
        
    elif tipo == 'estado':
        where_str += " AND c.estado_proceso IS NOT NULL "
        sql = f"""
            SELECT 
                c.estado_proceso as nombre,
                COUNT(DISTINCT c.id_convocatoria) as garantias,
                SUM(COALESCE(a.monto_adjudicado, 0)) as monto,
                COUNT(DISTINCT c.departamento) as departamentos
            FROM licitaciones_cabecera c
            LEFT JOIN licitaciones_adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
            WHERE {where_str}
            GROUP BY c.estado_proceso
            ORDER BY garantias DESC
        """
    
    else: # personalizado or default
        sql = f"""
            SELECT 
                c.descripcion as nombre,
                COUNT(DISTINCT a.id_adjudicacion) as garantias,
                SUM(COALESCE(a.monto_adjudicado, 0)) as monto,
                c.departamento
            FROM licitaciones_cabecera c
            LEFT JOIN licitaciones_adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
            WHERE {where_str}
            GROUP BY c.id_convocatoria
            LIMIT 100
        """

    try:
        result = db.execute(text(sql), params)
        rows = [dict(row._mapping) for row in result]
        
        # Format output
        formatted_rows = []
        for row in rows:
            # Clean up decimals for JSON serialization
            monto_val = row.get('monto', 0)
            formatted_rows.append({
                "nombre": row.get('nombre', 'Sin Nombre'),
                "garantias": row.get('garantias', 0),
                "monto": f"S/ {float(monto_val):,.2f}" if monto_val else "S/ 0.00",
                "departamentos": row.get('departamentos', 0) if 'departamentos' in row else row.get('departamento', '')
            })
            
        return {
            "success": True,
            "data": formatted_rows,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_records": len(formatted_rows)
            }
        }
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/resumen-ejecutivo")
def get_resumen_ejecutivo(db: Session = Depends(get_db)):
    """
    Endpoint for EcommerceMetrics card.
    Returns total tenders and total adjudicated amount.
    """
    try:
        sql = text("""
            SELECT 
                COUNT(*) as total_licitaciones,
                COALESCE(SUM(monto_estimado), 0) as monto_total
            FROM licitaciones_cabecera
        """)
        result = db.execute(sql).fetchone()
        
        return {
            "success": True,
            "data": {
                "total_licitaciones": result[0] or 0,
                "monto_total": float(result[1]) if result[1] else 0
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/por-departamento")
def get_reporte_por_departamento(db: Session = Depends(get_db)):
    """
    Endpoint for DemographicCard.
    Returns list of departments with count and amount.
    """
    try:
        sql = text("""
            SELECT 
                departamento,
                COUNT(*) as total,
                COALESCE(SUM(monto_estimado), 0) as monto_total
            FROM licitaciones_cabecera
            WHERE departamento IS NOT NULL AND departamento != ''
            GROUP BY departamento
            ORDER BY total DESC
        """)
        result = db.execute(sql).fetchall()
        
        departamentos = []
        for row in result:
            departamentos.append({
                "departamento": row[0],
                "total": row[1],
                "monto_total": float(row[2]) if row[2] else 0
            })
            
        return {
            "success": True,
            "data": {
                "departamentos": departamentos
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/por-provincia/{departamento}")
def get_reporte_por_provincia(departamento: str, db: Session = Depends(get_db)):
    """
    Endpoint for DemographicCard drill-down.
    Returns list of provinces for a specific department.
    """
    try:
        sql = text("""
            SELECT 
                provincia,
                COUNT(*) as total,
                COALESCE(SUM(monto_estimado), 0) as monto_total
            FROM licitaciones_cabecera
            WHERE departamento = :dept 
              AND provincia IS NOT NULL 
              AND provincia != ''
            GROUP BY provincia
            ORDER BY total DESC
        """)
        result = db.execute(sql, {"dept": departamento}).fetchall()
        
        provincias = []
        for row in result:
            provincias.append({
                "provincia": row[0],
                "total": row[1],
                "monto_total": float(row[2]) if row[2] else 0
            })
            
        return {
            "success": True,
            "data": {
                "provincias": provincias
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/por-tiempo")
def get_reporte_por_tiempo(db: Session = Depends(get_db)):
    """
    Endpoint for StatisticsChart.
    Returns tenders grouped by year and month.
    """
    try:
        sql = text("""
            SELECT 
                YEAR(fecha_publicacion) as anio,
                MONTH(fecha_publicacion) as mes_num,
                DATE_FORMAT(fecha_publicacion, '%b') as mes_nombre,
                COUNT(*) as total
            FROM licitaciones_cabecera
            WHERE fecha_publicacion IS NOT NULL
            GROUP BY YEAR(fecha_publicacion), MONTH(fecha_publicacion)
            ORDER BY anio DESC, mes_num ASC
        """)
        result = db.execute(sql).fetchall()
        
        # Process data into expected format: { "2024": { months: [], licitaciones: [] } }
        data = {}
        
        # Initialize structure for years found
        for row in result:
            anio = str(row[0])
            if anio not in data:
                data[anio] = {"months": [], "licitaciones": []}
        
        # Fill data
        for row in result:
            anio = str(row[0])
            mes = row[2] # Short month name
            total = row[3]
            
            data[anio]["months"].append(mes)
            data[anio]["licitaciones"].append(total)
            
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/por-entidad-financiera")
def get_reporte_por_entidad_financiera(db: Session = Depends(get_db)):
    """
    Endpoint for TopEntidadesFinancieras.
    """
    try:
        # Check if we have data in adjudicaciones
        check_sql = text("SELECT COUNT(*) FROM licitaciones_adjudicaciones")
        count = db.execute(check_sql).scalar()
        
        if count > 0:
            sql = text("""
                SELECT 
                    entidad_financiera,
                    COUNT(*) as total,
                    COALESCE(SUM(monto_adjudicado), 0) as monto_total,
                    COUNT(DISTINCT c.departamento) as departamentos_atendidos
                FROM licitaciones_adjudicaciones a
                LEFT JOIN licitaciones_cabecera c ON a.id_convocatoria = c.id_convocatoria
                WHERE a.entidad_financiera IS NOT NULL 
                  AND a.entidad_financiera != ''
                  AND a.entidad_financiera != 'SIN_GARANTIA'
                  AND a.entidad_financiera NOT LIKE '%ERROR%'
                GROUP BY entidad_financiera
                ORDER BY total DESC
                LIMIT 20
            """)
            result = db.execute(sql).fetchall()
            entidades = []
            for row in result:
                entidades.append({
                    "entidad_financiera": row[0],
                    "total": row[1],
                    "monto_total": str(row[2]),
                    "departamentos_atendidos": row[3],
                    "categorias_atendidas": 0 # Simplified
                })
        else:
            # Fallback returning empty list
            entidades = []

        return {
            "success": True,
            "data": {
                "entidades": entidades
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/por-estado")
def get_reporte_por_estado(db: Session = Depends(get_db)):
    """
    Endpoint for MonthlySalesChart (Licitaciones por Estado).
    """
    try:
        sql = text("""
            SELECT 
                estado_proceso,
                COUNT(*) as total
            FROM licitaciones_cabecera
            WHERE estado_proceso IS NOT NULL AND estado_proceso != ''
            GROUP BY estado_proceso
            ORDER BY total DESC
        """)
        result = db.execute(sql).fetchall()
        
        estados = []
        for row in result:
            estados.append({
                "estado": row[0].replace('_', ' '),
                "total": row[1],
                "retencion": "0" # Placeholder
            })
            
        return {
            "success": True,
            "data": {
                "estados_proceso": estados
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
