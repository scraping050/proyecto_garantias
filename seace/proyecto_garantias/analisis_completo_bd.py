"""
Análisis Completo de Licitaciones en Base de Datos
- Total de licitaciones
- Detección de duplicados
- Distribución por mes/año
- Análisis de calidad de datos
"""
import mysql.connector
from config.secrets_manager import get_db_config
from datetime import datetime
import sys

# Fix encoding
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def print_section(title):
    """Imprime un separador de sección"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)

def analizar_totales(cursor):
    """Análisis de totales generales"""
    print_section("1. TOTALES GENERALES")
    
    # Total de licitaciones
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
    total_licitaciones = cursor.fetchone()[0]
    print(f"\n📊 Total de Licitaciones: {total_licitaciones:,}")
    
    # Total de adjudicaciones
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    total_adjudicaciones = cursor.fetchone()[0]
    print(f"📊 Total de Adjudicaciones: {total_adjudicaciones:,}")
    
    # Total de contratos
    cursor.execute("SELECT COUNT(*) FROM Contratos")
    total_contratos = cursor.fetchone()[0]
    print(f"📊 Total de Contratos: {total_contratos:,}")
    
    # Promedio de adjudicaciones por licitación
    promedio = total_adjudicaciones / total_licitaciones if total_licitaciones > 0 else 0
    print(f"\n📈 Promedio de adjudicaciones por licitación: {promedio:.2f}")
    
    return total_licitaciones

def analizar_duplicados(cursor):
    """Detección de duplicados por OCID y id_convocatoria"""
    print_section("2. ANÁLISIS DE DUPLICADOS")
    
    # Duplicados por OCID
    cursor.execute("""
        SELECT ocid, COUNT(*) as cantidad
        FROM Licitaciones_Cabecera
        GROUP BY ocid
        HAVING COUNT(*) > 1
        ORDER BY cantidad DESC
    """)
    duplicados_ocid = cursor.fetchall()
    
    print(f"\n🔍 Duplicados por OCID:")
    if duplicados_ocid:
        print(f"   ❌ Se encontraron {len(duplicados_ocid)} OCIDs duplicados")
        print(f"\n   Top 10 OCIDs con más duplicados:")
        for i, (ocid, cantidad) in enumerate(duplicados_ocid[:10], 1):
            print(f"   {i:2}. {ocid:30} | {cantidad:3} veces")
        
        # Total de registros duplicados
        total_duplicados = sum(cantidad - 1 for _, cantidad in duplicados_ocid)
        print(f"\n   📊 Total de registros duplicados: {total_duplicados:,}")
    else:
        print(f"   ✅ No se encontraron duplicados por OCID")
    
    # Duplicados por id_convocatoria
    cursor.execute("""
        SELECT id_convocatoria, COUNT(*) as cantidad
        FROM Licitaciones_Cabecera
        WHERE id_convocatoria IS NOT NULL
        GROUP BY id_convocatoria
        HAVING COUNT(*) > 1
        ORDER BY cantidad DESC
    """)
    duplicados_id = cursor.fetchall()
    
    print(f"\n🔍 Duplicados por id_convocatoria:")
    if duplicados_id:
        print(f"   ❌ Se encontraron {len(duplicados_id)} IDs duplicados")
        print(f"\n   Top 10 IDs con más duplicados:")
        for i, (id_conv, cantidad) in enumerate(duplicados_id[:10], 1):
            print(f"   {i:2}. {id_conv:30} | {cantidad:3} veces")
    else:
        print(f"   ✅ No se encontraron duplicados por id_convocatoria")
    
    return len(duplicados_ocid), len(duplicados_id)

def analizar_distribucion_temporal(cursor):
    """Análisis de distribución por mes y año"""
    print_section("3. DISTRIBUCIÓN TEMPORAL")
    
    # Por año
    print("\n📅 Distribución por AÑO:")
    cursor.execute("""
        SELECT YEAR(fecha_publicacion) as anio, COUNT(*) as total
        FROM Licitaciones_Cabecera
        WHERE fecha_publicacion IS NOT NULL
        GROUP BY YEAR(fecha_publicacion)
        ORDER BY anio
    """)
    por_anio = cursor.fetchall()
    
    for anio, total in por_anio:
        print(f"   {anio}: {total:>6,} licitaciones")
    
    # Por mes (últimos 24 meses)
    print("\n📅 Distribución por MES (últimos 24 meses):")
    cursor.execute("""
        SELECT 
            DATE_FORMAT(fecha_publicacion, '%Y-%m') as mes,
            COUNT(*) as total
        FROM Licitaciones_Cabecera
        WHERE fecha_publicacion IS NOT NULL
        GROUP BY DATE_FORMAT(fecha_publicacion, '%Y-%m')
        ORDER BY mes DESC
        LIMIT 24
    """)
    por_mes = cursor.fetchall()
    
    print("\n   Mes      | Total")
    print("   " + "-" * 30)
    for mes, total in por_mes:
        print(f"   {mes}  | {total:>6,}")
    
    # Estadísticas mensuales
    if por_mes:
        totales = [total for _, total in por_mes]
        promedio = sum(totales) / len(totales)
        maximo = max(totales)
        minimo = min(totales)
        
        print("\n📊 Estadísticas Mensuales (últimos 24 meses):")
        print(f"   Promedio: {promedio:>6,.0f} licitaciones/mes")
        print(f"   Máximo:   {maximo:>6,} licitaciones/mes")
        print(f"   Mínimo:   {minimo:>6,} licitaciones/mes")

def analizar_calidad_datos(cursor):
    """Análisis de calidad de datos"""
    print_section("4. ANÁLISIS DE CALIDAD DE DATOS")
    
    # Campos NULL o vacíos
    print("\n🔍 Campos con valores NULL o vacíos:")
    
    campos = [
        'ocid',
        'id_convocatoria',
        'nomenclatura',
        'descripcion',
        'comprador',
        'monto_estimado',
        'fecha_publicacion',
        'estado_proceso',
        'departamento',
        'provincia',
        'distrito'
    ]
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
    total = cursor.fetchone()[0]
    
    print(f"\n   {'Campo':<25} | NULL/Vacío | % del Total")
    print("   " + "-" * 60)
    
    for campo in campos:
        if campo in ['fecha_publicacion']:
            # Para fechas, solo contar NULL
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM Licitaciones_Cabecera 
                WHERE {campo} IS NULL
            """)
        else:
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM Licitaciones_Cabecera 
                WHERE {campo} IS NULL OR {campo} = ''
            """)
        nulos = cursor.fetchone()[0]
        porcentaje = (nulos / total * 100) if total > 0 else 0
        
        estado = "✅" if nulos == 0 else "⚠️" if porcentaje < 5 else "❌"
        print(f"   {estado} {campo:<22} | {nulos:>10,} | {porcentaje:>6.2f}%")
    
    # Fechas inválidas
    print("\n🔍 Validación de Fechas:")
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Cabecera 
        WHERE fecha_publicacion > CURDATE()
    """)
    fechas_futuras = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Licitaciones_Cabecera 
        WHERE fecha_publicacion < '2020-01-01'
    """)
    fechas_antiguas = cursor.fetchone()[0]
    
    print(f"   Fechas futuras (> hoy): {fechas_futuras:,}")
    print(f"   Fechas muy antiguas (< 2020): {fechas_antiguas:,}")

def analizar_estados(cursor):
    """Análisis de estados de proceso"""
    print_section("5. DISTRIBUCIÓN POR ESTADO")
    
    cursor.execute("""
        SELECT estado_proceso, COUNT(*) as total
        FROM Licitaciones_Cabecera
        GROUP BY estado_proceso
        ORDER BY total DESC
    """)
    estados = cursor.fetchall()
    
    print(f"\n   {'Estado':<30} | Total")
    print("   " + "-" * 50)
    
    for estado, total in estados:
        estado_str = estado if estado else "(NULL)"
        print(f"   {estado_str:<30} | {total:>6,}")

def generar_resumen_ejecutivo(cursor, total_licitaciones, dup_ocid, dup_id):
    """Genera un resumen ejecutivo del análisis"""
    print_section("RESUMEN EJECUTIVO")
    
    print(f"""
📊 TOTALES:
   • Licitaciones en BD: {total_licitaciones:,}
   • Duplicados por OCID: {dup_ocid:,}
   • Duplicados por ID: {dup_id:,}

✅ CALIDAD DE DATOS:
   • Base de datos: garantias_seace
   • Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
   
⚠️ RECOMENDACIONES:
""")
    
    if dup_ocid > 0:
        print(f"   • Investigar y eliminar {dup_ocid:,} OCIDs duplicados")
    else:
        print(f"   • ✅ No hay duplicados por OCID")
    
    if dup_id > 0:
        print(f"   • Investigar y eliminar {dup_id:,} IDs duplicados")
    else:
        print(f"   • ✅ No hay duplicados por ID")

def main():
    """Función principal"""
    print("=" * 80)
    print(" ANÁLISIS COMPLETO DE LICITACIONES EN BASE DE DATOS")
    print("=" * 80)
    print(f" Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Conectar a BD
        conn = mysql.connector.connect(**get_db_config())
        cursor = conn.cursor()
        
        # Ejecutar análisis
        total_licitaciones = analizar_totales(cursor)
        dup_ocid, dup_id = analizar_duplicados(cursor)
        analizar_distribucion_temporal(cursor)
        analizar_calidad_datos(cursor)
        analizar_estados(cursor)
        generar_resumen_ejecutivo(cursor, total_licitaciones, dup_ocid, dup_id)
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 80)
        print(" ANÁLISIS COMPLETADO")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
