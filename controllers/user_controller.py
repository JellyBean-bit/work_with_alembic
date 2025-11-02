from litestar import Controller, get, post, delete, put
from litestar.di import Provide
from litestar.exceptions import NotFoundException, ValidationException
from typing import List
from uuid import UUID

from services.user_service import UserService
from schemas.user_schemas import UserCreate, UserResponse, UserUpdate


class UserController(Controller):
    path = "/users"

    @get("/{user_id:str}")
    async def get_user_by_id(
        self, user_service: UserService, user_id: str
    ) -> UserResponse:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise ValidationException(detail="Invalid user ID format")

        user = await user_service.get_by_id(user_uuid)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(self, user_service: UserService) -> List[UserResponse]:
        users = await user_service.get_by_filter(count=100, page=1)
        return [UserResponse.model_validate(u) for u in users]

    @post()
    async def create_user(self, user_service: UserService, data: UserCreate) -> UserResponse:
        user = await user_service.create(data)
        return UserResponse.model_validate(user)

    @delete("/{user_id:str}")
    async def delete_user(self, user_service: UserService, user_id: str) -> None:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise ValidationException(detail="Invalid user ID format")

        user = await user_service.get_by_id(user_uuid)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

        await user_service.delete(user_uuid)

    @put("/{user_id:str}")
    async def update_user(
        self, user_service: UserService, user_id: str, data: UserUpdate
    ) -> UserResponse:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise ValidationException(detail="Invalid user ID format")

        user = await user_service.update(user_uuid, data)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

        return UserResponse.model_validate(user)
