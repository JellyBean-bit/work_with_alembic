from typing import List
from uuid import UUID

from litestar import Controller, delete, get, post
from litestar.exceptions import NotFoundException, ValidationException

from app.schemas.order_schemas import OrderCreate, OrderResponse
from app.services.order_service import OrderService


class OrderController(Controller):
    path = "/orders"

    @get("/{order_id:str}")
    async def get_order_by_id(
        self, order_service: OrderService, order_id: str
    ) -> OrderResponse:
        try:
            order_uuid = UUID(order_id)
        except ValueError:
            raise ValidationException(detail="Invalid order ID format")

        order = await order_service.get_by_id(order_uuid)
        if not order:
            raise NotFoundException(detail=f"Order with ID {order_id} not found")
        return OrderResponse.model_validate(order)

    @get("/user/{user_id:str}")
    async def get_orders_by_user(
        self, order_service: OrderService, user_id: str
    ) -> List[OrderResponse]:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise ValidationException(detail="Invalid user ID format")

        orders = await order_service.get_by_user(user_uuid)
        return [OrderResponse.model_validate(o) for o in orders]

    @post()
    async def create_order(
        self, order_service: OrderService, data: OrderCreate
    ) -> OrderResponse:
        order = await order_service.create(data)
        return OrderResponse.model_validate(order)

    @delete("/{order_id:str}")
    async def delete_order(self, order_service: OrderService, order_id: str) -> None:
        try:
            order_uuid = UUID(order_id)
        except ValueError:
            raise ValidationException(detail="Invalid order ID format")

        order = await order_service.get_by_id(order_uuid)
        if not order:
            raise NotFoundException(detail=f"Order with ID {order_id} not found")

        await order_service.delete(order_uuid)
