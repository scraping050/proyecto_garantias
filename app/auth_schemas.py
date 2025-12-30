"""
Authentication schemas for request/response validation.
Updated to match the User model structure.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    id_corporativo: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str = Field(..., min_length=3)
    perfil: str = Field(default="COLABORADOR", pattern="^(DIRECTOR|COLABORADOR)$")
    job_title: Optional[str] = None



class UserLogin(BaseModel):
    """Schema for user login."""
    id_corporativo: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    id_corporativo: str
    nombre: Optional[str] = None
    email: Optional[str] = None
    perfil: Optional[str] = None
    activo: Optional[bool] = None
    job_title: Optional[str] = None
    avatar_url: Optional[str] = None
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class PinVerification(BaseModel):
    """Schema for admin PIN verification."""
    pin: str = Field(..., min_length=6, max_length=6)


class PinVerificationResponse(BaseModel):
    """Schema for PIN verification response."""
    valid: bool
    message: str
