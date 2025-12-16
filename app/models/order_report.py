from datetime import datetime
from uuid import UUID

from sqlalchemy import Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class OrderReport(Base):
    __tablename__ = "order_reports"

    report_at: Mapped[datetime] = mapped_column(Date, primary_key=True)
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    count_product: Mapped[int] = mapped_column(Integer, nullable=False)
    