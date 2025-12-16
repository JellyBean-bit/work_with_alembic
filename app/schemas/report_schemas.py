# app/schemas/report_schemas.py
from datetime import date
from uuid import UUID

from pydantic import BaseModel


class ReportResponse(BaseModel):
    report_at: date
    order_id: UUID
    count_product: int

    model_config = {"from_attributes": True}  # для model_validate из ORM-объекта