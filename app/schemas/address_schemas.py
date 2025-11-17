from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class AddressCreate(BaseModel):
    user_id: UUID
    street: str
    city: str
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str
    is_primary: bool = False


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    is_primary: Optional[bool] = None


class AddressResponse(BaseModel):
    id: UUID
    user_id: UUID
    street: str
    city: str
    state: Optional[str]
    zip_code: Optional[str]
    country: str
    is_primary: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
