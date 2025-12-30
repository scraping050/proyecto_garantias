"""
Test endpoint to verify UserResponse serialization
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth_schemas import UserResponse

router = APIRouter(prefix="/api/test-serialization", tags=["Test"])

@router.get("/user/{id_corporativo}", response_model=UserResponse)
def test_user_serialization(id_corporativo: str, db: Session = Depends(get_db)):
    """Test endpoint to verify UserResponse includes job_title"""
    user = db.query(User).filter(User.id_corporativo == id_corporativo).first()
    
    if not user:
        return {"error": "User not found"}
    
    # Print user attributes
    print(f"=== TEST SERIALIZATION ===")
    print(f"User object type: {type(user)}")
    print(f"User attributes:")
    for attr in ['id', 'id_corporativo', 'nombre', 'email', 'job_title', 'perfil', 'activo']:
        value = getattr(user, attr, 'ATTRIBUTE NOT FOUND')
        print(f"  {attr}: {value}")
    
    return user
