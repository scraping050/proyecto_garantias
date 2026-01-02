"""
Script de ejecución COMPLETA para cargar todos los 10,043 registros
Incluye migración OCID + re-descarga de datos actualizados
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
    print("PROCESO COMPLETO: CARGA DE TODOS LOS 10,043 REGISTROS")
    print("="*80)
    print("\nEste script ejecutará:")
    print("1. Migración de base de datos (OCID como PRIMARY KEY)")
    print("2. Re-descarga de JSONs actualizados (--force)")
    print("3. Limpieza de control de cargas")
    print("4. Carga completa de datos")
    print("5. Verificación de resultados")
    print("\n⚠️  Este proceso puede tomar varios minutos")
    
    respuesta = input("\n¿Deseas continuar? (si/no): ")
    if respuesta.lower() not in ['si', 's', 'yes', 'y']:
        print("\nProceso cancelado por el usuario")
        return
    
    # Paso 1: Migrar base de datos
    print("\n" + "="*80)
    print("FASE 1: MIGRACIÓN DE BASE DE DATOS")
    print("="*80)
    if not ejecutar_comando("python migrar_pk_a_ocid.py", "Migrando PRIMARY KEY a OCID"):
        print("\n❌ Migración fallida. Proceso detenido.")
        return
    
    # Paso 2: Re-descargar JSONs con datos actualizados
    print("\n" + "="*80)
    print("FASE 2: RE-DESCARGA DE DATOS ACTUALIZADOS")
    print("="*80)
    if not ejecutar_comando("cd 1_motor_etl && python descargador.py --force", "Re-descargando JSONs actualizados"):
        print("\n⚠️  Advertencia: Descarga falló, pero continuando con datos existentes...")
    
    # Paso 3: Limpiar control de cargas
    print("\n" + "="*80)
    print("FASE 3: LIMPIEZA DE CONTROL")
    print("="*80)
    if not ejecutar_comando("python limpiar_control_cargas.py", "Limpiando control de cargas"):
        print("\n⚠️  Advertencia: Limpieza falló, pero continuando...")
    
    # Paso 4: Re-ejecutar cargador
    print("\n" + "="*80)
    print("FASE 4: CARGA COMPLETA DE DATOS")
    print("="*80)
    if not ejecutar_comando("cd 1_motor_etl && python cargador.py", "Cargando todos los datos"):
        print("\n❌ Carga de datos fallida. Proceso detenido.")
        return
    
    # Paso 5: Verificar resultados
    print("\n" + "="*80)
    print("FASE 5: VERIFICACIÓN DE RESULTADOS")
    print("="*80)
    if not ejecutar_comando("python verificar_licitacion_publica.py", "Verificando resultados"):
        print("\n⚠️  Advertencia: Verificación falló")
    
    print("\n" + "="*80)
    print("PROCESO COMPLETADO")
    print("="*80)
    print("\nRevisa los resultados arriba.")
    print("Deberías ver aproximadamente 10,043 registros cargados.")

if __name__ == "__main__":
    main()
