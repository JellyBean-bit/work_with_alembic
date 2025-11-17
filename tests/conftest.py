import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from litestar.testing import TestClient
from app.models.base import Base
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.address_repository import AddressRepository
from main import app

TEST_DB_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Создаем event loop для тестов"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    """Двигатель базы данных для тестов"""
    engine = create_async_engine(TEST_DB_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    await engine.dispose()

@pytest.fixture
async def session(engine):
    """Сессия для каждого теста с очисткой данных после теста"""
    async_session = sessionmaker(
        engine, 
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()  

            tables_to_clear = ['orders', 'addresses', 'products', 'users']
            for table in tables_to_clear:
                await session.execute(text(f"DELETE FROM {table}"))
            
            await session.commit()

@pytest.fixture
async def user_repo(session):
    return UserRepository(session)

@pytest.fixture
async def product_repo(session):
    return ProductRepository(session)

@pytest.fixture
async def order_repo(session):
    return OrderRepository(session)

@pytest.fixture
async def address_repo(session):
    return AddressRepository(session)

@pytest.fixture
async def client():
    return TestClient(app=app)