"""
Script de verificación completa del sistema ETL antes de producción
"""

import mysql.connector
import sys
import os

# Agregar path de config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from secrets_manager import get_db_config

print("="*70)
print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA ETL")
print("="*70 + "\n")

# 1. Verificar conexión a BD
print("1️⃣ Verificando conexión a base de datos...")
try:
    DB_CONFIG = get_db_config()
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("   ✅ Conexión exitosa")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    sys.exit(1)

# 2. Verificar tabla Licitaciones_Adjudicaciones
print("\n2️⃣ Verificando tabla Licitaciones_Adjudicaciones...")
try:
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    total = cursor.fetchone()[0]
    print(f"   ✅ Tabla existe: {total:,} registros totales")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    sys.exit(1)

# 3. Verificar contratos con CONSORCIO
print("\n3️⃣ Verificando contratos con CONSORCIO...")
try:
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones 
        WHERE ganador_nombre LIKE '%CONSORCIO%'
    """)
    total_consorcios = cursor.fetchone()[0]
    print(f"   ✅ Contratos con CONSORCIO: {total_consorcios:,}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    sys.exit(1)

# 4. Verificar tabla Detalle_Consorcios
print("\n4️⃣ Verificando tabla Detalle_Consorcios...")
try:
    cursor.execute("SELECT COUNT(*) FROM Detalle_Consorcios")
    total_procesados = cursor.fetchone()[0]
    print(f"   ✅ Tabla existe: {total_procesados:,} miembros guardados")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    sys.exit(1)

# 5. Verificar contratos ya procesados
print("\n5️⃣ Verificando contratos ya procesados...")
try:
    cursor.execute("""
        SELECT COUNT(DISTINCT id_contrato) 
        FROM Detalle_Consorcios
    """)
    contratos_procesados = cursor.fetchone()[0]
    print(f"   ✅ Contratos ya procesados: {contratos_procesados:,}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    sys.exit(1)

# 6. Calcular contratos pendientes
print("\n6️⃣ Calculando contratos pendientes...")
try:
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones a
        LEFT JOIN Detalle_Consorcios d ON a.id_contrato = d.id_contrato
        WHERE a.ganador_nombre LIKE '%CONSORCIO%' 
          AND d.id_contrato IS NULL
          AND a.id_contrato IS NOT NULL 
          AND a.id_contrato != ''
    """)
    pendientes = cursor.fetchone()[0]
    print(f"   ✅ Contratos pendientes: {pendientes:,}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    sys.exit(1)

# 7. Verificar tabla de auditoría
print("\n7️⃣ Verificando tabla ETL_Consorcios_Log...")
try:
    cursor.execute("SELECT COUNT(*) FROM ETL_Consorcios_Log")
    total_log = cursor.fetchone()[0]
    print(f"   ✅ Tabla existe: {total_log:,} registros de auditoría")
except Exception as e:
    print(f"   ⚠️  Tabla NO existe - Ejecuta: python setup_auditoria_consorcios.py")

# 8. Verificar modo del ETL
print("\n8️⃣ Verificando configuración del ETL...")
try:
    with open('1_motor_etl/etl_consorcios_openai.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'TEST_MODE = False' in content:
            print("   ✅ TEST_MODE = False (MODO PRODUCCIÓN)")
        elif 'TEST_MODE = True' in content:
            print("   ❌ TEST_MODE = True (MODO PRUEBA) - CAMBIAR A False")
            sys.exit(1)
        else:
            print("   ⚠️  No se pudo verificar TEST_MODE")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# 9. Verificar API Key de OpenAI
print("\n9️⃣ Verificando API Key de OpenAI...")
try:
    from config.secrets_manager import config
    ai_config = config.get_ai_config()
    if hasattr(ai_config, 'openai_api_key') and ai_config.openai_api_key:
        print(f"   ✅ API Key configurada (termina en: ...{ai_config.openai_api_key[-4:]})")
    else:
        print("   ❌ API Key NO configurada")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    sys.exit(1)

# 10. Verificar OCR
print("\n🔟 Verificando OCR (Tesseract)...")
try:
    import pytesseract
    import pdf2image
    print("   ✅ Tesseract y pdf2image instalados")
except ImportError as e:
    print(f"   ⚠️  OCR no disponible: {e}")

conn.close()

# RESUMEN FINAL
print("\n" + "="*70)
print("📊 RESUMEN DE VERIFICACIÓN")
print("="*70)
print(f"Total contratos con CONSORCIO: {total_consorcios:,}")
print(f"Contratos ya procesados: {contratos_procesados:,}")
print(f"Contratos pendientes: {pendientes:,}")
print(f"\n💰 ESTIMACIÓN:")
print(f"   Costo primera pasada: ${pendientes * 0.0154:.2f} USD")
print(f"   Costo segunda pasada: ${pendientes * 0.02 * 0.0308:.2f} USD")
print(f"   Costo total estimado: ${pendientes * 0.0154 + pendientes * 0.02 * 0.0308:.2f} USD")
print(f"\n⏱️  Tiempo estimado: {pendientes * 30 / 3600:.1f} horas")
print("="*70)

if pendientes > 0:
    print("\n✅ SISTEMA LISTO PARA EJECUTAR")
    print("\nPróximos pasos:")
    print("1. python setup_auditoria_consorcios.py  (si no se ha ejecutado)")
    print("2. cd 1_motor_etl")
    print("3. python etl_consorcios_openai.py")
else:
    print("\n✅ NO HAY CONTRATOS PENDIENTES")
    print("Todos los consorcios ya han sido procesados")

print()
