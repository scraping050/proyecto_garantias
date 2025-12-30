"""
Script to update users in the database.
Deletes old users and adds new ones with specified roles and credentials.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
    from app.utils.security import get_password_hash
    
    # Load environment variables
    load_dotenv()
    
    # Get database connection
    database_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:123456789@localhost:3306/garantias_seace')
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # Start transaction
        trans = conn.begin()
        
        try:
            print("=" * 60)
            print("ACTUALIZANDO USUARIOS EN LA BASE DE DATOS")
            print("=" * 60)
            
            # 1. Delete old users
            print("\n1. Eliminando usuarios antiguos...")
            users_to_delete = ["Chaupin", "Olimpio", "Brayan"]
            
            for username in users_to_delete:
                result = conn.execute(
                    text("DELETE FROM usuarios WHERE id_corporativo = :username OR nombre LIKE :name_pattern"),
                    {"username": username, "name_pattern": f"%{username}%"}
                )
                if result.rowcount > 0:
                    print(f"   ✓ Eliminado: {username} ({result.rowcount} registro(s))")
                else:
                    print(f"   ○ No encontrado: {username}")
            
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
            for user_data in new_users:
                # Check if user exists
                result = conn.execute(
                    text("SELECT id FROM usuarios WHERE id_corporativo = :id_corp"),
                    {"id_corp": user_data["id_corporativo"]}
                )
                existing = result.fetchone()
                
                password_hash = get_password_hash(user_data["password"])
                
                if existing:
                    # Update existing user
                    conn.execute(
                        text("""
                            UPDATE usuarios 
                            SET nombre = :nombre,
                                perfil = :perfil,
                                job_title = :job_title,
                                password_hash = :password_hash,
                                activo = 1,
                                updated_at = :updated_at
                            WHERE id_corporativo = :id_corp
                        """),
                        {
                            "nombre": user_data["nombre"],
                            "perfil": user_data["perfil"],
                            "job_title": user_data["job_title"],
                            "password_hash": password_hash,
                            "id_corp": user_data["id_corporativo"],
                            "updated_at": datetime.now()
                        }
                    )
                    print(f"   ✓ Actualizado: {user_data['nombre']} ({user_data['perfil']})")
                else:
                    # Insert new user
                    conn.execute(
                        text("""
                            INSERT INTO usuarios 
                            (id_corporativo, nombre, perfil, job_title, password_hash, activo, email, created_at)
                            VALUES 
                            (:id_corp, :nombre, :perfil, :job_title, :password_hash, 1, :email, :created_at)
                        """),
                        {
                            "id_corp": user_data["id_corporativo"],
                            "nombre": user_data["nombre"],
                            "perfil": user_data["perfil"],
                            "job_title": user_data["job_title"],
                            "password_hash": password_hash,
                            "email": f"{user_data['id_corporativo'].lower()}@mqs.com",
                            "created_at": datetime.now()
                        }
                    )
                    print(f"   ✓ Creado: {user_data['nombre']} ({user_data['perfil']})")
            
            # Commit transaction
            trans.commit()
            
            print("\n" + "=" * 60)
            print("✓ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
            print("=" * 60)
            print("\nResumen:")
            print(f"  • Usuarios eliminados: {len(users_to_delete)}")
            print(f"  • Usuarios creados/actualizados: {len(new_users)}")
            print(f"  • Administradores (DIRECTOR): {sum(1 for u in new_users if u['perfil'] == 'DIRECTOR')}")
            print(f"  • Colaboradores: {sum(1 for u in new_users if u['perfil'] == 'COLABORADOR')}")
            print("\nCredenciales de acceso:")
            for user in new_users:
                print(f"  • {user['nombre']}: {user['id_corporativo']} / {user['password']}")
            
        except Exception as e:
            trans.rollback()
            print(f"\n✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    main()
