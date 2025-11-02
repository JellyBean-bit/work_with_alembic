from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    description: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True