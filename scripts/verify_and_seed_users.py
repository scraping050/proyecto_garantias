import sys
import os

# Add the parent directory to sys.path to resolve app imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.session import UserSession
# Import other models to resolve relationships
try:
    from app.models.audit import AuditLog
except ImportError:
    pass 
try:
    from app.models.notification import Notification
except ImportError:
    pass
try:
    from app.models.chat_history import ChatHistory
except ImportError:
    pass
try:
    from app.models.support import SupportTicket
except ImportError:
    pass    
from app.utils.security import get_password_hash

# Credentials provided by user
USERS_TO_SEED = [
    {
        "id_corporativo": "Diana",
        "nombre": "Diana",
        "perfil": "DIRECTOR", # Mapped from 'roll admin'
        "job_title": "Asistente de operaciones",
        "password": "OpeGe10",
        "pin": "123123"
    },
    {
        "id_corporativo": "Michel", # Using provided spelling
        "nombre": "Michel",
        "perfil": "DIRECTOR",
        "job_title": "Asesor Michael",
        "password": "AseGe10",
        "pin": "123123"
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

def seed_users():
    db = SessionLocal()
    try:
        print("Checking users in database...")
        for user_data in USERS_TO_SEED:
            user = db.query(User).filter(User.id_corporativo == user_data["id_corporativo"]).first()
            
            if not user:
                print(f"Creating user: {user_data['id_corporativo']}")
                hashed_pw = get_password_hash(user_data["password"])
                
                # Handle PIN if present
                pin_hash = None
                if "pin" in user_data:
                    pin_hash = get_password_hash(user_data["pin"])

                new_user = User(
                    id_corporativo=user_data["id_corporativo"],
                    nombre=user_data["nombre"],
                    password_hash=hashed_pw,
                    perfil=user_data["perfil"],
                    job_title=user_data["job_title"],
                    pin_hash=pin_hash,
                    activo=True
                )
                db.add(new_user)
                db.commit()
                print(f"User {user_data['id_corporativo']} created successfully.")
            else:
                print(f"User {user_data['id_corporativo']} already exists. Updating details...")
                # Optional: Update password/details to match specific request
                user.password_hash = get_password_hash(user_data["password"])
                user.job_title = user_data["job_title"]
                user.perfil = user_data["perfil"]
                if "pin" in user_data:
                   user.pin_hash = get_password_hash(user_data["pin"])
                
                db.commit()
                print(f"User {user_data['id_corporativo']} updated.")

    except Exception as e:
        print(f"Error seeding users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
