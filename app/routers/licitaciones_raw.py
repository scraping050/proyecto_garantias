"""
Raw SQL licitaciones endpoint - bypasses SQLAlchemy mapper issues
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import Optional
from datetime import date

router = APIRouter(prefix="/api/licitaciones", tags=["Licitaciones"])


@router.get("")
def get_licitaciones(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    categoria: Optional[str] = Query(None),
    departamento: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of licitaciones using RAW SQL.
    Returns data from licitaciones_cabecera table.
    """
    
    try:
        # Build WHERE clause
        where_clauses = []
        params = {}
        
        if search:
            where_clauses.append("(nomenclatura LIKE :search OR comprador LIKE :search)")
            params['search'] = f"%{search}%"
        if estado:
            where_clauses.append("estado_proceso = :estado")
            params['estado'] = estado
        if categoria:
            where_clauses.append("categoria = :categoria")
            params['categoria'] = categoria
        if departamento:
            where_clauses.append("departamento = :departamento")
            params['departamento'] = departamento
        
        where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # Get total count
        count_sql = text(f"""
            SELECT COUNT(DISTINCT id_convocatoria)
            FROM licitaciones_cabecera
            {where_sql}
        """)
        
        total = db.execute(count_sql, params).scalar() or 0
        
        # Get paginated data
        offset = (page - 1) * limit
        data_sql = text(f"""
            SELECT 
                id_convocatoria,
                ocid,
                nomenclatura,
                descripcion,
                comprador,
                categoria,
                tipo_procedimiento,
                monto_estimado,
                moneda,
                fecha_publicacion,
                estado_proceso,
                ubicacion_completa,
                departamento,
                provincia,
                distrito
            FROM licitaciones_cabecera
            {where_sql}
            ORDER BY fecha_publicacion DESC
            LIMIT :limit OFFSET :offset
        """)
        
        params['limit'] = limit
        params['offset'] = offset
        
        rows = db.execute(data_sql, params).fetchall()
        
        # Format results
        items = []
        for row in rows:
            items.append({
                "id_convocatoria": row[0],
                "ocid": row[1],
                "nomenclatura": row[2],
                "descripcion": row[3],
                "comprador": row[4],
                "categoria": row[5],
                "tipo_procedimiento": row[6],
                "monto_estimado": float(row[7]) if row[7] else 0,
                "moneda": row[8],
                "fecha_publicacion": row[9].isoformat() if row[9] else None,
                "estado_proceso": row[10],
                "ubicacion_completa": row[11],
                "departamento": row[12],
                "provincia": row[13],
                "distrito": row[14]
            })
        
        # Calculate pagination
        total_pages = (total + limit - 1) // limit if limit > 0 else 0
        
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "items": items
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "total": 0,
            "page": page,
            "limit": limit,
            "total_pages": 0,
            "items": []
        }


@router.get("/{id_convocatoria}")
def get_licitacion_detail(
    id_convocatoria: str,
    db: Session = Depends(get_db)
):
    """
    Get licitacion detail with adjudicaciones.
    """
    
    try:
        # Get main licitacion data
        main_sql = text("""
            SELECT 
                id_convocatoria, ocid, nomenclatura, descripcion,
                comprador, categoria, tipo_procedimiento,
                monto_estimado, moneda, fecha_publicacion,
                estado_proceso, ubicacion_completa,
                departamento, provincia, distrito
            FROM licitaciones_cabecera
            WHERE id_convocatoria = :id
        """)
        
        row = db.execute(main_sql, {"id": id_convocatoria}).fetchone()
        
        if not row:
            return {"error": "Not found"}
        
        licitacion = {
            "id_convocatoria": row[0],
            "ocid": row[1],
            "nomenclatura": row[2],
            "descripcion": row[3],
            "comprador": row[4],
            "categoria": row[5],
            "tipo_procedimiento": row[6],
            "monto_estimado": float(row[7]) if row[7] else 0,
            "moneda": row[8],
            "fecha_publicacion": row[9].isoformat() if row[9] else None,
            "estado_proceso": row[10],
            "ubicacion_completa": row[11],
            "departamento": row[12],
            "provincia": row[13],
            "distrito": row[14]
        }
        
        # Get adjudicaciones
        adj_sql = text("""
            SELECT 
                id_adjudicacion, ganador_nombre, ganador_ruc,
                monto_adjudicado, fecha_adjudicacion,
                estado_item, entidad_financiera
            FROM licitaciones_adjudicaciones
            WHERE id_convocatoria = :id
        """)
        
        adj_rows = db.execute(adj_sql, {"id": id_convocatoria}).fetchall()
        
        adjudicaciones = []
        for adj_row in adj_rows:
            adjudicaciones.append({
                "id_adjudicacion": adj_row[0],
                "ganador_nombre": adj_row[1],
                "ganador_ruc": adj_row[2],
                "monto_adjudicado": float(adj_row[3]) if adj_row[3] else 0,
                "fecha_adjudicacion": adj_row[4].isoformat() if adj_row[4] else None,
                "estado_item": adj_row[5],
                "entidad_financiera": adj_row[6]
            })
        
        licitacion["adjudicaciones"] = adjudicaciones
        
        return licitacion
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
