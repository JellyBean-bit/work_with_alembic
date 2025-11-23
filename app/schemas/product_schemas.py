from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    stock: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None


class ProductResponse(BaseModel):
    id: UUID
    name: str
    price: float
    description: Optional[str]
    stock: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
