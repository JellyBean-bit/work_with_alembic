from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schemas.order_schemas import OrderCreate
from app.services.order_service import OrderService


class TestOrderService:
    @pytest.mark.asyncio
    async def test_create_order_success(self):
        """Тест успешного создания заказа"""
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)

        user_id = uuid4()
        product_id = uuid4()
        address_id = uuid4()
        order_id = uuid4()

        mock_user = Mock()
        mock_user.id = user_id
        mock_user.username = "Username"
        mock_user.first_name = "Name"
        mock_user.last_name = "Last name"
        mock_user.email = "test@example.com"

        mock_product = Mock()
        mock_product.id = product_id
        mock_product.name = "Test Product"
        mock_product.price = 100.0
        mock_product.stock = 5

        mock_user_repo.get_by_id.return_value = mock_user
        mock_product_repo.get_by_id.return_value = mock_product
        mock_product_repo.update.return_value = Mock()

        mock_created_order = Mock()
        mock_created_order.id = order_id
        mock_created_order.user_id = user_id
        mock_created_order.product_id = product_id
        mock_created_order.address_id = address_id
        mock_created_order.quantity = 2
        mock_created_order.total_price = 200.0

        mock_order_repo.create.return_value = mock_created_order

        order_service = OrderService(
            order_repo=mock_order_repo,
            product_repo=mock_product_repo,
            user_repo=mock_user_repo,
        )

        order_data = OrderCreate(
            user_id=user_id, address_id=address_id, product_id=product_id, quantity=2
        )

        result = await order_service.create(order_data)

        assert result is not None
        assert result.id == order_id
        assert result.total_price == 200.0
        assert result.quantity == 2

        mock_user_repo.get_by_id.assert_called_once_with(user_id)
        mock_product_repo.get_by_id.assert_called_once_with(product_id)
        mock_product_repo.update.assert_called_once_with(product_id, {"stock": 3})
        mock_order_repo.create.assert_called_once_with(order_data, 200.0)

    @pytest.mark.asyncio
    async def test_create_order_insufficient_stock(self):
        """Тест создания заказа с недостаточным количеством товара"""
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)

        user_id = uuid4()
        product_id = uuid4()
        address_id = uuid4()

        mock_user = Mock()
        mock_user.id = user_id

        mock_product = Mock()
        mock_product.id = product_id
        mock_product.name = "Test Product"
        mock_product.price = 100.0
        mock_product.stock = 2

        mock_user_repo.get_by_id.return_value = mock_user
        mock_product_repo.get_by_id.return_value = mock_product

        order_service = OrderService(
            order_repo=mock_order_repo,
            product_repo=mock_product_repo,
            user_repo=mock_user_repo,
        )

        order_data = OrderCreate(
            user_id=user_id, address_id=address_id, product_id=product_id, quantity=5
        )

        with pytest.raises(ValueError, match="Not enough stock"):
            await order_service.create(order_data)

        mock_product_repo.update.assert_not_called()
        mock_order_repo.create.assert_not_called()

        mock_user_repo.get_by_id.assert_called_once_with(user_id)
        mock_product_repo.get_by_id.assert_called_once_with(product_id)

    @pytest.mark.asyncio
    async def test_create_order_exact_stock(self):
        """Тест создания заказа с точным количеством товара (граничный случай)"""
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)

        user_id = uuid4()
        product_id = uuid4()
        address_id = uuid4()
        order_id = uuid4()

        mock_user = Mock()
        mock_user.id = user_id

        mock_product = Mock()
        mock_product.id = product_id
        mock_product.name = "Test Product"
        mock_product.price = 50.0
        mock_product.stock = 3

        mock_user_repo.get_by_id.return_value = mock_user
        mock_product_repo.get_by_id.return_value = mock_product
        mock_product_repo.update.return_value = Mock()

        mock_created_order = Mock()
        mock_created_order.id = order_id
        mock_created_order.user_id = user_id
        mock_created_order.product_id = product_id
        mock_created_order.address_id = address_id
        mock_created_order.quantity = 3
        mock_created_order.total_price = 150.0

        mock_order_repo.create.return_value = mock_created_order

        order_service = OrderService(
            order_repo=mock_order_repo,
            product_repo=mock_product_repo,
            user_repo=mock_user_repo,
        )

        order_data = OrderCreate(
            user_id=user_id, address_id=address_id, product_id=product_id, quantity=3
        )

        result = await order_service.create(order_data)

        assert result is not None
        assert result.quantity == 3
        assert result.total_price == 150.0

        mock_user_repo.get_by_id.assert_called_once_with(user_id)
        mock_product_repo.get_by_id.assert_called_once_with(product_id)
        mock_product_repo.update.assert_called_once_with(product_id, {"stock": 0})
        mock_order_repo.create.assert_called_once_with(order_data, 150.0)
