"""
Script para corregir datos erróneos en entidades financieras
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from secrets_manager import get_db_config
import mysql.connector

print("=" * 100)
print("🔧 CORRECCIÓN DE DATOS ERRÓNEOS EN ENTIDADES FINANCIERAS")
print("=" * 100)
print()

# Conectar a BD
DB_CONFIG = get_db_config()
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Definir correcciones
correcciones = [
    {
        'nombre': 'SECREX → CESCE',
        'condicion': "entidad_financiera LIKE '%SECREX%'",
        'nuevo_valor': 'CESCE PERÚ S.A. COMPAÑIA DE SEGUROS'
    },
    {
        'nombre': 'INTERNACIONAL DEL PERU INTERBANK → INTERBANK',
        'condicion': "entidad_financiera = 'INTERNACIONAL DEL PERU INTERBANK'",
        'nuevo_valor': 'INTERBANK'
    },
    {
        'nombre': 'ERROR_API_500 → Investigar manualmente',
        'condicion': "entidad_financiera = 'ERROR_API_500'",
        'nuevo_valor': None  # Requiere investigación manual
    },
    {
        'nombre': 'FINANCIERO → Investigar manualmente',
        'condicion': "entidad_financiera = 'FINANCIERO'",
        'nuevo_valor': None  # Requiere investigación manual
    },
    {
        'nombre': 'DE COMERCIO → BANCO DE COMERCIO',
        'condicion': "entidad_financiera = 'DE COMERCIO'",
        'nuevo_valor': 'BANCO DE COMERCIO'
    }
]

print("Correcciones a aplicar:")
print()

registros_afectados = 0

for corr in correcciones:
    # Contar registros afectados
    cursor.execute(f"SELECT COUNT(*), COALESCE(SUM(monto_adjudicado), 0) FROM licitaciones_adjudicaciones WHERE {corr['condicion']}")
    count, monto = cursor.fetchone()
    
    print(f"✓ {corr['nombre']}")
    print(f"  Registros afectados: {count}")
    print(f"  Monto total: S/ {float(monto):,.2f}")
    
    if corr['nuevo_valor']:
        print(f"  Acción: Actualizar a '{corr['nuevo_valor']}'")
        registros_afectados += count
    else:
        print(f"  Acción: Requiere investigación manual")
    
    print()

print("=" * 100)
print(f"Total registros a corregir automáticamente: {registros_afectados}")
print("=" * 100)
print()

# Preguntar confirmación
respuesta = input("¿Deseas aplicar las correcciones automáticas? (si/no): ")

if respuesta.lower() in ['si', 's', 'yes', 'y']:
    print()
    print("Aplicando correcciones...")
    print()
    
    for corr in correcciones:
        if corr['nuevo_valor']:
            query = f"UPDATE licitaciones_adjudicaciones SET entidad_financiera = %s WHERE {corr['condicion']}"
            cursor.execute(query, (corr['nuevo_valor'],))
            print(f"✓ {corr['nombre']} - {cursor.rowcount} registros actualizados")
    
    conn.commit()
    print()
    print("✅ Correcciones aplicadas exitosamente")
else:
    print()
    print("❌ Correcciones canceladas")

conn.close()
