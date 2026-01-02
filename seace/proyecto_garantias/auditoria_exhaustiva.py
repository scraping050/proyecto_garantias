"""
AUDITORIA EXHAUSTIVA DE BASE DE DATOS
Verifica TODOS los aspectos de integridad de datos
"""
import mysql.connector
from config.secrets_manager import get_db_config
import json
import os
import sys
from datetime import datetime
import re

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

problemas_criticos = []
advertencias = []
info = []

print("=" * 100)
print(" AUDITORIA EXHAUSTIVA DE BASE DE DATOS")
print("=" * 100)

# ============================================================================
# 1. INTEGRIDAD DE LICITACIONES_CABECERA
# ============================================================================
print("\n" + "=" * 100)
print(" 1. AUDITORIA: Licitaciones_Cabecera")
print("=" * 100)

# 1.1 Campos NULL
print("\n1.1 Verificando campos NULL...")
campos_criticos = [
    ('id_convocatoria', True), ('ocid', True), ('departamento', True),
    ('categoria', True), ('estado_proceso', True), ('comprador', True)
]
campos_fecha = ['fecha_publicacion']

for campo, check_empty in campos_criticos:
    if check_empty:
        cursor.execute(f"SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE {campo} IS NULL OR {campo} = ''")
    else:
        cursor.execute(f"SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE {campo} IS NULL")
    count = cursor.fetchone()[0]
    if count > 0:
        problemas_criticos.append(f"Licitaciones_Cabecera.{campo}: {count} registros NULL/vacios")
        print(f"  ERROR: {campo}: {count:,} NULL/vacios")
    else:
        print(f"  OK: {campo}: 0 NULL")

# Verificar fechas (solo NULL, no empty string)
for campo in campos_fecha:
    cursor.execute(f"SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE {campo} IS NULL")
    count = cursor.fetchone()[0]
    if count > 0:
        problemas_criticos.append(f"Licitaciones_Cabecera.{campo}: {count} registros NULL")
        print(f"  ERROR: {campo}: {count:,} NULL")
    else:
        print(f"  OK: {campo}: 0 NULL")

# 1.2 Valores únicos
print("\n1.2 Verificando unicidad...")
cursor.execute("SELECT COUNT(*), COUNT(DISTINCT ocid) FROM Licitaciones_Cabecera")
total, unicos = cursor.fetchone()
if total != unicos:
    problemas_criticos.append(f"OCIDs duplicados: {total - unicos} duplicados")
    print(f"  ERROR: OCIDs duplicados: {total - unicos}")
else:
    print(f"  OK: Todos los OCIDs son unicos ({unicos:,})")

cursor.execute("SELECT COUNT(*), COUNT(DISTINCT id_convocatoria) FROM Licitaciones_Cabecera")
total, unicos = cursor.fetchone()
if total != unicos:
    problemas_criticos.append(f"id_convocatoria duplicados: {total - unicos}")
    print(f"  ERROR: id_convocatoria duplicados: {total - unicos}")
else:
    print(f"  OK: Todos los id_convocatoria son unicos ({unicos:,})")

# 1.3 Validar fechas
print("\n1.3 Verificando fechas...")
cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE fecha_publicacion < '2020-01-01' OR fecha_publicacion > '2030-01-01'")
fechas_raras = cursor.fetchone()[0]
if fechas_raras > 0:
    advertencias.append(f"Fechas fuera de rango esperado: {fechas_raras}")
    print(f"  ADVERTENCIA: {fechas_raras:,} fechas fuera de rango 2020-2030")
else:
    print(f"  OK: Todas las fechas en rango valido")

# 1.4 Validar montos
print("\n1.4 Verificando montos...")
cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE monto_estimado < 0")
montos_negativos = cursor.fetchone()[0]
if montos_negativos > 0:
    problemas_criticos.append(f"Montos negativos: {montos_negativos}")
    print(f"  ERROR: {montos_negativos:,} montos negativos")
else:
    print(f"  OK: No hay montos negativos")

cursor.execute("SELECT MIN(monto_estimado), MAX(monto_estimado), AVG(monto_estimado) FROM Licitaciones_Cabecera WHERE monto_estimado > 0")
min_m, max_m, avg_m = cursor.fetchone()
print(f"  INFO: Rango de montos: S/ {min_m:,.2f} - S/ {max_m:,.2f} (promedio: S/ {avg_m:,.2f})")

if max_m > 1000000000:  # 1 billon
    cursor.execute("SELECT id_convocatoria, nomenclatura, monto_estimado FROM Licitaciones_Cabecera WHERE monto_estimado > 1000000000 LIMIT 3")
    print(f"  ADVERTENCIA: Montos extremadamente altos detectados:")
    for row in cursor.fetchall():
        advertencias.append(f"Monto muy alto: {row[0]} - S/ {row[2]:,.2f}")
        print(f"    - {row[0]}: S/ {row[2]:,.2f}")

# 1.5 Validar categorias
print("\n1.5 Verificando categorias...")
cursor.execute("SELECT DISTINCT categoria, COUNT(*) FROM Licitaciones_Cabecera GROUP BY categoria")
categorias = cursor.fetchall()
categorias_validas = ['BIENES', 'OBRAS', 'SERVICIOS', 'CONSULTORIA']
for cat, count in categorias:
    if cat not in categorias_validas:
        advertencias.append(f"Categoria no estandar: {cat} ({count} registros)")
        print(f"  ADVERTENCIA: Categoria '{cat}': {count:,} registros (no estandar)")
    else:
        print(f"  OK: {cat}: {count:,} registros")

# ============================================================================
# 2. INTEGRIDAD DE LICITACIONES_ADJUDICACIONES
# ============================================================================
print("\n" + "=" * 100)
print(" 2. AUDITORIA: Licitaciones_Adjudicaciones")
print("=" * 100)

# 2.1 Campos NULL
print("\n2.1 Verificando campos NULL...")
campos_adj = ['id_adjudicacion', 'id_convocatoria', 'ganador_nombre']

for campo in campos_adj:
    cursor.execute(f"SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE {campo} IS NULL OR {campo} = ''")
    count = cursor.fetchone()[0]
    if count > 0:
        problemas_criticos.append(f"Licitaciones_Adjudicaciones.{campo}: {count} NULL/vacios")
        print(f"  ERROR: {campo}: {count:,} NULL/vacios")
    else:
        print(f"  OK: {campo}: 0 NULL")

# 2.2 Validar RUCs
print("\n2.2 Verificando RUCs...")
cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE ganador_ruc IS NOT NULL AND ganador_ruc != '' AND LENGTH(ganador_ruc) != 11")
rucs_invalidos = cursor.fetchone()[0]
if rucs_invalidos > 0:
    advertencias.append(f"RUCs con longitud invalida: {rucs_invalidos}")
    print(f"  ADVERTENCIA: {rucs_invalidos:,} RUCs con longitud != 11")
    
    cursor.execute("SELECT ganador_ruc, COUNT(*) FROM Licitaciones_Adjudicaciones WHERE ganador_ruc IS NOT NULL AND ganador_ruc != '' AND LENGTH(ganador_ruc) != 11 GROUP BY ganador_ruc LIMIT 5")
    print(f"  Ejemplos:")
    for ruc, count in cursor.fetchall():
        print(f"    - '{ruc}' (longitud {len(ruc)}): {count:,} registros")
else:
    print(f"  OK: Todos los RUCs tienen longitud correcta")

# 2.3 Validar montos adjudicados
print("\n2.3 Verificando montos adjudicados...")
cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE monto_adjudicado < 0")
montos_neg = cursor.fetchone()[0]
if montos_neg > 0:
    problemas_criticos.append(f"Montos adjudicados negativos: {montos_neg}")
    print(f"  ERROR: {montos_neg:,} montos negativos")
else:
    print(f"  OK: No hay montos negativos")

cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE monto_adjudicado = 0")
montos_cero = cursor.fetchone()[0]
if montos_cero > 0:
    advertencias.append(f"Montos adjudicados en cero: {montos_cero}")
    print(f"  ADVERTENCIA: {montos_cero:,} montos en cero")

# 2.4 Validar estado_item
print("\n2.4 Verificando estado_item...")
cursor.execute("SELECT DISTINCT estado_item, COUNT(*) FROM Licitaciones_Adjudicaciones GROUP BY estado_item")
estados = cursor.fetchall()
print(f"  Estados encontrados:")
for estado, count in estados:
    print(f"    - {estado}: {count:,}")
    if estado == 'DESCONOCIDO' and count > 100:
        advertencias.append(f"Muchos registros con estado DESCONOCIDO: {count}")

# 2.5 Validar entidad_financiera
print("\n2.5 Verificando entidad_financiera...")
cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE entidad_financiera IS NULL")
sin_entidad = cursor.fetchone()[0]
total_adj = cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
cursor.fetchone()
cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
total_adj = cursor.fetchone()[0]

porcentaje_sin = (sin_entidad / total_adj * 100) if total_adj > 0 else 0
print(f"  Sin entidad_financiera: {sin_entidad:,} ({porcentaje_sin:.2f}%)")

if porcentaje_sin > 70:
    advertencias.append(f"Alto porcentaje sin entidad_financiera: {porcentaje_sin:.2f}%")
    print(f"  ADVERTENCIA: Mas del 70% sin entidad_financiera (spider incompleto?)")

# ============================================================================
# 3. RELACIONES (FOREIGN KEYS)
# ============================================================================
print("\n" + "=" * 100)
print(" 3. AUDITORIA: Relaciones (Foreign Keys)")
print("=" * 100)

# 3.1 Adjudicaciones huerfanas
print("\n3.1 Verificando adjudicaciones huerfanas...")
cursor.execute("""
    SELECT COUNT(*) 
    FROM Licitaciones_Adjudicaciones a
    LEFT JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
    WHERE c.id_convocatoria IS NULL
""")
adj_huerfanas = cursor.fetchone()[0]
if adj_huerfanas > 0:
    problemas_criticos.append(f"Adjudicaciones huerfanas: {adj_huerfanas}")
    print(f"  ERROR: {adj_huerfanas:,} adjudicaciones sin cabecera")
    
    cursor.execute("""
        SELECT a.id_adjudicacion, a.id_convocatoria, a.ganador_nombre
        FROM Licitaciones_Adjudicaciones a
        LEFT JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
        WHERE c.id_convocatoria IS NULL
        LIMIT 3
    """)
    print(f"  Ejemplos:")
    for row in cursor.fetchall():
        print(f"    - {row[0]} (convocatoria: {row[1]})")
else:
    print(f"  OK: Todas las adjudicaciones tienen cabecera")

# 3.2 Contratos huerfanos
print("\n3.2 Verificando contratos huerfanos...")
cursor.execute("""
    SELECT COUNT(*) 
    FROM Contratos c
    LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_adjudicacion = a.id_adjudicacion
    WHERE a.id_adjudicacion IS NULL
""")
cont_huerfanos = cursor.fetchone()[0]
if cont_huerfanos > 0:
    problemas_criticos.append(f"Contratos huerfanos: {cont_huerfanos}")
    print(f"  ERROR: {cont_huerfanos:,} contratos sin adjudicacion")
else:
    print(f"  OK: Todos los contratos tienen adjudicacion")

# ============================================================================
# 4. VALIDACION CON JSON
# ============================================================================
print("\n" + "=" * 100)
print(" 4. AUDITORIA: Validacion con JSON fuente")
print("=" * 100)

db_folder = os.path.join(os.path.dirname(__file__), "1_database")
archivos_json = sorted([f for f in os.listdir(db_folder) if f.endswith('.json')])

print(f"\n4.1 Contando registros en JSONs...")
total_json = 0
ocids_json = set()

for archivo in archivos_json[:3]:  # Muestra de 3 archivos
    ruta = os.path.join(db_folder, archivo)
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count_archivo = 0
        for r in data.get('records', []):
            compiled = r.get('compiledRelease', {})
            tender = compiled.get('tender', {})
            
            if tender.get('procurementMethodDetails') == 'Licitacion Publica':
                count_archivo += 1
                ocid = r.get('ocid')
                if ocid:
                    ocids_json.add(ocid)
        
        total_json += count_archivo
        print(f"  {archivo}: {count_archivo:,} registros")
    except Exception as e:
        print(f"  ERROR leyendo {archivo}: {e}")

cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
total_bd = cursor.fetchone()[0]

print(f"\n  Total en muestra JSON: {total_json:,}")
print(f"  Total en BD: {total_bd:,}")

# ============================================================================
# 5. LOGICA DE NEGOCIO
# ============================================================================
print("\n" + "=" * 100)
print(" 5. AUDITORIA: Logica de Negocio")
print("=" * 100)

# 5.1 tipo_garantia vs entidad_financiera
print("\n5.1 Verificando coherencia tipo_garantia...")
cursor.execute("""
    SELECT COUNT(*) 
    FROM Licitaciones_Adjudicaciones 
    WHERE entidad_financiera = 'SIN_GARANTIA' AND tipo_garantia = 'GARANTIA_BANCARIA'
""")
incoherentes = cursor.fetchone()[0]
if incoherentes > 0:
    problemas_criticos.append(f"SIN_GARANTIA clasificado como GARANTIA_BANCARIA: {incoherentes}")
    print(f"  ERROR: {incoherentes:,} registros con SIN_GARANTIA clasificados como GARANTIA_BANCARIA")
else:
    print(f"  OK: SIN_GARANTIA clasificado correctamente como RETENCION")

# 5.2 Fechas en orden logico
print("\n5.2 Verificando orden de fechas...")
cursor.execute("""
    SELECT COUNT(*)
    FROM Licitaciones_Cabecera c
    INNER JOIN Licitaciones_Adjudicaciones a ON c.id_convocatoria = a.id_convocatoria
    WHERE a.fecha_adjudicacion < c.fecha_publicacion
""")
fechas_invertidas = cursor.fetchone()[0]
if fechas_invertidas > 0:
    advertencias.append(f"Fechas en orden illogico: {fechas_invertidas}")
    print(f"  ADVERTENCIA: {fechas_invertidas:,} adjudicaciones antes de publicacion")
else:
    print(f"  OK: Todas las fechas en orden logico")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "=" * 100)
print(" RESUMEN DE AUDITORIA")
print("=" * 100)

print(f"\nPROBLEMAS CRITICOS: {len(problemas_criticos)}")
for p in problemas_criticos:
    print(f"  - {p}")

print(f"\nADVERTENCIAS: {len(advertencias)}")
for a in advertencias:
    print(f"  - {a}")

# Calificacion
if len(problemas_criticos) == 0 and len(advertencias) == 0:
    calificacion = 10
    estado = "EXCELENTE"
elif len(problemas_criticos) == 0 and len(advertencias) <= 3:
    calificacion = 9
    estado = "MUY BUENO"
elif len(problemas_criticos) <= 2 and len(advertencias) <= 5:
    calificacion = 7
    estado = "BUENO"
else:
    calificacion = 5
    estado = "REQUIERE ATENCION"

print(f"\nCALIFICACION FINAL: {calificacion}/10 - {estado}")
print("=" * 100)

conn.close()
