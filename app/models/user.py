"""
User model for authentication and authorization.
Matches the exact structure of the 'usuarios' table in MySQL.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration."""
    DIRECTOR = "DIRECTOR"
    COLABORADOR = "COLABORADOR"


class User(Base):
    """User model matching the usuarios table structure."""
    
    __tablename__ = "usuarios"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User credentials
    id_corporativo = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # User information
    nombre = Column(String(255), nullable=True)
    apellidos = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    email_verified = Column(Boolean, default=False)
    phone_number = Column(String(20), nullable=True)
    
    # Professional Profile
    job_title = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    digital_signature_url = Column(String(500), nullable=True)
    
    # Preferences (JSON)
    preferences = Column(JSON, nullable=True, default={})
    
    # Role and status
    perfil = Column(SQLEnum('DIRECTOR', 'COLABORADOR', name='perfil_enum'), nullable=True)
    activo = Column(Boolean, default=True, nullable=True)
    
    # PIN for admin access
    pin_hash = Column(String(255), nullable=True)
    
    # Timestamps
    ultimo_acceso = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    chat_history = relationship("ChatHistory", back_populates="user")
    sessions = relationship("UserSession", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    support_tickets = relationship("SupportTicket", back_populates="user")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id_corporativo='{self.id_corporativo}', perfil='{self.perfil}')>"
