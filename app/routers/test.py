"""
Minimal test router to verify database connection
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/api/test", tags=["Test"])

@router.get("/db")
def test_database(db: Session = Depends(get_db)):
    """Test database connection without using models"""
    try:
        # Simple raw SQL query
        result = db.execute(text("SELECT COUNT(*) as total FROM licitaciones_cabecera")).fetchone()
        total_sum = db.execute(text("SELECT SUM(monto_adjudicado) as sum FROM licitaciones_adjudicaciones")).fetchone()
        
        return {
            "status": "ok",
            "total_licitaciones": result.total if result else 0,
            "total_adjudicado": float(total_sum.sum) if total_sum and total_sum.sum else 0
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
