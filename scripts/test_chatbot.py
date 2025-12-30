"""
Test the enhanced chatbot with Text-to-SQL
"""
import requests
import json

API_URL = "http://localhost:8000"

print("="*80)
print("TESTING ENHANCED CHATBOT")
print("="*80)

# Test 1: Health check
print("\n1. Health Check...")
try:
    response = requests.get(f"{API_URL}/api/chatbot/health", timeout=10)
    print(f"   Status: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Simple question (no database)
print("\n2. Simple Question (No DB)...")
try:
    response = requests.post(
        f"{API_URL}/api/chatbot/chat",
        json={"message": "Hola, ¿cómo estás?"},
        timeout=30
    )
    data = response.json()
    print(f"   Response: {data['response'][:100]}...")
    print(f"   Has Data: {data.get('has_data', False)}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Database question
print("\n3. Database Question...")
test_questions = [
    "¿Cuántas licitaciones hay en total?",
    "¿Cuántas licitaciones hay en Lima?",
    "Muéstrame el top 5 de departamentos con más licitaciones"
]

for question in test_questions:
    print(f"\n   Q: {question}")
    try:
        response = requests.post(
            f"{API_URL}/api/chatbot/chat",
            json={"message": question},
            timeout=30
        )
        data = response.json()
        print(f"   A: {data['response'][:200]}...")
        if data.get('has_data'):
            print(f"   📊 SQL Executed: {data.get('data', {}).get('sql', 'N/A')}")
            print(f"   📊 Results: {len(data.get('data', {}).get('results', []))} rows")
    except Exception as e:
        print(f"   Error: {e}")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
