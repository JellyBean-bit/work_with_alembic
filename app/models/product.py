from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ProductStatus(str, Enum):
    available = "available"
    out_of_stock = "out_of_stock"
    discontinued = "discontinued"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()
    stock: Mapped[int] = mapped_column(nullable=False, default=0)

    status: Mapped[str] = mapped_column(
        String(20), default=ProductStatus.available.value, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    orders = relationship("Order", back_populates="product")

    __table_args__ = (
        CheckConstraint(
            status.in_([s.value for s in ProductStatus]), name="chk_product_status"
        ),
    )

    def update_status_from_stock(self):
        if self.stock <= 0:
            self.status = ProductStatus.out_of_stock.value
        else:
            self.status = ProductStatus.available.value
