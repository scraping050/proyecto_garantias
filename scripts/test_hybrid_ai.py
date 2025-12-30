"""
Test hybrid AI service
"""
import sys
sys.path.insert(0, 'c:/laragon/www/proyecto_garantias')

from app.services.hybrid_ai_service import hybrid_ai_service

print("="*80)
print("TESTING HYBRID AI SERVICE")
print("="*80)

# Test 1: Simple response
print("\n1. Testing simple response...")
try:
    response = hybrid_ai_service.generate_response("Hola, ¿cómo estás?", [])
    if response:
        print(f"   ✅ Response: {response[:100]}...")
    else:
        print("   ❌ No response")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: SQL generation
print("\n2. Testing SQL Generation...")
try:
    sql = hybrid_ai_service.generate_sql("¿Cuántas licitaciones hay en total?")
    if sql:
        print(f"   ✅ Generated SQL: {sql}")
    else:
        print("   ❌ No SQL generated")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
