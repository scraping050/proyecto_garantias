"""
Comparación de datos OECE oficial vs Base de Datos
Basado en la imagen oficial de OECE
"""
import mysql.connector
from config.secrets_manager import get_db_config
import sys

# Fix encoding
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Datos OFICIALES de OECE (extraídos de la imagen)
DATOS_OECE_2024 = {
    'ENERO': 68,
    'FEBRERO': 200,
    'MARZO': 332,
    'ABRIL': 420,
    'MAYO': 533,
    'JUNIO': 473,
    'JULIO': 493,
    'AGOSTO': 664,
    'SEPTIEMBRE': 654,
    'OCTUBRE': 685,
    'NOVIEMBRE': 496,
    'DICIEMBRE': 794
}

DATOS_OECE_2025 = {
    'ENERO': 71,
    'FEBRERO': 228,
    'MARZO': 340,
    'ABRIL': 614,
    'MAYO': 143,
    'JUNIO': 329,
    'JULIO': 389,
    'AGOSTO': 416,
    'SEPTIEMBRE': 488,
    'OCTUBRE': 634,
    'NOVIEMBRE': 377,
    'DICIEMBRE': 202
}

def comparar_con_oece():
    """Compara los datos de BD con los datos oficiales de OECE"""
    
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("=" * 100)
    print(" COMPARACIÓN: BASE DE DATOS vs DATOS OFICIALES OECE")
    print("=" * 100)
    
    # Obtener datos de BD por mes
    cursor.execute("""
        SELECT 
            YEAR(fecha_publicacion) as anio,
            MONTH(fecha_publicacion) as mes,
            COUNT(*) as total
        FROM Licitaciones_Cabecera
        WHERE fecha_publicacion IS NOT NULL
        GROUP BY YEAR(fecha_publicacion), MONTH(fecha_publicacion)
        ORDER BY anio, mes
    """)
    
    datos_bd = {}
    for anio, mes, total in cursor.fetchall():
        if anio not in datos_bd:
            datos_bd[anio] = {}
        datos_bd[anio][mes] = total
    
    # Mapeo de números de mes a nombres
    meses_nombres = {
        1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL',
        5: 'MAYO', 6: 'JUNIO', 7: 'JULIO', 8: 'AGOSTO',
        9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE', 12: 'DICIEMBRE'
    }
    
    # Comparación 2024
    print("\n" + "=" * 100)
    print(" AÑO 2024")
    print("=" * 100)
    print(f"\n{'Mes':<15} | {'OECE':>8} | {'BD':>8} | {'Diferencia':>12} | {'Estado':>10}")
    print("-" * 100)
    
    total_oece_2024 = 0
    total_bd_2024 = 0
    diferencias_2024 = []
    
    for mes_num, mes_nombre in meses_nombres.items():
        oece = DATOS_OECE_2024.get(mes_nombre, 0)
        bd = datos_bd.get(2024, {}).get(mes_num, 0)
        diferencia = bd - oece
        
        total_oece_2024 += oece
        total_bd_2024 += bd
        
        if diferencia != 0:
            diferencias_2024.append((mes_nombre, oece, bd, diferencia))
        
        estado = "✅" if diferencia == 0 else "⚠️" if abs(diferencia) < 10 else "❌"
        signo = "+" if diferencia > 0 else ""
        
        print(f"{mes_nombre:<15} | {oece:>8,} | {bd:>8,} | {signo}{diferencia:>11,} | {estado:>10}")
    
    print("-" * 100)
    print(f"{'TOTAL 2024':<15} | {total_oece_2024:>8,} | {total_bd_2024:>8,} | {'+' if (total_bd_2024-total_oece_2024) > 0 else ''}{total_bd_2024-total_oece_2024:>11,} |")
    
    # Comparación 2025
    print("\n" + "=" * 100)
    print(" AÑO 2025")
    print("=" * 100)
    print(f"\n{'Mes':<15} | {'OECE':>8} | {'BD':>8} | {'Diferencia':>12} | {'Estado':>10}")
    print("-" * 100)
    
    total_oece_2025 = 0
    total_bd_2025 = 0
    diferencias_2025 = []
    
    for mes_num, mes_nombre in meses_nombres.items():
        oece = DATOS_OECE_2025.get(mes_nombre, 0)
        bd = datos_bd.get(2025, {}).get(mes_num, 0)
        diferencia = bd - oece
        
        total_oece_2025 += oece
        total_bd_2025 += bd
        
        if diferencia != 0:
            diferencias_2025.append((mes_nombre, oece, bd, diferencia))
        
        estado = "✅" if diferencia == 0 else "⚠️" if abs(diferencia) < 10 else "❌"
        signo = "+" if diferencia > 0 else ""
        
        print(f"{mes_nombre:<15} | {oece:>8,} | {bd:>8,} | {signo}{diferencia:>11,} | {estado:>10}")
    
    print("-" * 100)
    print(f"{'TOTAL 2025':<15} | {total_oece_2025:>8,} | {total_bd_2025:>8,} | {'+' if (total_bd_2025-total_oece_2025) > 0 else ''}{total_bd_2025-total_oece_2025:>11,} |")
    
    # Resumen general
    print("\n" + "=" * 100)
    print(" RESUMEN GENERAL")
    print("=" * 100)
    
    total_oece = total_oece_2024 + total_oece_2025
    total_bd = total_bd_2024 + total_bd_2025
    diferencia_total = total_bd - total_oece
    
    print(f"\n📊 TOTALES:")
    print(f"   OECE Oficial:     {total_oece:>8,} licitaciones")
    print(f"   Base de Datos:    {total_bd:>8,} licitaciones")
    print(f"   Diferencia:       {'+' if diferencia_total > 0 else ''}{diferencia_total:>8,} ({(diferencia_total/total_oece*100):+.2f}%)")
    
    # Análisis de discrepancias
    print("\n" + "=" * 100)
    print(" ANÁLISIS DE DISCREPANCIAS")
    print("=" * 100)
    
    if diferencias_2024:
        print("\n❌ Meses con diferencias en 2024:")
        for mes, oece, bd, dif in diferencias_2024:
            print(f"   {mes:12}: OECE={oece:>4,} | BD={bd:>4,} | Diferencia={dif:+5,}")
    else:
        print("\n✅ 2024: Todos los meses coinciden perfectamente")
    
    if diferencias_2025:
        print("\n❌ Meses con diferencias en 2025:")
        for mes, oece, bd, dif in diferencias_2025:
            print(f"   {mes:12}: OECE={oece:>4,} | BD={bd:>4,} | Diferencia={dif:+5,}")
    else:
        print("\n✅ 2025: Todos los meses coinciden perfectamente")
    
    # Recomendaciones
    print("\n" + "=" * 100)
    print(" RECOMENDACIONES")
    print("=" * 100)
    
    if diferencia_total == 0:
        print("\n✅ PERFECTO: Los datos coinciden exactamente con OECE")
        print("   No se requiere ninguna acción")
    elif abs(diferencia_total) < 100:
        print(f"\n⚠️ DIFERENCIA MENOR: {abs(diferencia_total)} registros de diferencia")
        print("   Posibles causas:")
        print("   • Duplicados legítimos (modificaciones/re-publicaciones)")
        print("   • Diferencia en criterios de filtrado")
        print("   • Actualización en tiempo real de OECE")
    else:
        print(f"\n❌ DIFERENCIA SIGNIFICATIVA: {abs(diferencia_total)} registros")
        print("   Acciones recomendadas:")
        print("   1. Re-descargar archivos JSON con --force")
        print("   2. Verificar criterios de filtrado en cargador.py")
        print("   3. Investigar duplicados en JSON")
    
    # Identificar archivos a re-descargar
    archivos_recargar = []
    
    for mes, oece, bd, dif in diferencias_2024:
        if dif != 0:
            mes_num = list(meses_nombres.keys())[list(meses_nombres.values()).index(mes)]
            archivos_recargar.append(f"2024-{mes_num:02d}_seace_v3.json")
    
    for mes, oece, bd, dif in diferencias_2025:
        if dif != 0:
            mes_num = list(meses_nombres.keys())[list(meses_nombres.values()).index(mes)]
            archivos_recargar.append(f"2025-{mes_num:02d}_seace_v3.json")
    
    if archivos_recargar:
        print("\n📁 Archivos que podrían necesitar re-descarga:")
        for archivo in archivos_recargar:
            print(f"   • {archivo}")
        
        print("\n💡 Comando para re-descargar:")
        print("   cd 1_motor_etl")
        print("   python descargador.py --years 2024 2025 --force")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    comparar_con_oece()
