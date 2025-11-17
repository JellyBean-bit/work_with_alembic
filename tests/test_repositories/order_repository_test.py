import pytest
from uuid import UUID
from app.repositories.order_repository import OrderRepository
from app.schemas.order_schemas import OrderCreate


class TestOrderRepository:
    @pytest.mark.asyncio
    async def test_create_order(self, order_repo: OrderRepository):
        """Тест создания заказа"""
        user_id = UUID("12345678-1234-1234-1234-123456789abc")
        product_id = UUID("22345678-1234-1234-1234-123456789abc")
        address_id = UUID("33345678-1234-1234-1234-123456789abc")

        data = OrderCreate(
            user_id=user_id,
            product_id=product_id,
            address_id=address_id,
            quantity=2
        )

        order = await order_repo.create(data, total_price=199.98)

        assert order.id is not None
        assert order.user_id == user_id
        assert order.product_id == product_id
        assert order.address_id == address_id
        assert order.quantity == 2
        assert order.total_price == 199.98

    @pytest.mark.asyncio
    async def test_get_order_by_id(self, order_repo: OrderRepository):
        """Тест получения заказа по ID"""
        user_id = UUID("12345678-1234-1234-1234-123456789abc")
        product_id = UUID("22345678-1234-1234-1234-123456789abc")
        address_id = UUID("33345678-1234-1234-1234-123456789abc")

        order = await order_repo.create(
            OrderCreate(
                user_id=user_id,
                product_id=product_id,
                address_id=address_id,
                quantity=1
            ),
            total_price=99.99
        )

        found_order = await order_repo.get_by_id(order.id)

        assert found_order is not None
        assert found_order.id == order.id
        assert found_order.user_id == user_id
        assert found_order.product_id == product_id
        assert found_order.address_id == address_id
        assert found_order.quantity == 1
        assert found_order.total_price == 99.99

    @pytest.mark.asyncio
    async def test_get_orders_by_user(self, order_repo: OrderRepository):
        """Тест получения заказов пользователя"""
        user_id = UUID("12345678-1234-1234-1234-123456789abc")
        other_user_id = UUID("32345678-1234-1234-1234-123456789abc")
        address_id = UUID("33345678-1234-1234-1234-123456789abc")  
        other_address_id = UUID("44445678-1234-1234-1234-123456789abc")

        await order_repo.create(
            OrderCreate(
                user_id=user_id,
                product_id=UUID("11111111-1111-1111-1111-111111111111"),
                address_id=address_id,
                quantity=1
            ),
            total_price=100.0
        )
        await order_repo.create(
            OrderCreate(
                user_id=user_id,
                product_id=UUID("22222222-2222-2222-2222-222222222222"),
                address_id=address_id,
                quantity=2
            ),
            total_price=200.0
        )

        await order_repo.create(
            OrderCreate(
                user_id=other_user_id,
                product_id=UUID("33333333-3333-3333-3333-333333333333"),
                address_id=other_address_id,
                quantity=1
            ),
            total_price=50.0
        )

        user_orders = await order_repo.get_by_user(user_id)

        assert len(user_orders) == 2
        for order in user_orders:
            assert order.user_id == user_id

    @pytest.mark.asyncio
    async def test_delete_order(self, order_repo: OrderRepository):
        """Тест удаления заказа"""
        user_id = UUID("12345678-1234-1234-1234-123456789abc")
        product_id = UUID("22345678-1234-1234-1234-123456789abc")
        address_id = UUID("33345678-1234-1234-1234-123456789abc")

        order = await order_repo.create(
            OrderCreate(
                user_id=user_id,
                product_id=product_id,
                address_id=address_id,
                quantity=1
            ),
            total_price=99.99
        )

        found_order = await order_repo.get_by_id(order.id)
        assert found_order is not None

        await order_repo.delete(order.id)

        deleted_order = await order_repo.get_by_id(order.id)
        assert deleted_order is None
