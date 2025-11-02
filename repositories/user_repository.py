from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from models.user import User
from schemas.user_schemas import UserCreate, UserUpdate


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(select(User).filter_by(id=user_id))
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[User]:
        stmt = select(User).filter_by(**kwargs).limit(count).offset((page - 1) * count)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> None:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        await self.session.delete(user)
        await self.session.commit()
