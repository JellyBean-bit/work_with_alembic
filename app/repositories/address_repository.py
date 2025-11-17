from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.address import Address
from app.schemas.address_schemas import AddressCreate, AddressUpdate


class AddressRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, address_id: UUID):
        result = await self.session.execute(select(Address).filter_by(
            id=address_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: UUID):
        result = await self.session.execute(
            select(Address).filter_by(user_id=user_id)
        )
        return result.scalars().all()

    async def create(self, data: AddressCreate):
        address = Address(**data.model_dump())
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def update(self, address_id: UUID, data: AddressUpdate):
        address = await self.get_by_id(address_id)
        if not address:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(address, field, value)

        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def delete(self, address_id: UUID):
        address = await self.get_by_id(address_id)
        if address:
            await self.session.delete(address)
            await self.session.commit()
