from uuid import UUID

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from app.schemas.enums import OrderStatus, ProductStatus
from app.schemas.rabbitmq import OrderItemMessage, ProductMessage

products_db: dict[UUID, ProductMessage] = {}

orders_status: dict[UUID, OrderStatus] = {}


broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672/local")
app = FastStream(broker)


@broker.subscriber("product")
async def subscribe_product(product: ProductMessage):
    print(f"📦 Продукт получен: {product.name} (ID={product.id})")

    product.status = (
        ProductStatus.out_of_stock if product.stock <= 0 else ProductStatus.available
    )
    products_db[product.id] = product


@broker.subscriber("order")
async def subscribe_order(item: OrderItemMessage):
    """Обрабатывает одну позицию заказа"""
    print(
        f"📥 Позиция заказа получена: ID={item.id}, товар={item.product_id}, кол-во={item.quantity}"
    )

    prod = products_db.get(item.product_id)
    if not prod:
        print(f"❌ Товар {item.product_id} не найден")
        item.status = OrderStatus.cancelled
    elif prod.status != ProductStatus.available:
        print(f"❌ Товар {item.product_id} ({prod.name}) недоступен: {prod.status}")
        item.status = OrderStatus.cancelled
    elif prod.stock < item.quantity:
        print(
            f"❌ Недостаточно товара {prod.name}: запрошено {item.quantity}, есть {prod.stock}"
        )
        item.status = OrderStatus.cancelled
    else:

        prod.stock -= item.quantity
        if prod.stock == 0:
            prod.status = ProductStatus.out_of_stock
        item.status = OrderStatus.confirmed
        print(f"✅ Позиция {item.id} подтверждена. Остаток {prod.name}: {prod.stock}")

    orders_status[item.id] = item.status


if __name__ == "__main__":
    import asyncio

    print("🚀 Starting RabbitMQ consumer...")
    asyncio.run(app.run())
