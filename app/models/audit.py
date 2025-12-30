from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    action = Column(String(50))      # LOGIN, UPDATE_PROFILE, CHANGE_PASSWORD
    details = Column(String(255))    # "Cambio de contraseña exitoso"
    ip_address = Column(String(45))
    timestamp = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="audit_logs")
