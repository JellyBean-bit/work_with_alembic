from uuid import UUID

from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schemas.order_schemas import OrderCreate
from app.models.order import Order


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
        user_repo: UserRepository
    ):
        self.orders = order_repo
        self.products = product_repo
        self.users = user_repo

    async def get_by_id(self, order_id: UUID) -> Order | None:
        return await self.orders.get_by_id(order_id)

    async def get_by_user(self, user_id: UUID):
        user = await self.users.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return await self.orders.get_by_user(user_id)

    async def create(self, data: OrderCreate) -> Order:
        user = await self.users.get_by_id(data.user_id)
        if not user:
            raise ValueError("User not found")

        product = await self.products.get_by_id(data.product_id)
        if not product:
            raise ValueError("Product not found")

        if product.stock < data.quantity:
            raise ValueError("Not enough stock")

        total_price = product.price * data.quantity

        product.stock -= data.quantity
        await self.products.update(product.id, {"stock": product.stock})

        order = await self.orders.create(data, total_price)
        return order

    async def delete(self, order_id: UUID) -> None:
        order = await self.orders.get_by_id(order_id)
        if not order:
            return None

        user = await self.users.get_by_id(order.user_id)
        if not user:
            raise ValueError("User related to order not found")

        product = await self.products.get_by_id(order.product_id)
        if not product:
            raise ValueError("Product related to order not found")

        product.stock += order.quantity
        await self.products.update(product.id, {"stock": product.stock})

        await self.orders.delete(order_id)
