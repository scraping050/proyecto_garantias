"""
Chat History Model for conversation memory.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ChatHistory(Base):
    """Model for storing chat conversation history."""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("usuarios.id_corporativo"), nullable=False)
    session_id = Column(String(100), nullable=False, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to User
    user = relationship("User", back_populates="chat_history")
