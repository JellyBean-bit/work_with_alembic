from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class OrderCreate(BaseModel):
    user_id: UUID
    address_id: UUID
    product_id: UUID
    quantity: int


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    address_id: UUID
    product_id: UUID
    quantity: int
    total_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
