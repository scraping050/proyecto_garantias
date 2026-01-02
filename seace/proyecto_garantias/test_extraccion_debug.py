"""
Script de prueba para diagnosticar el problema de extracción de consorcios.
Procesa SOLO 1 contrato con logs muy detallados.
"""
import os
import sys
import json
import pypdf
import mysql.connector
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Configurar variables de entorno ANTES de importar secrets_manager
os.environ['GARANTIAS_DB_HOST'] = 'localhost'
os.environ['GARANTIAS_DB_USER'] = 'root'
os.environ['GARANTIAS_DB_PASS'] = '123456789'
os.environ['GARANTIAS_DB_NAME'] = 'garantias_seace'
os.environ['GARANTIAS_GEMINI_API_KEY'] = 'YOUR_API_KEY_HERE'
os.environ['GARANTIAS_GROQ_API_KEY'] = 'YOUR_GROQ_API_KEY_HERE'
os.environ['GARANTIAS_EMAIL_USER'] = 'test@test.com'
os.environ['GARANTIAS_EMAIL_PASS'] = 'test'
os.environ['GARANTIAS_EMAIL_TO'] = 'test@test.com'

# Configuración
if sys.platform.startswith('win'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = script_dir  # Este script está en la raíz del proyecto

sys.path.insert(0, os.path.join(parent_dir, 'config'))
from secrets_manager import config, get_db_config

CARPETA_EVIDENCIA = os.path.join(script_dir, "evidencia_consorcios")
if not os.path.exists(CARPETA_EVIDENCIA): 
    os.makedirs(CARPETA_EVIDENCIA)
    print(f"✅ Carpeta creada: {CARPETA_EVIDENCIA}")

DB_CONFIG = get_db_config()
ai_config = config.get_ai_config()

print("=" * 60)
print("TEST DE DIAGNÓSTICO - EXTRACCIÓN DE CONSORCIOS")
print("=" * 60)

# Verificar API keys
print("\n1. Verificando configuración...")
print(f"   ✅ DB Config: {DB_CONFIG['host']}/{DB_CONFIG['database']}")
print(f"   ✅ Gemini API: {'*' * 20}...{ai_config.gemini_api_key[-4:]}")
if ai_config.groq_api_key:
    print(f"   ✅ Groq API: {'*' * 20}...{ai_config.groq_api_key[-4:]}")
    GROQ_API_KEY = ai_config.groq_api_key
    USAR_GROQ = True
else:
    print(f"   ⚠️ Groq API: No configurada, usando Gemini")
    USAR_GROQ = False

# URLs
URL_METADATA = "https://prod4.seace.gob.pe:9000/api/bus/contrato/idContrato/{}"
URL_DESCARGA = "https://prod4.seace.gob.pe:9000/api/con/documentos/descargar/{}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

print("\n2. Obteniendo UN contrato de prueba...")
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    sql = """
        SELECT a.id_contrato, a.ganador_nombre 
        FROM Licitaciones_Adjudicaciones a
        LEFT JOIN Detalle_Consorcios d ON a.id_contrato = d.id_contrato
        WHERE a.ganador_nombre LIKE '%CONSORCIO%' 
          AND d.id_contrato IS NULL
          AND a.id_contrato IS NOT NULL AND a.id_contrato != ''
        LIMIT 1
    """
    cursor.execute(sql)
    resultado = cursor.fetchone()
    conn.close()
    
    if not resultado:
        print("   ❌ No hay contratos pendientes")
        sys.exit(1)
    
    id_contrato, ganador = resultado
    print(f"   ✅ Contrato encontrado:")
    print(f"      ID: {id_contrato}")
    print(f"      Ganador: {ganador}")
    
except Exception as e:
    print(f"   ❌ Error DB: {e}")
    sys.exit(1)

print("\n3. Descargando metadata del contrato...")
try:
    r = requests.get(URL_METADATA.format(id_contrato), headers=HEADERS, verify=False, timeout=10)
    print(f"   Status: {r.status_code}")
    
    if r.status_code != 200:
        print(f"   ❌ Error descargando metadata")
        sys.exit(1)
    
    data = r.json()
    print(f"   ✅ Metadata recibida")
    
    # Buscar ID del documento
    id_doc = None
    if data.get("idDocumentoConsorcio"): 
        id_doc = data.get("idDocumentoConsorcio")
        print(f"   ✅ Encontrado idDocumentoConsorcio: {id_doc}")
    elif data.get("idDocumento2"):
        id_doc = data.get("idDocumento2")
        print(f"   ✅ Encontrado idDocumento2: {id_doc}")
    elif data.get("idDocumento"):
        id_doc = data.get("idDocumento")
        print(f"   ✅ Encontrado idDocumento: {id_doc}")
    
    if not id_doc:
        print(f"   ❌ No se encontró ID de documento")
        print(f"   Metadata disponible: {list(data.keys())}")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print("\n4. Descargando PDF...")
try:
    ruta_pdf = os.path.join(CARPETA_EVIDENCIA, f"{id_contrato}_test.pdf")
    
    with requests.get(URL_DESCARGA.format(id_doc), headers=HEADERS, stream=True, verify=False, timeout=60) as r_down:
        print(f"   Status descarga: {r_down.status_code}")
        
        if r_down.status_code == 200:
            with open(ruta_pdf, 'wb') as f:
                for chunk in r_down.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            tamaño_mb = os.path.getsize(ruta_pdf) / (1024 * 1024)
            print(f"   ✅ PDF descargado: {tamaño_mb:.2f} MB")
            print(f"   Ruta: {ruta_pdf}")
        else:
            print(f"   ❌ Error descargando PDF")
            sys.exit(1)
            
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print("\n5. Extrayendo texto del PDF...")
try:
    reader = pypdf.PdfReader(ruta_pdf)
    num_paginas = len(reader.pages)
    print(f"   Páginas totales: {num_paginas}")
    
    texto = ""
    for i in range(min(num_paginas, 10)):  # Primeras 10 páginas
        try:
            texto += reader.pages[i].extract_text() + "\n"
        except:
            continue
    
    print(f"   ✅ Texto extraído: {len(texto)} caracteres")
    print(f"   Primeros 200 caracteres:")
    print(f"   {texto[:200]}")
    
    if len(texto) < 100:
        print(f"   ⚠️ Texto muy corto, puede ser un PDF escaneado")
    
except Exception as e:
    print(f"   ❌ Error extrayendo texto: {e}")
    sys.exit(1)

if USAR_GROQ:
    print("\n6. Analizando con GROQ...")
    try:
        GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
        
        prompt = f"""Extrae los miembros del CONSORCIO del siguiente contrato.
Responde SOLO con JSON en este formato:
[{{"ruc": "12345678901", "nombre": "EMPRESA SAC", "participacion": 50.0}}]

TEXTO:
{texto[:20000]}
"""
        
        payload = {
            "model": "llama-3.1-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 2000
        }
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        print(f"   Enviando request a Groq...")
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            texto_respuesta = resultado['choices'][0]['message']['content']
            print(f"   ✅ Respuesta recibida:")
            print(f"   {texto_respuesta}")
            
            # Parsear JSON
            texto_respuesta = texto_respuesta.replace("```json", "").replace("```", "").strip()
            datos = json.loads(texto_respuesta)
            print(f"\n   ✅ JSON parseado exitosamente:")
            print(f"   Miembros encontrados: {len(datos)}")
            for m in datos:
                print(f"      - {m.get('nombre')} (RUC: {m.get('ruc')}, Part: {m.get('participacion')}%)")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text[:500]}")
            
    except Exception as e:
        print(f"   ❌ Error con Groq: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETADO")
print("=" * 60)
