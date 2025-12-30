"""
MQS Operations router for managing obras, formatos, renovaciones, fianzas, entregas, and correos.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.dependencies import get_current_user
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal

router = APIRouter(prefix="/api/mqs", tags=["MQS Operations"])


# ============================================
# SCHEMAS
# ============================================

class ObraResponse(BaseModel):
    """Obra (construction project) response."""
    id: int
    nombre: str
    ubicacion: str
    estado: str
    consorcio: str
    
    class Config:
        from_attributes = True


class FormatoResponse(BaseModel):
    """Formato (downloadable format) response."""
    id: int
    nombre: str
    descripcion: str
    tipo: str  # PDF, WORD, EXCEL
    icon: str  # Font Awesome icon class


class RenovacionResponse(BaseModel):
    """Renovación (renewal) response."""
    id: int
    fianza_codigo: str
    beneficiario: str
    vencimiento: date
    estado: str  # URGENTE, POR_VENCER, VIGENTE
    dias_restantes: int


class FianzaResponse(BaseModel):
    """Fianza (guarantee) response."""
    id: int
    codigo: str
    cliente: str
    monto: Decimal
    vencimiento: date
    estado: str


class EntregaResponse(BaseModel):
    """Entrega (delivery) response."""
    id: int
    fianza_codigo: str
    destino: str
    entregado: bool


class CorreoResponse(BaseModel):
    """Correo (email) response."""
    id: int
    asunto: str
    remitente: str
    fecha: datetime
    leido: bool


# ============================================
# ENDPOINTS - OBRAS
# ============================================

@router.get("/obras", response_model=List[ObraResponse])
def get_obras(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of obras (construction projects)."""
    # Mock data for now - replace with actual database queries
    obras = [
        {
            "id": 1,
            "nombre": "Mejoramiento Ruta HU-803",
            "ubicacion": "Chinchao, Huánuco",
            "estado": "En Ejecución",
            "consorcio": "Consorcio Chirapatan"
        }
    ]
    return obras


# ============================================
# ENDPOINTS - FORMATOS
# ============================================

@router.get("/formatos", response_model=List[FormatoResponse])
def get_formatos(current_user: User = Depends(get_current_user)):
    """Get list of downloadable formats."""
    formatos = [
        {"id": 1, "nombre": "Solicitud Carta Fianza", "descripcion": "Formato de solicitud", "tipo": "PDF", "icon": "fa-file-pdf"},
        {"id": 2, "nombre": "Obras Sev y Sum", "descripcion": "Documentación de obras", "tipo": "WORD", "icon": "fa-file-word"},
        {"id": 3, "nombre": "Conocimiento Cliente PJ", "descripcion": "Formato KYC persona jurídica", "tipo": "PDF", "icon": "fa-file-contract"},
        {"id": 4, "nombre": "Relación Patrimonial", "descripcion": "Declaración patrimonial", "tipo": "PDF", "icon": "fa-scale-balanced"},
        {"id": 5, "nombre": "Declaración Jurada", "descripcion": "Declaración jurada general", "tipo": "PDF", "icon": "fa-signature"},
        {"id": 6, "nombre": "Formato P. Natural", "descripcion": "Formato persona natural", "tipo": "PDF", "icon": "fa-user"},
    ]
    return formatos


# ============================================
# ENDPOINTS - RENOVACIONES
# ============================================

@router.get("/renovaciones", response_model=List[RenovacionResponse])
def get_renovaciones(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of fianzas requiring renewal."""
    from datetime import timedelta
    
    # Mock data
    renovaciones = [
        {
            "id": 1,
            "fianza_codigo": "F-001",
            "beneficiario": "Gobierno Regional Huánuco",
            "vencimiento": date.today() + timedelta(days=2),
            "estado": "URGENTE",
            "dias_restantes": 2
        },
        {
            "id": 2,
            "fianza_codigo": "F-002",
            "beneficiario": "Municipalidad Amarilis",
            "vencimiento": date.today() + timedelta(days=15),
            "estado": "VIGENTE",
            "dias_restantes": 15
        }
    ]
    return renovaciones


# ============================================
# ENDPOINTS - FIANZAS
# ============================================

@router.get("/fianzas", response_model=List[FianzaResponse])
def get_fianzas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """Get historical fianzas."""
    # Mock data - generate realistic fianzas
    import random
    empresas = ['Consorcio Vial', 'Constructora Andes', 'Ovaldizan SAC', 'Ingenieros Sur']
    
    fianzas = []
    for i in range(min(limit, 50)):
        dias_offset = random.randint(-30, 60)
        fianzas.append({
            "id": i + 1,
            "codigo": f"F-{202400 + i}",
            "cliente": random.choice(empresas),
            "monto": Decimal(random.randint(10000, 500000)),
            "vencimiento": date.today() + timedelta(days=dias_offset),
            "estado": "VIGENTE" if dias_offset > 5 else ("POR_VENCER" if dias_offset > 0 else "VENCIDA")
        })
    
    return fianzas


# ============================================
# ENDPOINTS - ENTREGAS
# ============================================

@router.get("/entregas", response_model=List[EntregaResponse])
def get_entregas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get delivery status list."""
    entregas = [
        {"id": 1, "fianza_codigo": "F-0089", "destino": "Mesa de Partes", "entregado": False},
        {"id": 2, "fianza_codigo": "F-0090", "destino": "Notaría Gomez", "entregado": True},
    ]
    return entregas


@router.patch("/entregas/{entrega_id}")
def toggle_entrega(
    entrega_id: int,
    entregado: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle delivery status."""
    return {"id": entrega_id, "entregado": entregado, "message": "Estado actualizado"}


# ============================================
# ENDPOINTS - CORREOS
# ============================================

@router.get("/correos", response_model=List[CorreoResponse])
def get_correos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get inbox emails."""
    import random
    empresas = ['Consorcio Vial', 'Constructora Andes', 'Ovaldizan SAC', 'Ingenieros Sur']
    
    correos = []
    for i in range(min(limit, 20)):
        correos.append({
            "id": i + 1,
            "asunto": f"Asunto Importante #{i + 1}",
            "remitente": random.choice(empresas),
            "fecha": datetime.now(),
            "leido": random.choice([True, False])
        })
    
    return correos


@router.patch("/correos/{correo_id}/read")
def mark_correo_read(
    correo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark email as read."""
    return {"id": correo_id, "leido": True, "message": "Correo marcado como leído"}


# ============================================
# ENDPOINTS - CONSORCIOS/ENTIDADES (OBRAS)
# ============================================

@router.get("/consorcios")
def get_consorcios(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of unique consorcios/entities from database."""
    from sqlalchemy import func, distinct
    from app.models.seace import LicitacionesAdjudicaciones, LicitacionesCabecera
    
    # Get unique winners (ganadores) with their licitaciones count
    consorcios = db.query(
        LicitacionesAdjudicaciones.ganador_nombre,
        LicitacionesAdjudicaciones.ganador_ruc,
        func.count(LicitacionesAdjudicaciones.id_adjudicacion).label('total_licitaciones'),
        func.sum(LicitacionesAdjudicaciones.monto_adjudicado).label('monto_total')
    ).filter(
        LicitacionesAdjudicaciones.ganador_nombre.isnot(None)
    ).group_by(
        LicitacionesAdjudicaciones.ganador_nombre,
        LicitacionesAdjudicaciones.ganador_ruc
    ).order_by(
        func.count(LicitacionesAdjudicaciones.id_adjudicacion).desc()
    ).limit(50).all()
    
    result = []
    for consorcio in consorcios:
        result.append({
            "nombre": consorcio.ganador_nombre,
            "ruc": consorcio.ganador_ruc,
            "total_licitaciones": consorcio.total_licitaciones,
            "monto_total": float(consorcio.monto_total) if consorcio.monto_total else 0
        })
    
    return result


@router.get("/consorcios/{ruc}/detalles")
def get_consorcio_detalles(
    ruc: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information for a specific consorcio by RUC."""
    from app.models.seace import LicitacionesAdjudicaciones, LicitacionesCabecera, DetalleConsorcios
    
    # Get all licitaciones for this consorcio
    licitaciones = db.query(
        LicitacionesAdjudicaciones,
        LicitacionesCabecera
    ).join(
        LicitacionesCabecera,
        LicitacionesAdjudicaciones.id_convocatoria == LicitacionesCabecera.id_convocatoria
    ).filter(
        LicitacionesAdjudicaciones.ganador_ruc == ruc
    ).all()
    
    # Get consorcio members if exists
    miembros = db.query(DetalleConsorcios).filter(
        DetalleConsorcios.ruc_miembro == ruc
    ).all()
    
    result = {
        "ruc": ruc,
        "nombre": licitaciones[0][0].ganador_nombre if licitaciones else "Desconocido",
        "total_licitaciones": len(licitaciones),
        "monto_total": sum([float(lic[0].monto_adjudicado or 0) for lic in licitaciones]),
        "licitaciones": [],
        "miembros": []
    }
    
    for adj, cab in licitaciones:
        result["licitaciones"].append({
            "id_convocatoria": cab.id_convocatoria,
            "nomenclatura": cab.nomenclatura,
            "descripcion": cab.descripcion,
            "entidad": cab.comprador,
            "monto_adjudicado": float(adj.monto_adjudicado or 0),
            "fecha_adjudicacion": str(adj.fecha_adjudicacion) if adj.fecha_adjudicacion else None,
            "estado": cab.estado_proceso,
            "ubicacion": cab.ubicacion_completa,
            "departamento": cab.departamento
        })
    
    for miembro in miembros:
        result["miembros"].append({
            "nombre": miembro.nombre_miembro,
            "ruc": miembro.ruc_miembro,
            "porcentaje": float(miembro.porcentaje_participacion or 0)
        })
    
    return result

