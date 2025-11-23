from typing import List
from uuid import UUID

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_by_email(email)

    async def get_by_filter(self, count: int, page: int, **kwargs) -> List[User]:
        return await self.user_repository.get_by_filter(count, page, **kwargs)

    async def create(self, data: UserCreate) -> User:
        return await self.user_repository.create(data)

    async def update(self, user_id: UUID, data: UserUpdate) -> User | None:
        return await self.user_repository.update(user_id, data)

    async def delete(self, user_id: UUID) -> None:
        return await self.user_repository.delete(user_id)
