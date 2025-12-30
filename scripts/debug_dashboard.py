import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker
from app.models.seace import LicitacionesCabecera, LicitacionesAdjudicaciones
from app.database import DATABASE_URL

# Setup DB connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print("Testing Dashboard Query...")
    
    # Test 1: Count Cabecera
    count = db.query(LicitacionesCabecera).count()
    print(f"Total Licitaciones: {count}")

    # Test 2: Sum Adjudicaciones
    total_amount = db.query(
        func.sum(LicitacionesAdjudicaciones.monto_adjudicado)
    ).scalar()
    print(f"Total Amount: {total_amount}")

    # Test 3: Join Query (likely culprit)
    print("Testing Join Query...")
    query = db.query(LicitacionesAdjudicaciones).join(
        LicitacionesCabecera,
        LicitacionesAdjudicaciones.id_convocatoria == LicitacionesCabecera.id_convocatoria
    ).limit(5)
    results = query.all()
    print(f"Join Query Results: {len(results)}")

except Exception as e:
    print(f"\nERROR DETECTED:\n{e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
