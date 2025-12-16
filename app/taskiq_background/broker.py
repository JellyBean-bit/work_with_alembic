from taskiq_aio_pika import AioPikaBroker
import logging
logger = logging.getLogger(__name__)


broker = AioPikaBroker(
    url="amqp://guest:guest@rabbitmq:5672/local",
    exchange_name="report",
    queue_name="cmd_order"
)

logger.info(f"🔧 broker создан (id={id(broker)})")

@broker.on_event("startup")
async def startup():
    logger.info("🔌 Подключаюсь к RabbitMQ...")
    await broker.startup()
    logger.info("✅ RabbitMQ готов")

@broker.on_event("shutdown")
async def shutdown():
    await broker.shutdown()