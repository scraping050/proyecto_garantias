"""
Test Groq API connectivity and diagnose issues
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("="*80)
print("GROQ API DIAGNOSTIC TEST")
print("="*80)

# Check API key
api_key = os.getenv("GROQ_API_KEY")
print(f"\n1. API Key loaded: {'YES' if api_key else 'NO'}")
if api_key:
    print(f"   Key preview: {api_key[:20]}...{api_key[-10:]}")

# Test connection
try:
    print("\n2. Testing Groq connection...")
    from openai import OpenAI
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    print("   Client created successfully")
    
    # Simple test
    print("\n3. Sending test message...")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Di solo 'funciona' si puedes leerme"}
        ],
        temperature=0.5,
        max_tokens=20
    )
    
    response = completion.choices[0].message.content
    print(f"   Response: {response}")
    print("\n   ✅ SUCCESS - Groq API is working!")
    
except Exception as e:
    print(f"\n   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
