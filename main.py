from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from controllers.user_controller import UserController
from repositories.user_repository import UserRepository
from services.user_service import UserService
from database import async_session_factory


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()  


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)


app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
