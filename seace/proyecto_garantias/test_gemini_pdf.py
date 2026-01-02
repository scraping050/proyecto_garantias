"""
Test con Gemini para procesar UN PDF escaneado
"""
import os
import sys

# Configurar encoding UTF-8
if sys.platform.startswith('win'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

import google.generativeai as genai
import time

# Configurar variables de entorno
os.environ['GARANTIAS_GEMINI_API_KEY'] = 'YOUR_API_KEY_HERE'

GEMINI_API_KEY = os.environ['GARANTIAS_GEMINI_API_KEY']
genai.configure(api_key=GEMINI_API_KEY)

print("=" * 60)
print("TEST GEMINI - PDF ESCANEADO")
print("=" * 60)

# Usar el PDF que ya descargamos
ruta_pdf = r"C:\laragon\www\proyecto_garantias\evidencia_consorcios\2280973_test.pdf"

if not os.path.exists(ruta_pdf):
    print(f"❌ PDF no encontrado: {ruta_pdf}")
    sys.exit(1)

print(f"\n1. PDF a procesar: {ruta_pdf}")
print(f"   Tamaño: {os.path.getsize(ruta_pdf) / (1024*1024):.2f} MB")

print("\n2. Subiendo PDF a Gemini...")
try:
    archivo = genai.upload_file(ruta_pdf, mime_type='application/pdf')
    print(f"   ✅ Archivo subido: {archivo.name}")
    
    # Esperar procesamiento
    print("\n3. Esperando procesamiento...")
    wait_count = 0
    while archivo.state.name == "PROCESSING":
        time.sleep(2)
        archivo = genai.get_file(archivo.name)
        wait_count += 1
        print(f"   ⏳ Procesando... ({wait_count * 2}s)")
        if wait_count > 45:
            print("   ❌ Timeout")
            sys.exit(1)
    
    if archivo.state.name == "FAILED":
        print("   ❌ Google marcó como FAILED")
        sys.exit(1)
    
    print(f"   ✅ Estado: {archivo.state.name}")
    
    print("\n4. Enviando prompt a Gemini 2.0 Flash...")
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    prompt = """
    Eres un experto digitador de contratos públicos.
    Tarea: Extrae los miembros del CONSORCIO (las empresas privadas, no la entidad pública).
    
    Salida JSON estricta: 
    [{"ruc": "...", "nombre": "...", "participacion": 50.0}]
    
    Reglas: 
    - RUC: Solo números. Si no hay, null.
    - Participación: Número decimal.
    """
    
    res = model.generate_content([archivo, prompt])
    
    print(f"\n5. Respuesta de Gemini:")
    print("=" * 60)
    print(res.text)
    print("=" * 60)
    
    # Limpiar
    try:
        genai.delete_file(archivo.name)
        print(f"\n✅ Archivo eliminado de Google Cloud")
    except:
        pass
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
