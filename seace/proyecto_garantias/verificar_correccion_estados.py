"""
Script para probar la corrección del estado_proceso
Procesa solo el primer archivo JSON para verificar que los estados se extraen correctamente
"""
import mysql.connector
import sys
import os

# Configurar encoding UTF-8
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

def verificar_estados_despues_carga():
    """Verifica los estados después de cargar datos"""
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor(dictionary=True)
    
    print("\n" + "="*80)
    print("VERIFICACIÓN DE ESTADOS DESPUÉS DE LA CORRECCIÓN")
    print("="*80 + "\n")
    
    # Contar estados únicos
    cursor.execute("""
        SELECT estado_proceso, COUNT(*) as total
        FROM Licitaciones_Cabecera
        GROUP BY estado_proceso
        ORDER BY total DESC
    """)
    
    estados = cursor.fetchall()
    
    print("Estados encontrados en la base de datos:")
    for e in estados:
        print(f"  - {e['estado_proceso']}: {e['total']:,} registros")
    
    print("\n" + "="*80)
    
    # Mostrar ejemplos de cada estado
    print("\nEjemplos de registros por estado:\n")
    for e in estados[:5]:  # Top 5 estados
        estado = e['estado_proceso']
        cursor.execute("""
            SELECT id_convocatoria, descripcion, estado_proceso
            FROM Licitaciones_Cabecera
            WHERE estado_proceso = %s
            LIMIT 3
        """, (estado,))
        
        ejemplos = cursor.fetchall()
        print(f"\n{estado} ({e['total']} registros):")
        for ej in ejemplos:
            desc = ej['descripcion'][:60] + "..." if len(ej['descripcion']) > 60 else ej['descripcion']
            print(f"  - {ej['id_convocatoria']}: {desc}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    verificar_estados_despues_carga()
