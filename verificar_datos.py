"""
Script de prueba para verificar que el motor ETL funciona correctamente
"""
import sys
import os

# Agregar el directorio padre al path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from app.database import SessionLocal
from app.models import LicitacionesCabecera, LicitacionesAdjudicaciones, DetalleConsorcios

print("=" * 70)
print("🔍 VERIFICANDO DATOS EN LA BASE DE DATOS")
print("=" * 70)

db = SessionLocal()

try:
    # Contar licitaciones
    total_licitaciones = db.query(LicitacionesCabecera).count()
    print(f"\n📊 Total de Licitaciones: {total_licitaciones}")
    
    # Contar adjudicaciones
    total_adjudicaciones = db.query(LicitacionesAdjudicaciones).count()
    print(f"📊 Total de Adjudicaciones: {total_adjudicaciones}")
    
    # Contar consorcios
    total_consorcios = db.query(DetalleConsorcios).count()
    print(f"📊 Total de Miembros de Consorcios: {total_consorcios}")
    
    if total_licitaciones == 0:
        print("\n⚠️ WARNING: No hay datos en la base de datos")
        print("   Ejecuta el motor ETL para cargar datos:")
        print("   1. Accede a http://localhost:3000/seace/etl")
        print("   2. Click en 'Ejecutar ETL'")
        print("   3. Espera a que termine el proceso")
    else:
        print("\n✅ La base de datos tiene datos!")
        
        # Mostrar algunas licitaciones de ejemplo
        print("\n📋 Últimas 5 licitaciones:")
        licitaciones = db.query(LicitacionesCabecera).order_by(
            LicitacionesCabecera.id_convocatoria.desc()
        ).limit(5).all()
        
        for lic in licitaciones:
            print(f"\n  • {lic.nomenclatura}")
            print(f"    Comprador: {lic.comprador}")
            print(f"    Monto: S/ {lic.monto_estimado:,.2f}" if lic.monto_estimado else "    Monto: N/A")
            print(f"    Estado: {lic.estado_proceso}")
    
    print("\n" + "=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
