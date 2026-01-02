"""
Test simple del ETL de Consorcios - Procesa solo 1 contrato
"""
import mysql.connector
import requests
import google.generativeai as genai
import os
import sys
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# --- CONFIGURACIÓN ---
if sys.platform.startswith('win'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

# Importar módulo de configuración segura
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from secrets_manager import config, get_db_config

# Carpetas
CARPETA_EVIDENCIA = os.path.join(parent_dir, "evidencia_consorcios")
if not os.path.exists(CARPETA_EVIDENCIA): 
    os.makedirs(CARPETA_EVIDENCIA)
    print(f"✅ Carpeta creada: {CARPETA_EVIDENCIA}")

# DB y API
DB_CONFIG = get_db_config()
ai_config = config.get_ai_config()

print(f"✅ Configuración cargada")
print(f"   DB: {DB_CONFIG['host']}/{DB_CONFIG['database']}")
print(f"   Gemini API Key: {'*' * 20}...{ai_config.gemini_api_key[-4:]}")

if not ai_config.gemini_api_key:
    print("❌ Error Fatal: Configura GARANTIAS_GEMINI_API_KEY en las variables de entorno")
    sys.exit(1)

genai.configure(api_key=ai_config.gemini_api_key)
print("✅ Gemini AI configurado")

# URLs
URL_METADATA = "https://prod4.seace.gob.pe:9000/api/bus/contrato/idContrato/{}"
URL_DESCARGA = "https://prod4.seace.gob.pe:9000/api/con/documentos/descargar/{}"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def obtener_un_pendiente():
    """Obtiene solo 1 contrato pendiente para prueba"""
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
        data = cursor.fetchone()
        conn.close()
        return data
    except Exception as e:
        print(f"❌ Error DB: {e}")
        return None

def main():
    print("\n" + "=" * 80)
    print(" 🧪 TEST ETL CONSORCIOS - PROCESANDO 1 CONTRATO")
    print("=" * 80)
    
    # Obtener 1 contrato
    resultado = obtener_un_pendiente()
    
    if not resultado:
        print("\n✅ No hay contratos pendientes o error en la consulta")
        return
    
    id_contrato, nombre_ganador = resultado
    
    print(f"\n📋 Contrato seleccionado:")
    print(f"   ID: {id_contrato}")
    print(f"   Ganador: {nombre_ganador}")
    
    # Intentar descargar metadata
    print(f"\n📥 Intentando obtener metadata...")
    try:
        url = URL_METADATA.format(id_contrato)
        print(f"   URL: {url}")
        
        r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
        print(f"   Status Code: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            print(f"   ✅ Metadata obtenida")
            print(f"   Claves disponibles: {list(data.keys())[:10]}...")
            
            # Buscar ID de documento
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
            else:
                print(f"   ⚠️  No se encontró ID de documento")
                print(f"   Datos disponibles: {json.dumps(data, indent=2)[:500]}...")
                return
            
            # Intentar descargar PDF
            print(f"\n📄 Intentando descargar PDF...")
            url_pdf = URL_DESCARGA.format(id_doc)
            print(f"   URL: {url_pdf}")
            
            nombre_archivo = f"{id_contrato}_test.pdf"
            ruta_pdf = os.path.join(CARPETA_EVIDENCIA, nombre_archivo)
            
            with requests.get(url_pdf, headers=HEADERS, stream=True, verify=False, timeout=60) as r_down:
                print(f"   Status Code: {r_down.status_code}")
                
                if r_down.status_code == 200:
                    with open(ruta_pdf, 'wb') as f:
                        for chunk in r_down.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    tamaño_mb = os.path.getsize(ruta_pdf) / (1024 * 1024)
                    print(f"   ✅ PDF descargado: {tamaño_mb:.2f} MB")
                    print(f"   Ruta: {ruta_pdf}")
                    
                    # Probar con Gemini AI
                    print(f"\n🤖 Enviando a Gemini AI...")
                    try:
                        archivo = genai.upload_file(ruta_pdf, mime_type='application/pdf')
                        print(f"   ✅ Archivo subido a Gemini")
                        print(f"   Estado: {archivo.state.name}")
                        
                        # Esperar procesamiento
                        wait_count = 0
                        while archivo.state.name == "PROCESSING":
                            time.sleep(2)
                            archivo = genai.get_file(archivo.name)
                            wait_count += 1
                            print(f"   ⏳ Procesando... ({wait_count * 2}s)")
                            if wait_count > 30:
                                print("   ⚠️  Timeout esperando procesamiento")
                                break
                        
                        if archivo.state.name == "ACTIVE":
                            print(f"   ✅ Archivo listo para análisis")
                            
                            # Generar contenido
                            model = genai.GenerativeModel('gemini-2.0-flash')
                            prompt = """
                            Eres un experto digitador de contratos públicos.
                            Tarea: Extrae los miembros del CONSORCIO (las empresas privadas, no la entidad pública).
                            
                            Salida JSON estricta: 
                            [{"ruc": "...", "nombre": "...", "participacion": 50.0}]
                            
                            Reglas: 
                            - RUC: Solo números. Si no hay, null.
                            - Participación: Número decimal.
                            """
                            
                            print(f"\n💭 Generando respuesta...")
                            res = model.generate_content([archivo, prompt])
                            
                            print(f"\n📝 RESPUESTA DE GEMINI:")
                            print("=" * 80)
                            print(res.text)
                            print("=" * 80)
                            
                            # Intentar parsear JSON
                            try:
                                texto = res.text.replace("```json", "").replace("```", "").strip()
                                datos = json.loads(texto)
                                print(f"\n✅ JSON parseado correctamente:")
                                print(json.dumps(datos, indent=2, ensure_ascii=False))
                                
                                print(f"\n💾 Datos listos para guardar en BD")
                                print(f"   Total miembros: {len(datos)}")
                                
                            except Exception as e:
                                print(f"\n⚠️  Error parseando JSON: {e}")
                            
                            # Limpiar
                            try:
                                genai.delete_file(archivo.name)
                                print(f"\n🗑️  Archivo eliminado de Gemini Cloud")
                            except:
                                pass
                        else:
                            print(f"   ❌ Estado del archivo: {archivo.state.name}")
                        
                    except Exception as e:
                        print(f"   ❌ Error con Gemini AI: {e}")
                    
                    # Limpiar PDF local
                    try:
                        os.remove(ruta_pdf)
                        print(f"🗑️  PDF local eliminado")
                    except:
                        pass
                    
                else:
                    print(f"   ❌ Error descargando PDF")
        else:
            print(f"   ❌ Error obteniendo metadata")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print(" ✅ TEST COMPLETADO")
    print("=" * 80)

if __name__ == "__main__":
    main()
