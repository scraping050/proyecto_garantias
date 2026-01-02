"""
Auditoría Completa de cargador.py y spider_garantias.py
Verifica que estén cargando el 100% de los datos correctamente
"""
import mysql.connector
from config.secrets_manager import get_db_config
import json
import os
import sys

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def main():
    print("=" * 100)
    print(" 🔍 AUDITORÍA COMPLETA: CARGADOR.PY Y SPIDER_GARANTIAS.PY")
    print("=" * 100)
    
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    # ===================================================================
    # PARTE 1: AUDITORÍA DE CARGADOR.PY
    # ===================================================================
    
    print("\n" + "=" * 100)
    print(" 📦 PARTE 1: AUDITORÍA DE CARGADOR.PY")
    print("=" * 100)
    
    # 1.1 Verificar que todos los JSONs se procesaron
    print("\n🔍 1.1 Verificación de Archivos JSON Procesados")
    print("-" * 100)
    
    db_folder = os.path.join(os.path.dirname(__file__), "1_database")
    archivos_json = sorted([f for f in os.listdir(db_folder) if f.endswith('.json')])
    
    cursor.execute("SELECT nombre_archivo, estado, registros_procesados FROM control_cargas")
    archivos_procesados = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
    
    print(f"  Total archivos JSON en carpeta: {len(archivos_json)}")
    print(f"  Total archivos en control_cargas: {len(archivos_procesados)}")
    
    no_procesados = []
    for archivo in archivos_json:
        if archivo not in archivos_procesados:
            no_procesados.append(archivo)
            print(f"  ❌ NO PROCESADO: {archivo}")
        elif archivos_procesados[archivo][0] != 'EXITO':
            print(f"  ⚠️  ESTADO ANORMAL: {archivo} - {archivos_procesados[archivo][0]}")
    
    if not no_procesados:
        print(f"  ✅ Todos los archivos JSON han sido procesados")
    
    # 1.2 Contar registros en JSONs vs BD
    print("\n🔍 1.2 Comparación: Registros en JSONs vs Base de Datos")
    print("-" * 100)
    
    total_json = 0
    ocids_json = set()
    
    print("  Contando registros en JSONs...")
    for archivo in archivos_json:
        ruta = os.path.join(db_folder, archivo)
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            records = data.get('records', [])
            for r in records:
                compiled = r.get('compiledRelease', {})
                tender = compiled.get('tender', {})
                
                # Filtro: Solo Licitación Pública
                if tender.get('procurementMethodDetails') == 'Licitación Pública':
                    total_json += 1
                    ocid = r.get('ocid')
                    if ocid:
                        ocids_json.add(ocid)
        except Exception as e:
            print(f"  ⚠️  Error leyendo {archivo}: {e}")
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
    total_bd = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT ocid) FROM Licitaciones_Cabecera")
    ocids_bd_count = cursor.fetchone()[0]
    
    print(f"\n  📊 Resultados:")
    print(f"     Total en JSONs (Licitación Pública): {total_json:,}")
    print(f"     Total en BD (Licitaciones_Cabecera): {total_bd:,}")
    print(f"     OCIDs únicos en JSONs: {len(ocids_json):,}")
    print(f"     OCIDs únicos en BD: {ocids_bd_count:,}")
    print(f"     Diferencia: {total_bd - total_json:+,}")
    
    if total_bd == total_json:
        print(f"  ✅ PERFECTO: 100% de coincidencia")
    elif abs(total_bd - total_json) < 10:
        print(f"  ⚠️  Diferencia menor (posiblemente duplicados legítimos)")
    else:
        print(f"  ❌ ATENCIÓN: Diferencia significativa")
    
    # 1.3 Verificar integridad de datos en Cabecera
    print("\n🔍 1.3 Integridad de Datos en Licitaciones_Cabecera")
    print("-" * 100)
    
    checks = [
        ("id_convocatoria NULL", "SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE id_convocatoria IS NULL OR id_convocatoria = ''"),
        ("ocid NULL", "SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE ocid IS NULL OR ocid = ''"),
        ("fecha_publicacion NULL", "SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE fecha_publicacion IS NULL"),
        ("departamento NULL", "SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE departamento IS NULL OR departamento = ''"),
        ("categoria NULL", "SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE categoria IS NULL OR categoria = ''"),
        ("estado_proceso NULL", "SELECT COUNT(*) FROM Licitaciones_Cabecera WHERE estado_proceso IS NULL OR estado_proceso = ''"),
    ]
    
    problemas_cabecera = []
    for nombre, query in checks:
        cursor.execute(query)
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"  ❌ {nombre}: {count:,} registros")
            problemas_cabecera.append(nombre)
        else:
            print(f"  ✅ {nombre}: 0 registros (perfecto)")
    
    if not problemas_cabecera:
        print(f"\n  ✅ PERFECTO: Todos los campos críticos están completos")
    
    # 1.4 Verificar Adjudicaciones
    print("\n🔍 1.4 Integridad de Datos en Licitaciones_Adjudicaciones")
    print("-" * 100)
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    total_adj = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
    total_lic = cursor.fetchone()[0]
    
    print(f"  Total licitaciones: {total_lic:,}")
    print(f"  Total adjudicaciones: {total_adj:,}")
    print(f"  Promedio adj/licitación: {total_adj/total_lic:.2f}")
    
    checks_adj = [
        ("id_adjudicacion NULL", "SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE id_adjudicacion IS NULL OR id_adjudicacion = ''"),
        ("id_convocatoria NULL", "SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE id_convocatoria IS NULL OR id_convocatoria = ''"),
        ("ganador_nombre NULL", "SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE ganador_nombre IS NULL OR ganador_nombre = ''"),
        ("monto_adjudicado = 0", "SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE monto_adjudicado = 0 OR monto_adjudicado IS NULL"),
    ]
    
    for nombre, query in checks_adj:
        cursor.execute(query)
        count = cursor.fetchone()[0]
        porcentaje = (count / total_adj * 100) if total_adj > 0 else 0
        if count > 0:
            print(f"  ⚠️  {nombre}: {count:,} ({porcentaje:.2f}%)")
        else:
            print(f"  ✅ {nombre}: 0 registros")
    
    # 1.5 Verificar Contratos
    print("\n🔍 1.5 Integridad de Datos en Contratos")
    print("-" * 100)
    
    cursor.execute("SELECT COUNT(*) FROM Contratos")
    total_contratos = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(DISTINCT id_contrato) 
        FROM Licitaciones_Adjudicaciones 
        WHERE id_contrato IS NOT NULL AND id_contrato != ''
    """)
    contratos_en_adj = cursor.fetchone()[0]
    
    print(f"  Total contratos en tabla Contratos: {total_contratos:,}")
    print(f"  Contratos únicos en Adjudicaciones: {contratos_en_adj:,}")
    print(f"  Diferencia: {total_contratos - contratos_en_adj:+,}")
    
    if total_contratos >= contratos_en_adj:
        print(f"  ✅ Tabla Contratos tiene todos los contratos referenciados")
    else:
        print(f"  ❌ PROBLEMA: Faltan {contratos_en_adj - total_contratos} contratos en la tabla")
    
    # 1.6 Verificar relaciones FK
    print("\n🔍 1.6 Verificación de Relaciones (Foreign Keys)")
    print("-" * 100)
    
    # Adjudicaciones huérfanas (sin cabecera)
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Adjudicaciones a
        LEFT JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
        WHERE c.id_convocatoria IS NULL
    """)
    adj_huerfanas = cursor.fetchone()[0]
    
    if adj_huerfanas > 0:
        print(f"  ❌ Adjudicaciones huérfanas (sin cabecera): {adj_huerfanas:,}")
    else:
        print(f"  ✅ Todas las adjudicaciones tienen cabecera válida")
    
    # Contratos huérfanos
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Contratos c
        LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_adjudicacion = a.id_adjudicacion
        WHERE a.id_adjudicacion IS NULL
    """)
    contratos_huerfanos = cursor.fetchone()[0]
    
    if contratos_huerfanos > 0:
        print(f"  ❌ Contratos huérfanos (sin adjudicación): {contratos_huerfanos:,}")
    else:
        print(f"  ✅ Todos los contratos tienen adjudicación válida")
    
    # ===================================================================
    # PARTE 2: AUDITORÍA DE SPIDER_GARANTIAS.PY
    # ===================================================================
    
    print("\n" + "=" * 100)
    print(" 🕷️  PARTE 2: AUDITORÍA DE SPIDER_GARANTIAS.PY")
    print("=" * 100)
    
    # 2.1 Verificar campo entidad_financiera
    print("\n🔍 2.1 Verificación de Campo entidad_financiera")
    print("-" * 100)
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE entidad_financiera IS NULL")
    sin_procesar = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE entidad_financiera IS NOT NULL")
    procesados = cursor.fetchone()[0]
    
    total_adj = sin_procesar + procesados
    porcentaje_procesado = (procesados / total_adj * 100) if total_adj > 0 else 0
    
    print(f"  Total adjudicaciones: {total_adj:,}")
    print(f"  Con entidad_financiera: {procesados:,} ({porcentaje_procesado:.2f}%)")
    print(f"  Sin entidad_financiera: {sin_procesar:,} ({100-porcentaje_procesado:.2f}%)")
    
    if sin_procesar == 0:
        print(f"  ✅ PERFECTO: 100% de adjudicaciones procesadas por spider")
    elif sin_procesar < 100:
        print(f"  ⚠️  Casi completo, faltan {sin_procesar} registros")
    else:
        print(f"  ❌ ATENCIÓN: Spider no ha procesado {sin_procesar} registros")
    
    # 2.2 Distribución de valores en entidad_financiera
    print("\n🔍 2.2 Distribución de Valores en entidad_financiera")
    print("-" * 100)
    
    cursor.execute("""
        SELECT entidad_financiera, COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        WHERE entidad_financiera IS NOT NULL
        GROUP BY entidad_financiera
        ORDER BY total DESC
        LIMIT 10
    """)
    
    print(f"  {'Valor':<40} {'Cantidad':>12} {'%':>8}")
    print("  " + "-" * 65)
    
    for valor, cantidad in cursor.fetchall():
        porcentaje = (cantidad / procesados * 100) if procesados > 0 else 0
        valor_display = valor[:37] + "..." if len(valor) > 40 else valor
        print(f"  {valor_display:<40} {cantidad:>12,} {porcentaje:>7.2f}%")
    
    # 2.3 Verificar tipo_garantia (columna generada)
    print("\n🔍 2.3 Verificación de tipo_garantia (Columna Generada)")
    print("-" * 100)
    
    cursor.execute("""
        SELECT tipo_garantia, COUNT(*) as total
        FROM Licitaciones_Adjudicaciones
        GROUP BY tipo_garantia
        ORDER BY total DESC
    """)
    
    print(f"  {'Tipo Garantía':<30} {'Cantidad':>12} {'%':>8}")
    print("  " + "-" * 55)
    
    for tipo, cantidad in cursor.fetchall():
        porcentaje = (cantidad / total_adj * 100) if total_adj > 0 else 0
        print(f"  {tipo:<30} {cantidad:>12,} {porcentaje:>7.2f}%")
    
    # 2.4 Verificar consorcios procesados
    print("\n🔍 2.4 Verificación de Consorcios (Procesamiento Parcial)")
    print("-" * 100)
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE ganador_nombre LIKE '%CONSORCIO%'")
    total_consorcios = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Detalle_Consorcios")
    consorcios_procesados = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT id_contrato) FROM Detalle_Consorcios")
    contratos_con_detalle = cursor.fetchone()[0]
    
    print(f"  Adjudicaciones con 'CONSORCIO': {total_consorcios:,}")
    print(f"  Miembros en Detalle_Consorcios: {consorcios_procesados:,}")
    print(f"  Contratos con detalle: {contratos_con_detalle:,}")
    
    if consorcios_procesados == 0:
        print(f"  ⚠️  PENDIENTE: Spider descarga PDFs pero no procesa con IA")
        print(f"     Ejecutar: python 1_motor_etl/etl_consorcios_ai.py")
    else:
        porcentaje = (contratos_con_detalle / total_consorcios * 100) if total_consorcios > 0 else 0
        print(f"  ✅ {porcentaje:.2f}% de consorcios procesados")
    
    # ===================================================================
    # PARTE 3: RESUMEN FINAL
    # ===================================================================
    
    print("\n" + "=" * 100)
    print(" 📊 PARTE 3: RESUMEN FINAL Y RECOMENDACIONES")
    print("=" * 100)
    
    problemas = []
    advertencias = []
    
    # Evaluar problemas
    if no_procesados:
        problemas.append(f"❌ {len(no_procesados)} archivos JSON sin procesar")
    
    if abs(total_bd - total_json) > 10:
        problemas.append(f"❌ Diferencia significativa: BD tiene {total_bd - total_json:+,} registros vs JSONs")
    
    if problemas_cabecera:
        problemas.append(f"❌ Campos NULL en Cabecera: {', '.join(problemas_cabecera)}")
    
    if adj_huerfanas > 0:
        problemas.append(f"❌ {adj_huerfanas} adjudicaciones huérfanas")
    
    if contratos_huerfanos > 0:
        problemas.append(f"❌ {contratos_huerfanos} contratos huérfanos")
    
    if sin_procesar > 100:
        problemas.append(f"❌ {sin_procesar} adjudicaciones sin procesar por spider")
    
    # Evaluar advertencias
    if abs(total_bd - total_json) <= 10 and abs(total_bd - total_json) > 0:
        advertencias.append(f"⚠️  Diferencia menor: {total_bd - total_json:+,} registros")
    
    if sin_procesar > 0 and sin_procesar <= 100:
        advertencias.append(f"⚠️  {sin_procesar} adjudicaciones pendientes de spider")
    
    if consorcios_procesados == 0:
        advertencias.append(f"⚠️  Tabla Detalle_Consorcios vacía (requiere ETL de IA)")
    
    print("\n📋 PROBLEMAS CRÍTICOS:")
    if problemas:
        for p in problemas:
            print(f"  {p}")
    else:
        print(f"  ✅ No se encontraron problemas críticos")
    
    print("\n⚠️  ADVERTENCIAS:")
    if advertencias:
        for a in advertencias:
            print(f"  {a}")
    else:
        print(f"  ✅ No hay advertencias")
    
    print("\n🎯 CALIFICACIÓN GENERAL:")
    if not problemas and not advertencias:
        print(f"  ✅ EXCELENTE: 100% de datos cargados correctamente")
        print(f"  📊 Calificación: 10/10")
    elif not problemas and advertencias:
        print(f"  ✅ MUY BUENO: Datos principales al 100%, pendientes menores")
        print(f"  📊 Calificación: 9/10")
    elif len(problemas) <= 2:
        print(f"  ⚠️  BUENO: Algunos problemas menores detectados")
        print(f"  📊 Calificación: 7/10")
    else:
        print(f"  ❌ REQUIERE ATENCIÓN: Múltiples problemas detectados")
        print(f"  📊 Calificación: 5/10")
    
    print("\n" + "=" * 100)
    print(" ✅ AUDITORÍA COMPLETADA")
    print("=" * 100)
    
    conn.close()

if __name__ == "__main__":
    main()
