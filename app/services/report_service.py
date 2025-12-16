# app/services/report_service.py
from datetime import date
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_report import OrderReport


class ReportService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_reports_by_date(self, report_date: date) -> List[OrderReport]:
        result = await self.session.execute(
            select(OrderReport).where(OrderReport.report_at == report_date)
        )
        return list(result.scalars().all())