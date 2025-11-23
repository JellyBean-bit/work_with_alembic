from typing import List
from uuid import UUID

from app.models.address import Address
from app.repositories.address_repository import AddressRepository
from app.schemas.address_schemas import AddressCreate, AddressUpdate


class AddressService:
    def __init__(self, address_repo: AddressRepository):
        self.address_repo = address_repo

    async def get_by_id(self, address_id: UUID) -> Address | None:
        return await self.address_repo.get_by_id(address_id)

    async def get_by_user(self, user_id: UUID) -> List[Address]:
        return await self.address_repo.get_by_user(user_id)

    async def create(self, data: AddressCreate) -> Address:
        return await self.address_repo.create(data)

    async def update(self, address_id: UUID, data: AddressUpdate) -> Address | None:
        return await self.address_repo.update(address_id, data)

    async def delete(self, address_id: UUID) -> None:
        return await self.address_repo.delete(address_id)
