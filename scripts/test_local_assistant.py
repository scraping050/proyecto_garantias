"""
Simple test of local assistant
"""
import sys
sys.path.insert(0, 'c:/laragon/www/proyecto_garantias')

from app.database import SessionLocal
from app.services.local_assistant import local_assistant

db = SessionLocal()

print("="*80)
print("TESTING LOCAL ASSISTANT")
print("="*80)

# Test 1: Simple count
print("\n1. Test: ¿Cuántas licitaciones hay en Lima?")
try:
    result = local_assistant.process_message("cuantas licitaciones hay en lima", db, [])
    print(f"Response: {result['response']}")
    print(f"Has data: {result.get('has_data')}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Total general
print("\n2. Test: ¿Cuántas licitaciones hay en total?")
try:
    result = local_assistant.process_message("cuantas licitaciones hay", db, [])
    print(f"Response: {result['response']}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 3: Help query
print("\n3. Test: ¿Qué es SEACE?")
try:
    result = local_assistant.process_message("que es seace", db, [])
    print(f"Response: {result['response'][:200]}...")
except Exception as e:
    print(f"ERROR: {e}")

db.close()
print("\n" + "="*80)
