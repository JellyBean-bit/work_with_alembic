import json
from typing import List
from uuid import UUID

from app.models.user import User
from app.redis_client import redis_client
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _get_user_cache_key(self, user_id: UUID) -> str:
        return f"user:{user_id}"

    def _get_user_email_cache_key(self, email: str) -> str:
        return f"user:email:{email}"

    def _get_all_users_cache_key(self) -> str:
        return "users:all"

    async def get_by_id(self, user_id: UUID) -> User | None:
        cache_key = self._get_user_cache_key(user_id)
        cached_data = await redis_client.get(cache_key)

        if cached_data:
            user_dict = json.loads(cached_data)
            return User(**user_dict)

        user = await self.user_repository.get_by_id(user_id)

        if user:
            user_dict = {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "description": user.description,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            }
            await redis_client.set(cache_key, json.dumps(user_dict), expire=3600)

        return user

    async def get_by_email(self, email: str) -> User | None:
        email_cache_key = self._get_user_email_cache_key(email)
        cached_user_id = await redis_client.get(email_cache_key)

        if cached_user_id:
            return await self.get_by_id(UUID(cached_user_id))

        user = await self.user_repository.get_by_email(email)

        if user:
            await redis_client.set(email_cache_key, str(user.id), expire=3600)
            await self.get_by_id(user.id)

        return user

    async def get_by_filter(self, count: int, page: int, **kwargs) -> List[User]:
        return await self.user_repository.get_by_filter(count, page, **kwargs)

    async def create(self, data: UserCreate) -> User:
        user = await self.user_repository.create(data)

        await redis_client.delete(self._get_all_users_cache_key())

        return user

    async def update(self, user_id: UUID, data: UserUpdate) -> User | None:
        old_user = await self.user_repository.get_by_id(user_id)

        user = await self.user_repository.update(user_id, data)

        if user:
            if old_user:
                await redis_client.delete(
                    self._get_user_email_cache_key(old_user.email)
                )

            await redis_client.delete(self._get_user_cache_key(user_id))

            await redis_client.delete(self._get_all_users_cache_key())

            if data.email and old_user and data.email != old_user.email:
                await redis_client.set(
                    self._get_user_email_cache_key(data.email),
                    str(user_id),
                    expire=3600,
                )

        return user

    async def delete(self, user_id: UUID) -> None:
        user = await self.user_repository.get_by_id(user_id)

        if user:
            await redis_client.delete(self._get_user_cache_key(user_id))
            await redis_client.delete(self._get_user_email_cache_key(user.email))
            await redis_client.delete(self._get_all_users_cache_key())

        return await self.user_repository.delete(user_id)
