import sys
import os
sys.path.append(os.getcwd())

print("Testing backend components...")

try:
    from app.models.seace import LicitacionesCabecera, LicitacionesAdjudicaciones
    print("OK: Models imported")
    
    from app.database import engine
    from sqlalchemy.orm import sessionmaker
    
    Session = sessionmaker(bind=engine)
    db = Session()
    
    count = db.query(LicitacionesCabecera).count()
    print(f"OK: Database query works - {count} records")
    
    total = db.query(__import__('sqlalchemy').func.sum(LicitacionesAdjudicaciones.monto_adjudicado)).scalar()
    print(f"OK: Aggregation works - Total: {total}")
    
    db.close()
    print("SUCCESS: All tests passed")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
