"""
Script para verificar datos en la base de datos garantias_seace
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🔍 VERIFICANDO DATOS EN BASE DE DATOS")
print("=" * 80)

try:
    # Conectar a la base de datos
    config = {
        'host': os.getenv("DB_HOST", "localhost"),
        'user': os.getenv("DB_USER", "root"),
        'password': os.getenv("DB_PASS", "123456789"),
        'database': os.getenv("DB_NAME", "garantias_seace"),
        'charset': 'utf8mb4'
    }
    
    print(f"\n📡 Conectando a MySQL...")
    print(f"   Host: {config['host']}")
    print(f"   Database: {config['database']}")
    print(f"   User: {config['user']}")
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("✅ Conexión exitosa\n")
    
    # Verificar tablas
    print("📋 Tablas en la base de datos:")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(f"   - {table[0]}")
    
    # Contar registros en Licitaciones_Cabecera
    print("\n📊 Contando registros...")
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
    total_licitaciones = cursor.fetchone()[0]
    print(f"   Total Licitaciones_Cabecera: {total_licitaciones:,}")
    
    cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
    total_adjudicaciones = cursor.fetchone()[0]
    print(f"   Total Licitaciones_Adjudicaciones: {total_adjudicaciones:,}")
    
    if total_licitaciones > 0:
        print(f"\n✅ HAY DATOS EN LA BASE DE DATOS!")
        print(f"\n📋 Primeras 10 licitaciones:")
        cursor.execute("""
            SELECT 
                id_convocatoria,
                nomenclatura,
                comprador,
                monto_estimado,
                estado_proceso,
                fecha_publicacion
            FROM Licitaciones_Cabecera
            ORDER BY id_convocatoria DESC
            LIMIT 10
        """)
        
        licitaciones = cursor.fetchall()
        for lic in licitaciones:
            print(f"\n  ID: {lic[0]}")
            print(f"  Nomenclatura: {lic[1]}")
            print(f"  Comprador: {lic[2]}")
            print(f"  Monto: S/ {lic[3]:,.2f}" if lic[3] else "  Monto: N/A")
            print(f"  Estado: {lic[4]}")
            print(f"  Fecha: {lic[5]}")
    else:
        print(f"\n⚠️ NO HAY DATOS EN LA BASE DE DATOS")
        print(f"   Ejecuta el motor ETL para cargar datos")
    
    print("\n" + "=" * 80)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 80)
    
except mysql.connector.Error as e:
    print(f"\n❌ ERROR DE MYSQL: {e}")
    print(f"\n💡 Verifica:")
    print(f"   1. Que Laragon/MySQL esté corriendo")
    print(f"   2. Que la base de datos 'garantias_seace' exista")
    print(f"   3. Las credenciales en .env")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("\n🔌 Conexión cerrada")
