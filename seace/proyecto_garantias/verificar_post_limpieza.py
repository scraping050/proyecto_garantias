"""
Verificación exhaustiva de archivos esenciales del ETL
"""

import os
import sys

print("="*70)
print("🔍 VERIFICACIÓN EXHAUSTIVA POST-LIMPIEZA")
print("="*70 + "\n")

# 1. Verificar existencia de archivos
print("1️⃣ Verificando existencia de archivos esenciales...")
essential_files = {
    '1_motor_etl/etl_consorcios_openai.py': 'ETL Principal',
    '1_motor_etl/etl_consorcios_openai_retry.py': 'ETL Retry',
    'setup_auditoria_consorcios.py': 'Setup Auditoría',
    'generar_reporte_visual.py': 'Generador Reportes'
}

all_exist = True
for file, desc in essential_files.items():
    exists = os.path.exists(file)
    size = os.path.getsize(file) if exists else 0
    status = "✅" if exists and size > 1000 else "❌"
    print(f"   {status} {desc}: {size:,} bytes")
    if not exists or size < 1000:
        all_exist = False

if not all_exist:
    print("\n❌ ERROR: Faltan archivos esenciales")
    sys.exit(1)

# 2. Verificar compilación
print("\n2️⃣ Verificando compilación de archivos Python...")
import py_compile

for file in essential_files.keys():
    try:
        py_compile.compile(file, doraise=True)
        print(f"   ✅ {file}: Compila correctamente")
    except Exception as e:
        print(f"   ❌ {file}: ERROR - {e}")
        all_exist = False

# 3. Verificar funciones críticas en ETL principal
print("\n3️⃣ Verificando funciones críticas en ETL principal...")

with open('1_motor_etl/etl_consorcios_openai.py', 'r', encoding='utf-8') as f:
    content = f.read()

critical_functions = [
    'def obtener_pendientes',
    'def guardar_en_bd',
    'def registrar_en_auditoria',
    'def descargar_pdf_inteligente',
    'def extraer_texto_pdf',
    'def analizar_con_openai',
    'def validar_ruc',
    'def validar_participacion',
    'def validar_miembro'
]

for func in critical_functions:
    if func in content:
        print(f"   ✅ {func}")
    else:
        print(f"   ❌ {func} - NO ENCONTRADA")
        all_exist = False

# 4. Verificar configuración de producción
print("\n4️⃣ Verificando configuración de producción...")

if 'TEST_MODE = False' in content:
    print("   ✅ TEST_MODE = False (MODO PRODUCCIÓN)")
else:
    print("   ❌ TEST_MODE no está en False")
    all_exist = False

if 'limit = MAX_TEST_RECORDS if TEST_MODE else 10' in content:
    print("   ✅ Límite dinámico configurado")
else:
    print("   ⚠️  Límite dinámico no encontrado")

# 5. Verificar integración de auditoría
print("\n5️⃣ Verificando integración de auditoría...")

if 'registrar_en_auditoria(' in content:
    count = content.count('registrar_en_auditoria(')
    print(f"   ✅ Función de auditoría llamada {count} veces")
else:
    print("   ❌ Función de auditoría NO se llama")
    all_exist = False

# 6. Verificar tabla de auditoría
print("\n6️⃣ Verificando tabla de auditoría en BD...")

try:
    import mysql.connector
    sys.path.insert(0, 'config')
    from secrets_manager import get_db_config
    
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM ETL_Consorcios_Log")
    count = cursor.fetchone()[0]
    print(f"   ✅ Tabla ETL_Consorcios_Log existe: {count} registros")
    
    conn.close()
except Exception as e:
    print(f"   ❌ Error verificando tabla: {e}")
    all_exist = False

# RESULTADO FINAL
print("\n" + "="*70)
if all_exist:
    print("✅ VERIFICACIÓN EXITOSA - TODOS LOS COMPONENTES INTACTOS")
    print("="*70)
    print("\n🚀 El sistema está listo para ejecutar:")
    print("   cd 1_motor_etl")
    print("   python etl_consorcios_openai.py")
else:
    print("❌ VERIFICACIÓN FALLIDA - HAY PROBLEMAS")
    print("="*70)
    sys.exit(1)
