from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from uuid import uuid4, UUID

from .base import Base


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now
    )

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")
