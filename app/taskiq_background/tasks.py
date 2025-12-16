# app/taskiq_background/tasks.py
import logging
from datetime import date, timedelta
from app.taskiq_background.broker import broker
from app.models.order import Order
from app.models.order_report import OrderReport
from sqlalchemy import func, select
from app.database import async_session_factory

logger = logging.getLogger(__name__)

logger.info("📥 Регистрация задач...")


@broker.task(
    schedule=[
        {
            "cron": "*/1 * * * *",
            "args": [],
            "kwargs": {},
            "schedule_id": "report_every_minute",
            "labels": {
                "name": "report",
                "description": "generate reports"
            }
        }
    ]
)
async def my_scheduled_task() -> None:
    logger.info("⏰ Задача 'report' запущена")
    target_date = date.today() - timedelta(days=1)

    async with async_session_factory() as session:
        stmt = select(Order).where(func.date(Order.created_at) == target_date)
        result = await session.execute(stmt)
        orders = result.scalars().all()

        if not orders:
            logger.info("ℹ️ Нет заказов — отчёт не создан")
            return

        for order in orders:
            session.add(OrderReport(
                report_at=target_date,
                order_id=order.id,
                count_product=order.quantity
            ))
        await session.commit()
        logger.info(f"✅ Отчёт за {target_date} создан ({len(orders)} заказов)")