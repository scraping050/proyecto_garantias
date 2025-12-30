import sys
import os
sys.path.append(os.getcwd())

print("="*80)
print("DIAGNOSTIC SCRIPT - Backend Models & Database")
print("="*80)

try:
    print("\n1. Testing database connection...")
    from app.database import DATABASE_URL, engine
    print(f"   ✓ Database URL: {DATABASE_URL[:50]}...")
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(__import__('sqlalchemy').text("SELECT 1"))
        print("   ✓ Database connection successful")
        
except Exception as e:
    print(f"   ✗ Database error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n2. Testing model imports...")
    from app.models.seace import LicitacionesCabecera, LicitacionesAdjudicaciones
    print("   ✓ SEACE models imported successfully")
    
except Exception as e:
    print(f"   ✗ Model import error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n3. Testing mapper configuration...")
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("   ✓ Mappers configured successfully")
    
except Exception as e:
    print(f"   ✗ Mapper configuration error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n4. Testing database query...")
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    count = session.query(LicitacionesCabecera).count()
    print(f"   ✓ Query successful: {count} records in licitaciones_cabecera")
    
    session.close()
    
except Exception as e:
    print(f"   ✗ Query error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n5. Testing dashboard endpoint logic...")
    from app.routers.dashboard import get_dashboard_kpis
    from sqlalchemy.orm import Session
    
    session = sessionmaker(bind=engine)()
    result = get_dashboard_kpis(None, None, None, None, session)
    print(f"   ✓ Dashboard endpoint logic works: {result}")
    session.close()
    
except Exception as e:
    print(f"   ✗ Dashboard endpoint error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)
