"""
Procesamiento Manual de los 3 Registros Pendientes
Consulta la API de SEACE y actualiza la BD directamente
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://prod4.seace.gob.pe/"
}

# Los 3 registros pendientes
PENDIENTES = [
    ("1136959-20602007970", "2365490", "LC BIOCORP S.A.C."),
    ("1148638-20602007970", "2366181", "LC BIOCORP S.A.C."),
    ("1164267-1746873", "2367837", "CONSORCIO EL LIMON")
]

def procesar_contrato(id_contrato):
    """Consulta la API y extrae la entidad financiera"""
    url = URL_API_CONTRATO.format(id_contrato)
    
    try:
        print(f"\n  Consultando API: {url}")
        r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            
            # Extraer garantías
            garantias = data.get('listaGarantiaContrato') or []
            
            if garantias:
                print(f"  ✅ Encontradas {len(garantias)} garantía(s)")
                
                emisores = set()
                for g in garantias:
                    banco = g.get('entidadEmisora')
                    tipo = g.get('tipoGarantia', 'N/A')
                    print(f"     - {banco or 'N/A'} ({tipo})")
                    
                    if banco:
                        banco_limpio = banco.strip().upper().replace("BANCO", "").strip()
                        if banco_limpio:  # Solo agregar si no está vacío
                            emisores.add(banco_limpio)
                
                if emisores:
                    resultado = " | ".join(sorted(emisores))
                    print(f"  📝 Resultado: {resultado}")
                    return resultado
                else:
                    print(f"  📝 Resultado: SIN_GARANTIA (solo retención)")
                    return "SIN_GARANTIA"
            else:
                print(f"  📝 Resultado: SIN_GARANTIA (sin garantías)")
                return "SIN_GARANTIA"
                
        elif r.status_code == 404:
            print(f"  ❌ Contrato no encontrado (404)")
            return "CONTRATO_NO_ENCONTRADO_API"
        else:
            print(f"  ❌ Error API: {r.status_code}")
            return f"ERROR_API_{r.status_code}"
            
    except Exception as e:
        print(f"  ❌ Error de conexión: {str(e)[:100]}")
        return "ERROR_CONEXION"

def main():
    print("="*120)
    print("PROCESAMIENTO MANUAL DE REGISTROS PENDIENTES")
    print("="*120)
    
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    resultados = []
    
    for id_adj, id_contrato, ganador in PENDIENTES:
        print(f"\n{'='*120}")
        print(f"Procesando: {id_adj}")
        print(f"Contrato: {id_contrato}")
        print(f"Ganador: {ganador}")
        print(f"{'-'*120}")
        
        entidad = procesar_contrato(id_contrato)
        resultados.append((entidad, id_adj))
        
        print(f"\n  ✅ Procesado: {entidad}")
    
    # Guardar en la base de datos
    print(f"\n\n{'='*120}")
    print("GUARDANDO RESULTADOS EN BASE DE DATOS")
    print(f"{'='*120}")
    
    sql = "UPDATE Licitaciones_Adjudicaciones SET entidad_financiera = %s WHERE id_adjudicacion = %s"
    
    try:
        cursor.executemany(sql, resultados)
        conn.commit()
        print(f"\n✅ {len(resultados)} registros actualizados correctamente")
        
        # Verificar
        print(f"\n{'='*120}")
        print("VERIFICACIÓN")
        print(f"{'='*120}")
        
        for entidad, id_adj in resultados:
            cursor.execute(
                "SELECT entidad_financiera FROM Licitaciones_Adjudicaciones WHERE id_adjudicacion = %s",
                (id_adj,)
            )
            valor_bd = cursor.fetchone()[0]
            
            if valor_bd == entidad:
                print(f"✅ {id_adj}: {valor_bd}")
            else:
                print(f"❌ {id_adj}: Esperado '{entidad}', encontrado '{valor_bd}'")
        
        # Verificar pendientes restantes
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Licitaciones_Adjudicaciones
            WHERE (id_contrato IS NOT NULL AND id_contrato != '')
              AND (entidad_financiera IS NULL OR entidad_financiera = '')
        """)
        pendientes_restantes = cursor.fetchone()[0]
        
        print(f"\n{'='*120}")
        print("RESULTADO FINAL")
        print(f"{'='*120}")
        print(f"Registros pendientes restantes: {pendientes_restantes}")
        
        if pendientes_restantes == 0:
            print(f"\n🎉 ¡ÉXITO! 100% de registros procesables completados")
        else:
            print(f"\n⚠️  Aún quedan {pendientes_restantes} registros pendientes")
            
    except Exception as e:
        print(f"\n❌ Error al guardar: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    
    print(f"\n{'='*120}")
    print("FIN DEL PROCESAMIENTO MANUAL")
    print(f"{'='*120}")

if __name__ == "__main__":
    main()
