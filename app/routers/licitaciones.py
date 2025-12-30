"""
Licitaciones endpoints for listing and detail views.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from app.database import get_db
from app.models.seace import LicitacionesCabecera, LicitacionesAdjudicaciones
from app.schemas import (
    LicitacionListSchema,
    LicitacionDetalleSchema,
    PaginatedLicitacionesSchema
)
from typing import Optional
from datetime import date
import math

router = APIRouter(prefix="/api/licitaciones", tags=["Licitaciones"])


@router.get("", response_model=PaginatedLicitacionesSchema)
def get_licitaciones(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=1000, description="Items per page (max 1000)"),
    search: Optional[str] = Query(None, description="Search in nomenclatura, comprador, descripcion"),
    estado: Optional[str] = Query(None, description="Filter by estado_proceso"),
    ruc_ganador: Optional[str] = Query(None, description="Filter by winner RUC"),
    entidad_financiera: Optional[str] = Query(None, description="Filter by bank/financial entity"),
    # New filters
    departamento: Optional[str] = Query(None, description="Filter by department"),
    provincia: Optional[str] = Query(None, description="Filter by province"),
    distrito: Optional[str] = Query(None, description="Filter by district"),
    year: Optional[int] = Query(None, description="Filter by publication year"),
    mes: Optional[int] = Query(None, description="Filter by publication month"),
    categoria: Optional[str] = Query(None, description="Filter by category"),
    tipo_garantia: Optional[str] = Query(None, description="Filter by guarantee type"),
    fecha_desde: Optional[date] = Query(None, description="Filter from date (ISO format)"),
    fecha_hasta: Optional[date] = Query(None, description="Filter to date (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of tenders with optional filters.
    
    Filters:
    - search: Search in nomenclatura, comprador, or descripcion
    - estado: Filter by estado_proceso
    - ruc_ganador: Filter by winner's RUC
    - entidad_financiera: Filter by bank/guarantee issuer
    - fecha_desde/fecha_hasta: Filter by adjudication date range
    - location: departamento, provincia, distrito
    - time: year, mes
    - details: categoria, tipo_garantia
    """
    
    from sqlalchemy import extract

    # Base query
    query = db.query(LicitacionesCabecera)
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (LicitacionesCabecera.nomenclatura.like(search_term)) |
            (LicitacionesCabecera.comprador.like(search_term)) |
            (LicitacionesCabecera.descripcion.like(search_term)) |
            (LicitacionesCabecera.ocid.like(search_term))
        )
    
    # Simple filters
    if estado:
        query = query.filter(LicitacionesCabecera.estado_proceso == estado)
    if departamento:
        query = query.filter(LicitacionesCabecera.departamento == departamento)
    if provincia:
        query = query.filter(LicitacionesCabecera.provincia == provincia)
    if distrito:
        query = query.filter(LicitacionesCabecera.distrito == distrito)
    if categoria:
        query = query.filter(LicitacionesCabecera.categoria == categoria)
        
    # Date filters on Cabecera
    if year:
        query = query.filter(extract('year', LicitacionesCabecera.fecha_publicacion) == year)
    if mes:
        query = query.filter(extract('month', LicitacionesCabecera.fecha_publicacion) == mes)

    # Filters requiring Join with Adjudicaciones
    adjudicacion_joined = False
    
    # Helper to ensure join only happens once
    def ensure_adj_join(q, joined):
        if not joined:
            q = q.join(LicitacionesCabecera.adjudicaciones)
            return q, True
        return q, True

    if ruc_ganador:
        query, adjudicacion_joined = ensure_adj_join(query, adjudicacion_joined)
        query = query.filter(LicitacionesAdjudicaciones.ganador_ruc == ruc_ganador)
    
    if entidad_financiera:
        query, adjudicacion_joined = ensure_adj_join(query, adjudicacion_joined)
        query = query.filter(
            LicitacionesAdjudicaciones.entidad_financiera.like(f"%{entidad_financiera}%")
        )

    if tipo_garantia:
        query, adjudicacion_joined = ensure_adj_join(query, adjudicacion_joined)
        query = query.filter(LicitacionesAdjudicaciones.tipo_garantia == tipo_garantia)

    if fecha_desde or fecha_hasta:
        query, adjudicacion_joined = ensure_adj_join(query, adjudicacion_joined)
        if fecha_desde:
            query = query.filter(LicitacionesAdjudicaciones.fecha_adjudicacion >= fecha_desde)
        if fecha_hasta:
            query = query.filter(LicitacionesAdjudicaciones.fecha_adjudicacion <= fecha_hasta)
    
    # Get total count
    total = query.distinct().count()
    
    # Calculate pagination
    total_pages = math.ceil(total / limit) if total > 0 else 0
    offset = (page - 1) * limit
    
    # Get paginated results - order by most recent
    items = query.distinct().order_by(
        LicitacionesCabecera.fecha_publicacion.desc()
    ).offset(offset).limit(limit).all()
    
    return PaginatedLicitacionesSchema(
        items=items,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )


@router.get("/{id_convocatoria}", response_model=LicitacionDetalleSchema)
def get_licitacion_detalle(
    id_convocatoria: str,
    db: Session = Depends(get_db)
):
    """
    Get complete tender details including:
    - Header information
    - Adjudication details
    - Consortium members (if any)
    """
    
    # Query with eager loading for optimal performance
    licitacion = db.query(LicitacionesCabecera).options(
        joinedload(LicitacionesCabecera.adjudicaciones)
    ).filter(
        LicitacionesCabecera.id_convocatoria == id_convocatoria
    ).first()
    
    if not licitacion:
        raise HTTPException(
            status_code=404,
            detail=f"Licitación con id_convocatoria={id_convocatoria} no encontrada"
        )
    
    # Build response with first adjudication (if exists)
    adjudicacion = None
    if licitacion.adjudicaciones:
        from app.models import DetalleConsorcios
        adj = licitacion.adjudicaciones[0]
        
        # Manually load consorcios for this adjudication
        consorcios = []
        if adj.id_contrato:
            consorcios = db.query(DetalleConsorcios).filter(
                DetalleConsorcios.id_contrato == adj.id_contrato
            ).all()
        
        # Build adjudication schema with consorcios
        from app.schemas import AdjudicacionSchema
        adjudicacion = AdjudicacionSchema.model_validate(adj)
        adjudicacion.consorcios = consorcios
    
    return LicitacionDetalleSchema(
        id_convocatoria=licitacion.id_convocatoria,
        ocid=licitacion.ocid,
        nomenclatura=licitacion.nomenclatura,
        descripcion=licitacion.descripcion,
        comprador=licitacion.comprador,
        categoria=licitacion.categoria,
        tipo_procedimiento=licitacion.tipo_procedimiento,
        monto_estimado=licitacion.monto_estimado,
        moneda=licitacion.moneda,
        fecha_publicacion=licitacion.fecha_publicacion,
        estado_proceso=licitacion.estado_proceso,
        ubicacion_completa=licitacion.ubicacion_completa,
        departamento=licitacion.departamento,
        provincia=licitacion.provincia,
        distrito=licitacion.distrito,
        adjudicacion=adjudicacion
    )
