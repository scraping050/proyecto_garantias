# Script de prueba simplificado para procesar 1 consorcio con debug detallado
import mysql.connector
import requests
import google.generativeai as genai
import os
import sys
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pypdf

print("=" * 60)
print("INICIANDO PROCESAMIENTO DE CONSORCIOS CON IA - MODO DEBUG")
print("=" * 60)

# Configuración
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

# Importar configuración
sys.path.insert(0, os.path.join(parent_dir, 'config'))
from secrets_manager import config, get_db_config

print("\n1. Configurando conexiones...")
DB_CONFIG = get_db_config()
ai_config = config.get_ai_config()
genai.configure(api_key=ai_config.gemini_api_key)
print("   OK - Configuracion cargada")

# URLs
URL_METADATA = "https://prod4.seace.gob.pe:9000/api/bus/contrato/idContrato/{}"
URL_DESCARGA = "https://prod4.seace.gob.pe:9000/api/con/documentos/descargar/{}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

CARPETA_EVIDENCIA = os.path.join(parent_dir, "evidencia_consorcios")
if not os.path.exists(CARPETA_EVIDENCIA):
    os.makedirs(CARPETA_EVIDENCIA)
    print(f"   OK - Carpeta creada: {CARPETA_EVIDENCIA}")

print("\n2. Conectando a base de datos...")
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("   OK - Conexion exitosa")
    
    # Buscar 1 consorcio pendiente
    print("\n3. Buscando consorcio pendiente...")
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
    
    if not resultado:
        print("   ERROR - No se encontraron consorcios pendientes")
        sys.exit(1)
    
    id_contrato, nombre_ganador = resultado
    print(f"   OK - Encontrado: {id_contrato}")
    print(f"        Nombre: {nombre_ganador[:60]}...")
    
    # Obtener metadata del contrato
    print(f"\n4. Descargando metadata del contrato {id_contrato}...")
    url_meta = URL_METADATA.format(id_contrato)
    print(f"   URL: {url_meta}")
    
    r = requests.get(url_meta, headers=HEADERS, verify=False, timeout=10)
    print(f"   Status: {r.status_code}")
    
    if r.status_code != 200:
        print(f"   ERROR - No se pudo obtener metadata")
        sys.exit(1)
    
    data = r.json()
    print("   OK - Metadata descargada")
    
    # Buscar ID del documento
    print("\n5. Buscando documento PDF...")
    id_doc = None
    if data.get("idDocumentoConsorcio"):
        id_doc = data.get("idDocumentoConsorcio")
        print(f"   OK - Encontrado idDocumentoConsorcio: {id_doc}")
    elif data.get("idDocumento2"):
        id_doc = data.get("idDocumento2")
        print(f"   OK - Encontrado idDocumento2: {id_doc}")
    elif data.get("idDocumento"):
        id_doc = data.get("idDocumento")
        print(f"   OK - Encontrado idDocumento: {id_doc}")
    
    if not id_doc:
        print("   ADVERTENCIA - No se encontro ID de documento")
        print("   Saltando este contrato...")
        sys.exit(0)
    
    # Descargar PDF
    print(f"\n6. Descargando PDF (ID: {id_doc})...")
    nombre_archivo = f"{id_contrato}_test.pdf"
    ruta_pdf = os.path.join(CARPETA_EVIDENCIA, nombre_archivo)
    
    url_pdf = URL_DESCARGA.format(id_doc)
    print(f"   URL: {url_pdf}")
    
    with requests.get(url_pdf, headers=HEADERS, stream=True, verify=False, timeout=60) as r_down:
        print(f"   Status: {r_down.status_code}")
        if r_down.status_code == 200:
            with open(ruta_pdf, 'wb') as f:
                for chunk in r_down.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            tamano_mb = os.path.getsize(ruta_pdf) / (1024 * 1024)
            print(f"   OK - PDF descargado: {tamano_mb:.2f} MB")
        else:
            print(f"   ERROR - No se pudo descargar PDF")
            sys.exit(1)
    
    # Analizar con IA
    print("\n7. Analizando PDF con Google Gemini AI...")
    print("   Subiendo archivo a Gemini...")
    
    archivo = genai.upload_file(ruta_pdf, mime_type='application/pdf')
    print(f"   OK - Archivo subido: {archivo.name}")
    
    # Esperar procesamiento
    print("   Esperando procesamiento...")
    wait_count = 0
    while archivo.state.name == "PROCESSING":
        time.sleep(2)
        archivo = genai.get_file(archivo.name)
        wait_count += 1
        print(f"   ... procesando ({wait_count * 2}s)")
        if wait_count > 30:
            print("   ERROR - Timeout esperando procesamiento")
            sys.exit(1)
    
    if archivo.state.name == "FAILED":
        print("   ERROR - Gemini marco el archivo como FAILED")
        sys.exit(1)
    
    print("   OK - Archivo procesado por Gemini")
    
    # Generar respuesta
    print("\n8. Generando analisis con IA...")
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
    
    res = model.generate_content([archivo, prompt])
    print("   OK - Respuesta generada")
    
    # Limpiar respuesta
    texto = res.text.replace("```json", "").replace("```", "").strip()
    print(f"\n9. Respuesta de IA:")
    print(texto[:500])
    
    # Parsear JSON
    print("\n10. Parseando JSON...")
    try:
        miembros = json.loads(texto)
        print(f"   OK - {len(miembros)} miembros encontrados")
        
        for i, m in enumerate(miembros, 1):
            print(f"\n   Miembro {i}:")
            print(f"     RUC: {m.get('ruc', 'N/A')}")
            print(f"     Nombre: {m.get('nombre', 'N/A')[:50]}")
            print(f"     Participacion: {m.get('participacion', 0)}%")
    except json.JSONDecodeError as e:
        print(f"   ERROR - No se pudo parsear JSON: {e}")
        sys.exit(1)
    
    # Guardar en BD
    print("\n11. Guardando en base de datos...")
    sql_insert = """
        INSERT INTO Detalle_Consorcios (id_contrato, ruc_miembro, nombre_miembro, porcentaje_participacion)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE fecha_registro=NOW()
    """
    
    datos = []
    for m in miembros:
        ruc = m.get('ruc')
        if not ruc:
            ruc = "S/N"
        ruc = str(ruc).replace("RUC", "").replace(":", "").strip()[:20]
        
        nombre = str(m.get('nombre', 'DESCONOCIDO')).upper().strip()[:500]
        part = m.get('participacion')
        if part is None:
            part = 0.0
        
        datos.append((id_contrato, ruc, nombre, part))
    
    cursor.executemany(sql_insert, datos)
    conn.commit()
    print(f"   OK - {len(datos)} miembros guardados en BD")
    
    # Limpiar
    print("\n12. Limpiando archivos temporales...")
    try:
        genai.delete_file(archivo.name)
        print("   OK - Archivo eliminado de Gemini")
    except:
        pass
    
    try:
        os.remove(ruta_pdf)
        print("   OK - PDF local eliminado")
    except:
        pass
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    
except Exception as e:
    print(f"\nERROR FATAL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
