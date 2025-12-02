from typing import List
from uuid import UUID

from pydantic import BaseModel

from .enums import OrderStatus, ProductStatus


class OrderItem(BaseModel):
    product_id: UUID
    quantity: int


class ProductMessage(BaseModel):
    id: UUID
    name: str
    price: float
    stock: int
    description: str | None = None
    status: ProductStatus = ProductStatus.available


class OrderMessage(BaseModel):
    id: UUID
    user_id: UUID
    address_id: UUID
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.pending


class OrderItemMessage(BaseModel):
    id: UUID
    user_id: UUID
    address_id: UUID
    product_id: UUID
    quantity: int
    total_price: float
    status: OrderStatus = OrderStatus.pending
