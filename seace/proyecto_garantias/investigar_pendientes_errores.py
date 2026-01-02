"""
Investigación profunda de los registros pendientes y con errores
"""
import mysql.connector
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configurar encoding UTF-8 para Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

URL_API_CONTRATO = "https://prod4.seace.gob.pe:9000/api/bus/contrato/idContrato/{}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://prod4.seace.gob.pe/"
}

def main():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("="*120)
    print("INVESTIGACION PROFUNDA: Registros Pendientes y con Errores")
    print("="*120)
    
    # ========================================
    # 1. REGISTROS PENDIENTES (NULL)
    # ========================================
    print("\n" + "="*120)
    print("1. REGISTROS PENDIENTES (3 casos)")
    print("="*120)
    
    cursor.execute("""
        SELECT id_adjudicacion, id_contrato, estado_item, ganador_nombre, ganador_ruc
        FROM Licitaciones_Adjudicaciones
        WHERE (id_contrato IS NOT NULL AND id_contrato != '')
          AND (entidad_financiera IS NULL OR entidad_financiera = '')
    """)
    
    pendientes = cursor.fetchall()
    
    print(f"\nTotal pendientes: {len(pendientes)}")
    print("\nIntentando procesar ahora...")
    
    for id_adj, id_cont, estado, ganador, ruc in pendientes:
        print(f"\n{'-'*120}")
        print(f"ID Adjudicacion: {id_adj}")
        print(f"ID Contrato: {id_cont}")
        print(f"Estado: {estado}")
        print(f"Ganador: {ganador}")
        print(f"RUC: {ruc}")
        
        # Intentar consultar la API
        url = URL_API_CONTRATO.format(id_cont)
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
            
            if r.status_code == 200:
                data = r.json()
                
                # Buscar garantías
                garantias = data.get('listaGarantiaContrato') or []
                
                if garantias:
                    print(f"\n[OK] API responde correctamente")
                    print(f"Garantias encontradas: {len(garantias)}")
                    for i, g in enumerate(garantias, 1):
                        banco = g.get('entidadEmisora', 'N/A')
                        tipo = g.get('tipoGarantia', 'N/A')
                        print(f"  {i}. {banco} - {tipo}")
                else:
                    print(f"\n[OK] API responde - SIN_GARANTIA")
                    
            elif r.status_code == 404:
                print(f"\n[ERROR] Contrato no encontrado en API (404)")
            else:
                print(f"\n[ERROR] API respondio con codigo {r.status_code}")
                
        except Exception as e:
            print(f"\n[ERROR] Error de conexion: {str(e)[:100]}")
    
    # ========================================
    # 2. REGISTROS CON ERROR_API_500
    # ========================================
    print("\n\n" + "="*120)
    print("2. REGISTROS CON ERROR_API_500 (15 casos)")
    print("="*120)
    
    cursor.execute("""
        SELECT id_adjudicacion, id_contrato, estado_item, ganador_nombre, entidad_financiera
        FROM Licitaciones_Adjudicaciones
        WHERE entidad_financiera LIKE 'ERROR%'
        ORDER BY entidad_financiera
    """)
    
    errores = cursor.fetchall()
    
    print(f"\nTotal con errores: {len(errores)}")
    
    # Agrupar por tipo de error
    errores_por_tipo = {}
    for row in errores:
        tipo_error = row[4]
        if tipo_error not in errores_por_tipo:
            errores_por_tipo[tipo_error] = []
        errores_por_tipo[tipo_error].append(row)
    
    print(f"\nDistribucion de errores:")
    for tipo, casos in errores_por_tipo.items():
        print(f"  {tipo}: {len(casos)} casos")
    
    print("\n\nIntentando reprocesar los primeros 5...")
    
    for i, (id_adj, id_cont, estado, ganador, error_actual) in enumerate(errores[:5], 1):
        print(f"\n{'-'*120}")
        print(f"{i}. ID Adjudicacion: {id_adj}")
        print(f"   ID Contrato: {id_cont}")
        print(f"   Error actual: {error_actual}")
        print(f"   Ganador: {ganador[:60]}")
        
        # Intentar consultar la API
        url = URL_API_CONTRATO.format(id_cont)
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
            
            if r.status_code == 200:
                data = r.json()
                garantias = data.get('listaGarantiaContrato') or []
                
                if garantias:
                    print(f"   [OK] AHORA SI FUNCIONA - {len(garantias)} garantia(s)")
                    for g in garantias[:2]:
                        print(f"        - {g.get('entidadEmisora', 'N/A')}")
                else:
                    print(f"   [OK] AHORA SI FUNCIONA - SIN_GARANTIA")
                    
            elif r.status_code == 404:
                print(f"   [ERROR] Sigue sin existir (404)")
            elif r.status_code == 500:
                print(f"   [ERROR] Sigue dando error 500")
            else:
                print(f"   [ERROR] Codigo {r.status_code}")
                
        except Exception as e:
            print(f"   [ERROR] Error de conexion: {str(e)[:80]}")
    
    # ========================================
    # 3. RESUMEN Y RECOMENDACIONES
    # ========================================
    print("\n\n" + "="*120)
    print("3. RESUMEN Y RECOMENDACIONES")
    print("="*120)
    
    print(f"\n[PENDIENTES] {len(pendientes)} registros:")
    if len(pendientes) > 0:
        print(f"  - Ejecutar: cd 1_motor_etl && python spider_garantias.py")
        print(f"  - Tiempo estimado: menos de 1 minuto")
    
    print(f"\n[ERRORES] {len(errores)} registros con ERROR:")
    if len(errores) > 0:
        print(f"  - Opcion 1: Resetear y reprocesar")
        print(f"    UPDATE Licitaciones_Adjudicaciones SET entidad_financiera = NULL WHERE entidad_financiera LIKE 'ERROR%';")
        print(f"    cd 1_motor_etl && python spider_garantias.py")
        print(f"  - Opcion 2: Dejar como estan (solo 0.25% del total)")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*120)
    print("FIN DE INVESTIGACION")
    print("="*120)

if __name__ == "__main__":
    main()
