from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.database import async_session_factory

from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.address_repository import AddressRepository

from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.order_service import OrderService
from app.services.address_service import AddressService

from app.controllers.user_controller import UserController
from app.controllers.product_controller import ProductController
from app.controllers.order_controller import OrderController
from app.controllers.address_controller import AddressController


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


async def provide_product_repository(
    db_session: AsyncSession
) -> ProductRepository:
    return ProductRepository(db_session)


async def provide_order_repository(
    db_session: AsyncSession
) -> OrderRepository:
    return OrderRepository(db_session)


async def provide_address_repository(
    db_session: AsyncSession
) -> AddressRepository:
    return AddressRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)


async def provide_product_service(
    product_repository: ProductRepository
) -> ProductService:
    return ProductService(product_repository)


async def provide_order_service(
    order_repository: OrderRepository,
    product_repository: ProductRepository,
) -> OrderService:
    return OrderService(order_repository, product_repository)


async def provide_address_service(
    address_repository: AddressRepository,
) -> AddressService:
    return AddressService(address_repository)


app = Litestar(
    route_handlers=[
        UserController,
        ProductController,
        OrderController,
        AddressController,
    ],
    dependencies={
        "db_session": Provide(provide_db_session),

        "user_repository": Provide(provide_user_repository),
        "product_repository": Provide(provide_product_repository),
        "order_repository": Provide(provide_order_repository),
        "address_repository": Provide(provide_address_repository),

        "user_service": Provide(provide_user_service),
        "product_service": Provide(provide_product_service),
        "order_service": Provide(provide_order_service),
        "address_service": Provide(provide_address_service),
    },
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
