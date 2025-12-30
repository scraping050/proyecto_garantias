"""
Admin router for financial management (cheques, primas, facturas, flujo de caja).
Only accessible by users with admin role.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.dependencies import get_current_admin_user
from typing import List
from pydantic import BaseModel
from datetime import date
from decimal import Decimal

router = APIRouter(prefix="/api/admin", tags=["Admin - Financial Management"])


# ============================================
# SCHEMAS
# ============================================

class ChequeResponse(BaseModel):
    """Cheque response."""
    id: int
    fecha: date
    girado_a: str
    concepto: str
    monto: Decimal
    estado: str  # Cobrado, Pendiente


class PrimaResponse(BaseModel):
    """Prima (premium) for approval."""
    id: int
    obra: str
    monto: Decimal
    estado: str  # Pendiente, Aprobado, Rechazado


class FacturaResponse(BaseModel):
    """Factura (invoice) response."""
    id: int
    proveedor: str
    numero_factura: str
    monto: Decimal
    pdf_url: str


class FlujoCajaResponse(BaseModel):
    """Cash flow data response."""
    mes: str
    ingresos: Decimal
    egresos: Decimal


# ============================================
# ENDPOINTS - CHEQUES
# ============================================

@router.get("/cheques", response_model=List[ChequeResponse])
def get_cheques(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get list of cheques (admin only)."""
    import random
    from datetime import timedelta
    
    empresas = ['Consorcio Vial', 'Constructora Andes', 'Ovaldizan SAC', 'Ingenieros Sur']
    conceptos = ['Pago Valorización', 'Adelanto', 'Liquidación', 'Servicios']
    
    cheques = []
    for i in range(min(limit, 50)):
        cobrado = random.choice([True, False, True, True])  # 75% cobrado
        cheques.append({
            "id": i + 1,
            "fecha": date.today() - timedelta(days=i),
            "girado_a": random.choice(empresas),
            "concepto": random.choice(conceptos),
            "monto": Decimal(random.randint(5000, 50000)),
            "estado": "Cobrado" if cobrado else "Pendiente"
        })
    
    return cheques


# ============================================
# ENDPOINTS - PRIMAS
# ============================================

@router.get("/primas", response_model=List[PrimaResponse])
def get_primas_pendientes(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get primas pending approval (admin only)."""
    primas = [
        {"id": 1, "obra": "Mejoramiento Vial", "monto": Decimal(5000), "estado": "Pendiente"},
        {"id": 2, "obra": "Construcción Puente", "monto": Decimal(8500), "estado": "Pendiente"},
    ]
    return primas


@router.post("/primas/{prima_id}/approve")
def approve_prima(
    prima_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Approve a prima (admin only)."""
    return {"id": prima_id, "estado": "Aprobado", "message": "Prima aprobada exitosamente"}


@router.post("/primas/{prima_id}/reject")
def reject_prima(
    prima_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Reject a prima (admin only)."""
    return {"id": prima_id, "estado": "Rechazado", "message": "Prima rechazada"}


# ============================================
# ENDPOINTS - FACTURAS
# ============================================

@router.get("/facturas", response_model=List[FacturaResponse])
def get_facturas(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get invoices repository (admin only)."""
    facturas = [
        {"id": 1, "proveedor": "Aceros S.A.", "numero_factura": "F001-992", "monto": Decimal(12000), "pdf_url": "/facturas/f001-992.pdf"},
        {"id": 2, "proveedor": "Cemento Lima", "numero_factura": "F002-445", "monto": Decimal(8500), "pdf_url": "/facturas/f002-445.pdf"},
    ]
    return facturas


# ============================================
# ENDPOINTS - FLUJO DE CAJA
# ============================================

@router.get("/flujo-caja", response_model=List[FlujoCajaResponse])
def get_flujo_caja(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get cash flow data for chart (admin only)."""
    flujo = [
        {"mes": "Ene", "ingresos": Decimal(120000), "egresos": Decimal(100000)},
        {"mes": "Feb", "ingresos": Decimal(190000), "egresos": Decimal(150000)},
        {"mes": "Mar", "ingresos": Decimal(30000), "egresos": Decimal(80000)},
        {"mes": "Abr", "ingresos": Decimal(50000), "egresos": Decimal(120000)},
    ]
    return flujo


@router.get("/flujo-caja/summary")
def get_flujo_caja_summary(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get cash flow summary (admin only)."""
    return {
        "saldo_actual": Decimal(1240500),
        "ingresos_mes": Decimal(50000),
        "egresos_mes": Decimal(120000),
        "proyeccion_mes": Decimal(1170500)
    }
