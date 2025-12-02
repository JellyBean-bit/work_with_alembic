import json
from uuid import UUID

import pika

from app.models.order import Order
from app.models.product import Product


def send_to_queue(queue: str, data: dict):
    connection = pika.BlockingConnection(
        pika.URLParameters("amqp://guest:guest@rabbitmq:5672/local")
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()


products = [
    Product(
        id="28276524-7d1e-4783-9d90-4086e5c42e7c",
        name="Молоко",
        price=79.90,
        stock=100,
        description="Пастеризованное 3.2%, 1 л",
    ),
    Product(
        id="a1b2c3d4-e5f6-4a1b-8c9d-0e1f2a3b4c5d",
        name="Хлеб",
        price=45.00,
        stock=50,
        description="Пшеничный, батон нарезной, 400 г",
    ),
    Product(
        id="550e8400-e29b-41d4-a716-446655440000",
        name="Яйца",
        price=85.50,
        stock=200,
        description="Куриные, отборная категория, 10 шт",
    ),
    Product(
        id="f47ac10b-58cc-4372-a567-0e02b2c3d479",
        name="Сыр",
        price=320.00,
        stock=30,
        description="Полутвёрдый, 45%, 200 г",
    ),
    Product(
        id="9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        name="Колбаса",
        price=480.00,
        stock=20,
        description="Варёная «Докторская», 300 г",
    ),
]

orders = [
    Order(
        id=UUID("c3f7e7a2-1b9d-4f0e-8a6c-9d2e5b1f3a4c"),
        user_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        address_id=UUID("123e4567-e89b-12d3-a456-426614174001"),
        product_id=UUID("28276524-7d1e-4783-9d90-4086e5c42e7c"),
        quantity=5,
        total_price=5 * 79.90,
    ),
    Order(
        id=UUID("c3f7e7a2-1b9d-4f0e-8a6c-9d2e5b1f3a4d"),
        user_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        address_id=UUID("123e4567-e89b-12d3-a456-426614174001"),
        product_id=UUID("9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"),
        quantity=2,
        total_price=2 * 480.00,
    ),
    Order(
        id=UUID("7d8e9f0a-2b3c-4d5e-8f1a-0b2c3d4e5f6a"),
        user_id=UUID("123e4567-e89b-12d3-a456-426614174002"),
        address_id=UUID("123e4567-e89b-12d3-a456-426614174003"),
        product_id=UUID("a1b2c3d4-e5f6-4a1b-8c9d-0e1f2a3b4c5d"),
        quantity=10,
        total_price=10 * 45.00,
    ),
    Order(
        id=UUID("e1f2a3b4-c5d6-4e7f-9a0b-1c2d3e4f5a6b"),
        user_id=UUID("123e4567-e89b-12d3-a456-426614174004"),
        address_id=UUID("123e4567-e89b-12d3-a456-426614174005"),
        product_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
        quantity=2,
        total_price=2 * 89.50,
    ),
    Order(
        id=UUID("e1f2a3b4-c5d6-4e7f-9a0b-1c2d3e4f5a6c"),
        user_id=UUID("123e4567-e89b-12d3-a456-426614174004"),
        address_id=UUID("123e4567-e89b-12d3-a456-426614174005"),
        product_id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
        quantity=1,
        total_price=1 * 320.00,
    ),
    Order(
        id=UUID("e1f2a3b4-c5d6-4e7f-9a0b-1c2d3e4f5a6d"),
        user_id=UUID("123e4567-e89b-12d3-a456-426614174004"),
        address_id=UUID("123e4567-e89b-12d3-a456-426614174005"),
        product_id=UUID("28276524-7d1e-4783-9d90-4086e5c42e7c"),
        quantity=100,
        total_price=100 * 79.90,
    ),
]


for p in products:
    send_to_queue(
        "product",
        {
            "id": str(p.id),
            "name": p.name,
            "price": float(p.price),
            "stock": int(p.stock),
            "description": p.description,
        },
    )
    print(f"📤 Продукт {p.name} отправлен")

for o in orders:
    send_to_queue(
        "order",
        {
            "id": str(o.id),
            "user_id": str(o.user_id),
            "address_id": str(o.address_id),
            "product_id": str(o.product_id),
            "quantity": int(o.quantity),
            "total_price": float(o.total_price),
        },
    )
    print(f"📤 Заказ {o.id} отправлен")

print("✅ Тестовые данные опубликованы")
