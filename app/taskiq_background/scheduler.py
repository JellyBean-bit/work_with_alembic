# app/taskiq_background/scheduler.py
import logging
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from app.taskiq_background.broker import broker

# 🔑 КЛЮЧЕВОЙ МОМЕНТ: импортируем задачи, чтобы они зарегистрировались в broker
import app.taskiq_background.tasks  # ← просто импорт — этого достаточно!

logger = logging.getLogger(__name__)
logger.info("▶️ scheduler.py: задачи импортированы, создаю планировщик")

scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])
logger.info("✅ TaskiqScheduler создан и готов")

