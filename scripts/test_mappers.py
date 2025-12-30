import sys
import os
sys.path.append(os.getcwd())

print("Testing mapper configuration...")

try:
    # Clear any metadata
    from sqlalchemy.orm import clear_mappers
    clear_mappers()
    print("Cleared existing mappers")
    
    # Import models
    from app.models.seace import LicitacionesCabecera, LicitacionesAdjudicaciones
    print("Models imported")
    
    # Try to configure mappers explicitly
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("SUCCESS: Mappers configured!")
    
except Exception as e:
    print(f"FAIL: {e}")
    import traceback
    traceback.print_exc()
