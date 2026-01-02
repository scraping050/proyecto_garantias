"""
Script para aplicar correcciones a entidades financieras
EJECUTAR ESTE SCRIPT PARA CORREGIR DATOS
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from secrets_manager import get_db_config
import mysql.connector

print("=" * 100)
print("🔧 APLICANDO CORRECCIONES A ENTIDADES FINANCIERAS")
print("=" * 100)
print()

# Conectar a BD
DB_CONFIG = get_db_config()
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Definir correcciones
correcciones = [
    {
        'descripcion': 'SECREX → CESCE PERÚ S.A.',
        'query': "UPDATE licitaciones_adjudicaciones SET entidad_financiera = 'CESCE PERÚ S.A. COMPAÑIA DE SEGUROS' WHERE entidad_financiera LIKE '%SECREX%'"
    },
    {
        'descripcion': 'INTERNACIONAL DEL PERU INTERBANK → INTERBANK',
        'query': "UPDATE licitaciones_adjudicaciones SET entidad_financiera = 'INTERBANK' WHERE entidad_financiera = 'INTERNACIONAL DEL PERU INTERBANK'"
    },
    {
        'descripcion': 'DE COMERCIO → BANCO DE COMERCIO',
        'query': "UPDATE licitaciones_adjudicaciones SET entidad_financiera = 'BANCO DE COMERCIO' WHERE entidad_financiera = 'DE COMERCIO'"
    }
]

print("Correcciones a aplicar:")
print()

for idx, corr in enumerate(correcciones, 1):
    print(f"{idx}. {corr['descripcion']}")

print()
print("=" * 100)
print()

try:
    for corr in correcciones:
        cursor.execute(corr['query'])
        print(f"✓ {corr['descripcion']} - {cursor.rowcount} registros actualizados")
    
    conn.commit()
    print()
    print("=" * 100)
    print("✅ TODAS LAS CORRECCIONES APLICADAS EXITOSAMENTE")
    print("=" * 100)
    print()
    
    # Verificar resultado
    cursor.execute("""
        SELECT 
            CASE 
                WHEN a.entidad_financiera LIKE '%|%' 
                THEN TRIM(SUBSTRING_INDEX(a.entidad_financiera, '|', 1))
                ELSE a.entidad_financiera
            END as entidad_principal,
            COUNT(*) as total
        FROM licitaciones_adjudicaciones a
        WHERE a.entidad_financiera IS NOT NULL 
        AND a.entidad_financiera != ''
        AND a.entidad_financiera != 'SIN_GARANTIA'
        GROUP BY entidad_principal
        ORDER BY total DESC
    """)
    
    results = cursor.fetchall()
    print(f"Total de entidades únicas después de correcciones: {len(results)}")
    print()
    
except Exception as e:
    conn.rollback()
    print(f"❌ ERROR: {e}")
    print("Cambios revertidos")

conn.close()
