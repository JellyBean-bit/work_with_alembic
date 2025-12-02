from enum import Enum


class ProductStatus(str, Enum):
    available = "available"
    out_of_stock = "out_of_stock"
    discontinued = "discontinued"


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    cancelled = "cancelled"
