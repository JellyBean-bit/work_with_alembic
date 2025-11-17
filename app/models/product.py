from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from uuid import uuid4, UUID

from .base import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()
    stock: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now
    )
    orders = relationship("Order", back_populates="product")
