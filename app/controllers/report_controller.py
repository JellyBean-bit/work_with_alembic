# app/controllers/report_controller.py
from datetime import date
from typing import List

from litestar import Controller, get
from litestar.exceptions import NotFoundException, ValidationException
from litestar.params import Parameter

from app.schemas.report_schemas import ReportResponse
from app.services.report_service import ReportService


class ReportController(Controller):
    path = "/report"

    @get()
    async def get_report_by_date(
        self,
        report_service: ReportService,
        report_date: date = Parameter(
            query="report_date",
            description="Дата отчёта в формате YYYY-MM-DD",
            required=True,
        ),
    ) -> List[ReportResponse]:
        """
        Получить отчёт по заказам за указанную дату.
        """
        reports = await report_service.get_reports_by_date(report_date)

        if not reports:
            raise NotFoundException(
                detail=f"Отчёты за дату {report_date.isoformat()} не найдены"
            )

        return [ReportResponse.model_validate(r) for r in reports]