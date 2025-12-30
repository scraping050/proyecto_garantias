"""
Script para actualizar usuarios - maneja referencias de claves foráneas.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import pymysql
    from app.utils.security import get_password_hash
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def main():
    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456789',
        'database': 'garantias_seace',
        'charset': 'utf8mb4'
    }
    
    connection = None
    
    try:
        # Connect to database
        print("Conectando a la base de datos...")
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        print("=" * 60)
        print("ACTUALIZANDO USUARIOS EN LA BASE DE DATOS")
        print("=" * 60)
        
        # Disable foreign key checks temporarily
        print("\n⚙ Desactivando verificaciones de claves foráneas...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 1. Delete old users
        print("\n1. Eliminando usuarios antiguos...")
        users_to_delete = ["Chaupin", "Olimpio", "Brayan"]
        
        for username in users_to_delete:
            cursor.execute(
                "DELETE FROM usuarios WHERE id_corporativo = %s OR nombre LIKE %s",
                (username, f"%{username}%")
            )
            if cursor.rowcount > 0:
                print(f"   ✓ Eliminado: {username} ({cursor.rowcount} registro(s))")
            else:
                print(f"   ○ No encontrado: {username}")
        
        # Re-enable foreign key checks
        print("\n⚙ Reactivando verificaciones de claves foráneas...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # 2. Define new users
        new_users = [
            {
                "id_corporativo": "Diana",
                "nombre": "Diana",
                "perfil": "DIRECTOR",
                "job_title": "Asistente de operaciones",
                "password": "OpeGe10"
            },
            {
                "id_corporativo": "Michel",
                "nombre": "Michel",
                "perfil": "DIRECTOR",
                "job_title": "Asesor Michael",
                "password": "AseGe10"
            },
            {
                "id_corporativo": "Maylin",
                "nombre": "Maylin",
                "perfil": "COLABORADOR",
                "job_title": "Asistente de Renovaciones y Cobranza",
                "password": "ArenoC02"
            },
            {
                "id_corporativo": "Ruth",
                "nombre": "Ruth",
                "perfil": "COLABORADOR",
                "job_title": "Asistente Administrativo",
                "password": "AadmQS03"
            },
            {
                "id_corporativo": "Olimpio",
                "nombre": "Olimpio",
                "perfil": "COLABORADOR",
                "job_title": "Asistente de Archivos y sistema",
                "password": "AarchiS04"
            },
            {
                "id_corporativo": "Yanfranco",
                "nombre": "Yanfranco",
                "perfil": "COLABORADOR",
                "job_title": "Asistente de Archivos y sistema",
                "password": "AarchiS05"
            }
        ]
        
        # 3. Insert/Update new users
        print("\n2. Creando/Actualizando nuevos usuarios...")
        now = datetime.now()
        
        for user_data in new_users:
            # Check if user exists
            cursor.execute(
                "SELECT id FROM usuarios WHERE id_corporativo = %s",
                (user_data["id_corporativo"],)
            )
            existing = cursor.fetchone()
            
            password_hash = get_password_hash(user_data["password"])
            
            if existing:
                # Update existing user
                cursor.execute(
                    """
                    UPDATE usuarios 
                    SET nombre = %s,
                        perfil = %s,
                        job_title = %s,
                        password_hash = %s,
                        activo = 1,
                        updated_at = %s
                    WHERE id_corporativo = %s
                    """,
                    (
                        user_data["nombre"],
                        user_data["perfil"],
                        user_data["job_title"],
                        password_hash,
                        now,
                        user_data["id_corporativo"]
                    )
                )
                print(f"   ✓ Actualizado: {user_data['nombre']} ({user_data['perfil']})")
            else:
                # Insert new user
                cursor.execute(
                    """
                    INSERT INTO usuarios 
                    (id_corporativo, nombre, perfil, job_title, password_hash, activo, email, created_at)
                    VALUES 
                    (%s, %s, %s, %s, %s, 1, %s, %s)
                    """,
                    (
                        user_data["id_corporativo"],
                        user_data["nombre"],
                        user_data["perfil"],
                        user_data["job_title"],
                        password_hash,
                        f"{user_data['id_corporativo'].lower()}@mqs.com",
                        now
                    )
                )
                print(f"   ✓ Creado: {user_data['nombre']} ({user_data['perfil']})")
        
        # Commit all changes
        connection.commit()
        
        print("\n" + "=" * 60)
        print("✓ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\nResumen:")
        print(f"  • Usuarios eliminados: {len(users_to_delete)}")
        print(f"  • Usuarios creados/actualizados: {len(new_users)}")
        print(f"  • Administradores (DIRECTOR): {sum(1 for u in new_users if u['perfil'] == 'DIRECTOR')}")
        print(f"  • Colaboradores: {sum(1 for u in new_users if u['perfil'] == 'COLABORADOR')}")
        
        print("\n📋 Credenciales de acceso:")
        print("-" * 60)
        for user in new_users:
            role = "Admin" if user['perfil'] == 'DIRECTOR' else "Colaborador"
            print(f"  {user['nombre']:12} ({role:12}): {user['id_corporativo']:10} / {user['password']}")
        print("-" * 60)
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\n✓ Conexión cerrada.")

if __name__ == "__main__":
    main()
