import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.utils.security import get_password_hash

def update_users():
    db = SessionLocal()
    try:
        # 1. Delete users
        users_to_delete = ["Chaupin", "Olimpio", "Brayan"]
        print("Eliminando usuarios antiguos...")
        for name in users_to_delete:
            # Try to find by id_corporativo or nombre
            user = db.query(User).filter(
                (User.id_corporativo == name) | (User.nombre.like(f"%{name}%"))
            ).first()
            
            if user:
                print(f"Eliminando usuario: {user.nombre} ({user.id_corporativo})")
                db.delete(user)
            else:
                print(f"Usuario no encontrado para eliminar: {name}")
        
        db.commit()
        print("Eliminación completada.\n")

        # 2. Add new users
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

        print("Creando nuevos usuarios...")
        for user_data in new_users:
            # Check if user already exists (to avoid duplicates if script runs twice)
            existing = db.query(User).filter(User.id_corporativo == user_data["id_corporativo"]).first()
            if existing:
                print(f"Actualizando usuario existente: {user_data['nombre']}")
                existing.nombre = user_data["nombre"]
                existing.perfil = user_data["perfil"]
                existing.job_title = user_data["job_title"]
                existing.password_hash = get_password_hash(user_data["password"])
                existing.activo = True
            else:
                print(f"Creando usuario: {user_data['nombre']}")
                new_user = User(
                    id_corporativo=user_data["id_corporativo"],
                    nombre=user_data["nombre"],
                    perfil=user_data["perfil"],
                    job_title=user_data["job_title"],
                    password_hash=get_password_hash(user_data["password"]),
                    activo=True,
                    email=f"{user_data['id_corporativo'].lower()}@example.com" # Placeholder email
                )
                db.add(new_user)
        
        db.commit()
        print("Usuarios creados/actualizados exitosamente.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_users()
