"""
Dashboard endpoints using RAW SQL - adapted to real database structure.
Uses licitaciones_cabecera (which has data) instead of empty licitaciones_adjudicaciones.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import Optional
from decimal import Decimal

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/kpis")
def get_dashboard_kpis(
    estado: Optional[str] = Query(None, description="Filter by estado_proceso"),
    tipo_procedimiento: Optional[str] = Query(None, description="Filter by tipo_procedimiento"),
    categoria: Optional[str] = Query(None, description="Filter by categoria"),
    departamento: Optional[str] = Query(None, description="Filter by departamento"),
    db: Session = Depends(get_db)
):
    """
    Get dashboard KPIs using data from licitaciones_cabecera.
    Since licitaciones_adjudicaciones is empty, we use monto_estimado from cabecera.
    """
    
    try:
        # Build WHERE clause for filters
        where_clauses = []
        params = {}
        
        if estado:
            where_clauses.append("estado_proceso = :estado")
            params['estado'] = estado
        if tipo_procedimiento:
            where_clauses.append("tipo_procedimiento = :tipo_proc")
            params['tipo_proc'] = tipo_procedimiento
        if categoria:
            where_clauses.append("categoria = :categoria")
            params['categoria'] = categoria
        if departamento:
            where_clauses.append("departamento = :departamento")
            params['departamento'] = departamento
        
        where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # 1. Total monto estimado y cantidad de licitaciones
        sql_kpis = text(f"""
            SELECT 
                COALESCE(SUM(monto_estimado), 0) as monto_total,
                COUNT(DISTINCT id_convocatoria) as total_licitaciones
            FROM licitaciones_cabecera
            {where_sql}
        """)
        
        result = db.execute(sql_kpis, params).fetchone()
        monto_total = float(result[0]) if result[0] else 0
        total_licitaciones = result[1] or 0
        
        # 2. Top 5 departamentos
        sql_deptos = text(f"""
            SELECT 
                departamento as nombre,
                COUNT(*) as total,
                COALESCE(SUM(monto_estimado), 0) as monto
            FROM licitaciones_cabecera
            WHERE departamento IS NOT NULL AND departamento != ''
            {("AND " + " AND ".join(where_clauses)) if where_clauses else ""}
            GROUP BY departamento
            ORDER BY total DESC
            LIMIT 5
        """)
        
        deptos = db.execute(sql_deptos, params).fetchall()
        top_departamentos = [{"nombre": row[0], "total": row[1], "monto": float(row[2]) if row[2] else 0} for row in deptos]
        
        # 3. Top 5 entidades compradoras
        sql_entidades = text(f"""
            SELECT 
                comprador as nombre,
                COUNT(*) as total,
                COALESCE(SUM(monto_estimado), 0) as monto
            FROM licitaciones_cabecera
            WHERE comprador IS NOT NULL AND comprador != ''
            {("AND " + " AND ".join(where_clauses)) if where_clauses else ""}
            GROUP BY comprador
            ORDER BY total DESC
            LIMIT 5
        """)
        
        entidades = db.execute(sql_entidades, params).fetchall()
        top_entidades = [{"nombre": row[0], "total": row[1], "monto": float(row[2]) if row[2] else 0} for row in entidades]
        
        # 4. Distribución por categoría (Bien/Obra/Servicio/Consultoría)
        sql_categorias = text(f"""
            SELECT 
                categoria as nombre,
                COUNT(*) as total,
                COALESCE(SUM(monto_estimado), 0) as monto
            FROM licitaciones_cabecera
            WHERE categoria IS NOT NULL AND categoria != ''
            {("AND " + " AND ".join(where_clauses)) if where_clauses else ""}
            GROUP BY categoria
            ORDER BY total DESC
        """)
        
        categorias = db.execute(sql_categorias, params).fetchall()
        distribucion_categorias = [{"nombre": row[0], "total": row[1], "monto": float(row[2]) if row[2] else 0} for row in categorias]
        
        # 5. Licitaciones por estado
        sql_estados = text(f"""
            SELECT 
                estado_proceso as nombre,
                COUNT(*) as total
            FROM licitaciones_cabecera
            WHERE estado_proceso IS NOT NULL AND estado_proceso != ''
            {("AND " + " AND ".join(where_clauses)) if where_clauses else ""}
            GROUP BY estado_proceso
            ORDER BY total DESC
        """)
        
        estados = db.execute(sql_estados, params).fetchall()
        distribucion_estados = [{"nombre": row[0], "total": row[1]} for row in estados]
        
        return {
            "monto_total_estimado": str(Decimal(str(monto_total))),
            "total_licitaciones": total_licitaciones,
            "top_departamentos": top_departamentos,
            "top_entidades": top_entidades,
            "distribucion_categorias": distribucion_categorias,
            "distribucion_estados": distribucion_estados
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "monto_total_estimado": "0",
            "total_licitaciones": 0,
            "top_departamentos": [],
            "top_entidades": [],
            "distribucion_estados": []
        }


@router.get("/filter-options")
def get_filter_options(db: Session = Depends(get_db)):
    """
    Get all available filter options for dropdowns (Raw SQL version).
    """
    try:
        # Estados
        estados = db.execute(text("SELECT DISTINCT estado_proceso FROM licitaciones_cabecera WHERE estado_proceso IS NOT NULL AND estado_proceso != '' ORDER BY estado_proceso")).fetchall()
        
        # Categorias
        categorias = db.execute(text("SELECT DISTINCT categoria FROM licitaciones_cabecera WHERE categoria IS NOT NULL AND categoria != '' ORDER BY categoria")).fetchall()
        
        # Departamentos
        deptos = db.execute(text("SELECT DISTINCT departamento FROM licitaciones_cabecera WHERE departamento IS NOT NULL AND departamento != '' ORDER BY departamento")).fetchall()
        
        # Tipos Entidad
        tipos = db.execute(text("SELECT DISTINCT tipo_procedimiento FROM licitaciones_cabecera WHERE tipo_procedimiento IS NOT NULL AND tipo_procedimiento != '' ORDER BY tipo_procedimiento")).fetchall()
        
        # Aseguradoras (check if table exists or has data)
        try:
            aseguradoras = db.execute(text("SELECT DISTINCT entidad_financiera FROM licitaciones_adjudicaciones WHERE entidad_financiera IS NOT NULL AND entidad_financiera != '' ORDER BY entidad_financiera")).fetchall()
        except:
            aseguradoras = []

        return {
            "estados": [r[0] for r in estados],
            "objetos": [r[0] for r in categorias],
            "departamentos": [r[0] for r in deptos],
            "tipos_entidad": [r[0] for r in tipos],
            "aseguradoras": [r[0] for r in aseguradoras]
        }
    except Exception as e:
        print(f"Error getting filter options: {e}")
        return {
            "estados": [],
            "objetos": [],
            "departamentos": [],
            "tipos_entidad": [],
            "aseguradoras": []
        }

@router.get("/distribution-by-type")
def get_distribution_by_type(db: Session = Depends(get_db)):
    try:
        sql = text("""
            SELECT 
                categoria as name,
                COUNT(*) as value,
                COALESCE(SUM(monto_estimado), 0) as amount
            FROM licitaciones_cabecera
            WHERE categoria IS NOT NULL AND categoria != ''
            GROUP BY categoria
            ORDER BY value DESC
        """)
        result = db.execute(sql).fetchall()
        data = [{"name": row[0], "value": row[1], "amount": float(row[2])} for row in result]
        return {"data": data}
    except Exception as e:
        return {"data": [], "error": str(e)}

@router.get("/stats-by-status")
def get_stats_by_status(db: Session = Depends(get_db)):
    try:
        sql = text("""
            SELECT 
                estado_proceso as name,
                COUNT(*) as value
            FROM licitaciones_cabecera
            WHERE estado_proceso IS NOT NULL AND estado_proceso != ''
            GROUP BY estado_proceso
            ORDER BY value DESC
        """)
        result = db.execute(sql).fetchall()
        data = [{"name": row[0], "value": row[1]} for row in result]
        return {"data": data}
    except Exception as e:
        return {"data": [], "error": str(e)}

@router.get("/monthly-trend")
def get_monthly_trend(year: int = 2024, db: Session = Depends(get_db)):
    try:
        sql = text("""
            SELECT 
                MONTH(fecha_publicacion) as mes,
                COUNT(*) as count,
                COALESCE(SUM(monto_estimado), 0) as amount
            FROM licitaciones_cabecera
            WHERE YEAR(fecha_publicacion) = :year
            GROUP BY MONTH(fecha_publicacion)
            ORDER BY mes
        """)
        result = db.execute(sql, {"year": year}).fetchall()
        
        months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        data = []
        for i in range(12):
            month_idx = i + 1
            row = next((r for r in result if r[0] == month_idx), None)
            data.append({
                "name": months[i],
                "count": row[1] if row else 0,
                "value": float(row[2]) if row else 0
            })
            
        return {"data": data}
    except Exception as e:
        return {"data": [], "error": str(e)}

@router.get("/department-ranking")
def get_department_ranking(db: Session = Depends(get_db)):
    try:
        sql = text("""
            SELECT 
                departamento as name,
                COUNT(*) as count,
                COALESCE(SUM(monto_estimado), 0) as amount
            FROM licitaciones_cabecera
            WHERE departamento IS NOT NULL AND departamento != ''
            GROUP BY departamento
            ORDER BY count DESC
            LIMIT 10
        """)
        result = db.execute(sql).fetchall()
        data = [{"name": row[0], "count": row[1], "amount": float(row[2])} for row in result]
        return {"data": data}
    except Exception as e:
        return {"data": [], "error": str(e)}

@router.get("/financial-entities-ranking")
def get_financial_entities_ranking(db: Session = Depends(get_db)):
    try:
        # Use licitaciones_adjudicaciones for entities (Insurers) if available
        # OR licitaciones_cabecera 'comprador' (Entities buying) if preferred?
        # The name "Financial Entities" implies Insurers.
        sql = text("""
            SELECT 
                entidad_financiera as name,
                COUNT(*) as count,
                COALESCE(SUM(monto_adjudicado), 0) as amount
            FROM licitaciones_adjudicaciones
            WHERE entidad_financiera IS NOT NULL 
              AND entidad_financiera != '' 
              AND entidad_financiera != 'SIN_GARANTIA'
              AND entidad_financiera != 'ERROR_API_500'
            GROUP BY entidad_financiera
            ORDER BY count DESC
            LIMIT 10
        """)
        result = db.execute(sql).fetchall()
        data = [{"name": row[0], "count": row[1], "amount": float(row[2])} for row in result]
        return {"data": data}
    except Exception as e:
         # Fallback to Comprador if Adjudicaciones is empty or fails
        try:
             sql_fallback = text("""
                SELECT 
                    comprador as name,
                    COUNT(*) as count,
                    COALESCE(SUM(monto_estimado), 0) as amount
                FROM licitaciones_cabecera
                WHERE comprador IS NOT NULL AND comprador != ''
                GROUP BY comprador
                ORDER BY count DESC
                LIMIT 10
            """)
             result = db.execute(sql_fallback).fetchall()
             data = [{"name": row[0], "count": row[1], "amount": float(row[2])} for row in result]
             return {"data": data}
        except:
            return {"data": [], "error": str(e)}

