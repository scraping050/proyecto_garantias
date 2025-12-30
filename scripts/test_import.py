import sys
import os
sys.path.append(os.getcwd())

print("Importing models...")
try:
    from app.models.seace import LicitacionesCabecera, LicitacionesAdjudicaciones
    print("Import successful!")
    
    from app.database import engine
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("Mappers configured!")
    
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
