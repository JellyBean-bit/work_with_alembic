from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.order import Order
from app.schemas.order_schemas import OrderCreate


class OrderRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: UUID):
        result = await self.session.execute(
            select(Order).filter_by(id=order_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: UUID):
        result = await self.session.execute(
            select(Order).filter_by(user_id=user_id)
        )
        return result.scalars().all()

    async def create(self, data: OrderCreate, total_price: float):
        order = Order(**data.model_dump(), total_price=total_price)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def delete(self, order_id: UUID) -> None:
        order = await self.get_by_id(order_id)
        if order:
            await self.session.delete(order)
            await self.session.commit()
