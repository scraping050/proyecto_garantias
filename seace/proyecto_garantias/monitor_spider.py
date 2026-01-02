"""
Monitor de progreso del Spider en tiempo real
"""
import mysql.connector
from config.secrets_manager import get_db_config
import time
import sys

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def mostrar_progreso():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("=" * 80)
    print(" 📊 MONITOR DE PROGRESO - SPIDER_GARANTIAS.PY")
    print("=" * 80)
    
    while True:
        cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE entidad_financiera IS NOT NULL")
        procesados = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE entidad_financiera IS NULL")
        pendientes = cursor.fetchone()[0]
        
        porcentaje = (procesados / total * 100) if total > 0 else 0
        
        # Barra de progreso
        barra_total = 50
        barra_llena = int(barra_total * porcentaje / 100)
        barra = "█" * barra_llena + "░" * (barra_total - barra_llena)
        
        # Limpiar pantalla (solo en Windows)
        print("\033[H\033[J", end="")
        
        print("=" * 80)
        print(" 📊 MONITOR DE PROGRESO - SPIDER_GARANTIAS.PY")
        print("=" * 80)
        print(f"\n  Total adjudicaciones:     {total:,}")
        print(f"  ✅ Procesadas:            {procesados:,}")
        print(f"  ⏳ Pendientes:            {pendientes:,}")
        print(f"\n  Progreso: [{barra}] {porcentaje:.2f}%")
        
        if pendientes == 0:
            print("\n  🎉 ¡COMPLETADO! Todas las adjudicaciones han sido procesadas.")
            break
        
        # Estimación de tiempo
        if procesados > 0:
            # Asumiendo ~50 registros por minuto
            minutos_restantes = pendientes / 50
            horas = int(minutos_restantes // 60)
            mins = int(minutos_restantes % 60)
            print(f"\n  ⏱️  Tiempo estimado restante: {horas}h {mins}m")
        
        print(f"\n  Última actualización: {time.strftime('%H:%M:%S')}")
        print("  Presiona Ctrl+C para salir")
        print("=" * 80)
        
        time.sleep(10)  # Actualizar cada 10 segundos
    
    conn.close()

if __name__ == "__main__":
    try:
        mostrar_progreso()
    except KeyboardInterrupt:
        print("\n\n  ⏹️  Monitor detenido por el usuario")
    except Exception as e:
        print(f"\n  ❌ Error: {e}")
