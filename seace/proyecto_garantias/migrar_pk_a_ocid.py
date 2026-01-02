"""
Script de migración: Cambiar PRIMARY KEY de id_convocatoria a ocid
Esto permitirá cargar todos los 9,712 registros de Licitación Pública
"""
import mysql.connector
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from secrets_manager import get_db_config

def migrar():
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    print("="*80)
    print("MIGRACIÓN: PRIMARY KEY id_convocatoria -> ocid")
    print("="*80)
    print("\nEsta migración permitirá cargar TODOS los registros incluyendo duplicados")
    print("de id_convocatoria que tienen OCIDs únicos.\n")
    
    input("Presiona ENTER para continuar o Ctrl+C para cancelar...")
    
    try:
        # 1. Eliminar foreign keys
        print("\n1. Eliminando foreign keys...")
        try:
            cursor.execute("ALTER TABLE Contratos DROP FOREIGN KEY Contratos_ibfk_1")
            print("   - Contratos_ibfk_1 eliminada")
        except:
            print("   - Contratos_ibfk_1 no existe")
        
        try:
            cursor.execute("ALTER TABLE Contratos DROP FOREIGN KEY Contratos_ibfk_2")
            print("   - Contratos_ibfk_2 eliminada")
        except:
            print("   - Contratos_ibfk_2 no existe")
        
        try:
            cursor.execute("ALTER TABLE Licitaciones_Adjudicaciones DROP FOREIGN KEY Licitaciones_Adjudicaciones_ibfk_1")
            print("   - Licitaciones_Adjudicaciones_ibfk_1 eliminada")
        except:
            print("   - Licitaciones_Adjudicaciones_ibfk_1 no existe")
        
        # 2. Cambiar PRIMARY KEY en Licitaciones_Cabecera
        print("\n2. Cambiando PRIMARY KEY en Licitaciones_Cabecera...")
        try:
            cursor.execute("ALTER TABLE Licitaciones_Cabecera DROP PRIMARY KEY")
            print("   - PRIMARY KEY antigua eliminada")
        except Exception as e:
            print(f"   - Error eliminando PK: {e}")
        
        try:
            cursor.execute("ALTER TABLE Licitaciones_Cabecera DROP INDEX ocid")
            print("   - INDEX ocid eliminado")
        except:
            print("   - INDEX ocid no existe")
        
        cursor.execute("ALTER TABLE Licitaciones_Cabecera ADD PRIMARY KEY (ocid)")
        print("   - Nueva PRIMARY KEY (ocid) creada")
        
        cursor.execute("ALTER TABLE Licitaciones_Cabecera ADD INDEX idx_id_convocatoria (id_convocatoria)")
        print("   - INDEX idx_id_convocatoria creado")
        
        # 3. Actualizar Licitaciones_Adjudicaciones
        print("\n3. Actualizando Licitaciones_Adjudicaciones...")
        
        # Verificar si columna ocid ya existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'Licitaciones_Adjudicaciones' 
            AND COLUMN_NAME = 'ocid'
        """)
        existe_ocid = cursor.fetchone()[0] > 0
        
        if not existe_ocid:
            cursor.execute("""
                ALTER TABLE Licitaciones_Adjudicaciones 
                ADD COLUMN ocid VARCHAR(100) AFTER id_convocatoria
            """)
            print("   - Columna ocid agregada")
            
            # Copiar ocid desde Licitaciones_Cabecera
            cursor.execute("""
                UPDATE Licitaciones_Adjudicaciones a
                JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
                SET a.ocid = c.ocid
            """)
            print("   - Columna ocid poblada con datos")
        else:
            print("   - Columna ocid ya existe")
        
        # 4. Actualizar Contratos
        print("\n4. Actualizando Contratos...")
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'Contratos' 
            AND COLUMN_NAME = 'ocid'
        """)
        existe_ocid_contratos = cursor.fetchone()[0] > 0
        
        if not existe_ocid_contratos:
            cursor.execute("""
                ALTER TABLE Contratos 
                ADD COLUMN ocid VARCHAR(100) AFTER id_convocatoria
            """)
            print("   - Columna ocid agregada")
            
            cursor.execute("""
                UPDATE Contratos co
                JOIN Licitaciones_Cabecera c ON co.id_convocatoria = c.id_convocatoria
                SET co.ocid = c.ocid
            """)
            print("   - Columna ocid poblada con datos")
        else:
            print("   - Columna ocid ya existe")
        
        # 5. Recrear foreign keys
        print("\n5. Recreando foreign keys...")
        
        try:
            cursor.execute("""
                ALTER TABLE Licitaciones_Adjudicaciones 
                ADD FOREIGN KEY (ocid) REFERENCES Licitaciones_Cabecera(ocid)
                ON DELETE CASCADE ON UPDATE CASCADE
            """)
            print("   - FK Licitaciones_Adjudicaciones -> Licitaciones_Cabecera creada")
        except Exception as e:
            print(f"   - FK ya existe o error: {e}")
        
        try:
            cursor.execute("""
                ALTER TABLE Contratos 
                ADD FOREIGN KEY (id_adjudicacion) REFERENCES Licitaciones_Adjudicaciones(id_adjudicacion)
                ON DELETE CASCADE ON UPDATE CASCADE
            """)
            print("   - FK Contratos -> Licitaciones_Adjudicaciones creada")
        except Exception as e:
            print(f"   - FK ya existe o error: {e}")
        
        try:
            cursor.execute("""
                ALTER TABLE Contratos 
                ADD FOREIGN KEY (ocid) REFERENCES Licitaciones_Cabecera(ocid)
                ON DELETE CASCADE ON UPDATE CASCADE
            """)
            print("   - FK Contratos -> Licitaciones_Cabecera creada")
        except Exception as e:
            print(f"   - FK ya existe o error: {e}")
        
        conn.commit()
        
        print("\n" + "="*80)
        print("MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*80)
        print("\nPróximos pasos:")
        print("1. Limpiar control_cargas: python limpiar_control_cargas.py")
        print("2. Actualizar cargador.py (ver implementation_plan.md)")
        print("3. Re-ejecutar ETL: cd 1_motor_etl && python cargador.py")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nRevertiendo cambios...")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if migrar():
        print("\n✅ Migración exitosa")
    else:
        print("\n❌ Migración fallida")
