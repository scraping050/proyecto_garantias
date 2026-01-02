"""
Script de ejecución completa para migrar y recargar todos los datos
"""
import subprocess
import sys
import os

def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*80}")
    print(f"{descripcion}")
    print(f"{'='*80}")
    print(f"Comando: {comando}\n")
    
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    
    if resultado.stdout:
        print(resultado.stdout)
    if resultado.stderr:
        print(resultado.stderr)
    
    if resultado.returncode != 0:
        print(f"\n❌ ERROR: El comando falló con código {resultado.returncode}")
        return False
    else:
        print(f"\n✅ Comando ejecutado exitosamente")
        return True

def main():
    print("="*80)
    print("PROCESO COMPLETO: MIGRACIÓN Y RECARGA DE DATOS")
    print("="*80)
    print("\nEste script ejecutará los siguientes pasos:")
    print("1. Migrar base de datos (PRIMARY KEY: id_convocatoria -> ocid)")
    print("2. Limpiar control de cargas")
    print("3. Re-ejecutar cargador con nueva estructura")
    print("4. Verificar resultados")
    print("\n⚠️  ADVERTENCIA: Este proceso modificará la estructura de la base de datos")
    
    respuesta = input("\n¿Deseas continuar? (si/no): ")
    if respuesta.lower() not in ['si', 's', 'yes', 'y']:
        print("\nProceso cancelado por el usuario")
        return
    
    # Paso 1: Migrar base de datos
    if not ejecutar_comando("python migrar_pk_a_ocid.py", "PASO 1: Migración de Base de Datos"):
        print("\n❌ Migración fallida. Proceso detenido.")
        return
    
    # Paso 2: Limpiar control de cargas
    if not ejecutar_comando("python limpiar_control_cargas.py", "PASO 2: Limpieza de Control de Cargas"):
        print("\n⚠️  Advertencia: Limpieza de control falló, pero continuando...")
    
    # Paso 3: Re-ejecutar cargador
    if not ejecutar_comando("cd 1_motor_etl && python cargador.py", "PASO 3: Re-ejecución del Cargador"):
        print("\n❌ Carga de datos fallida. Proceso detenido.")
        return
    
    # Paso 4: Verificar resultados
    if not ejecutar_comando("python verificar_licitacion_publica.py", "PASO 4: Verificación de Resultados"):
        print("\n⚠️  Advertencia: Verificación falló")
    
    print("\n" + "="*80)
    print("PROCESO COMPLETADO")
    print("="*80)
    print("\nRevisa los resultados arriba para confirmar que se cargaron los 9,712 registros")

if __name__ == "__main__":
    main()
