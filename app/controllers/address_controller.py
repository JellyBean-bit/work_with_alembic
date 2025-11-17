from litestar import Controller, get, post, delete, put
from litestar.exceptions import NotFoundException, ValidationException
from typing import List
from uuid import UUID

from app.services.address_service import AddressService
from app.schemas.address_schemas import (
    AddressCreate,
    AddressResponse,
    AddressUpdate
)


class AddressController(Controller):
    path = "/addresses"

    @get("/{address_id:str}")
    async def get_address_by_id(
        self, address_service: AddressService, address_id: str
    ) -> AddressResponse:
        try:
            address_uuid = UUID(address_id)
        except ValueError:
            raise ValidationException(detail="Invalid address ID format")

        address = await address_service.get_by_id(address_uuid)
        if not address:
            raise NotFoundException(
                detail=f"Address with ID {address_id} not found"
            )
        return AddressResponse.model_validate(address)

    @get("/user/{user_id:str}")
    async def get_addresses_by_user(
        self, address_service: AddressService, user_id: str
    ) -> List[AddressResponse]:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise ValidationException(detail="Invalid user ID format")

        addresses = await address_service.get_by_user(user_uuid)
        return [AddressResponse.model_validate(a) for a in addresses]

    @post()
    async def create_address(
        self, address_service: AddressService, data: AddressCreate
    ) -> AddressResponse:
        address = await address_service.create(data)
        return AddressResponse.model_validate(address)

    @delete("/{address_id:str}")
    async def delete_address(
        self,
        address_service: AddressService,
        address_id: str
    ) -> None:
        try:
            address_uuid = UUID(address_id)
        except ValueError:
            raise ValidationException(detail="Invalid address ID format")

        address = await address_service.get_by_id(address_uuid)
        if not address:
            raise NotFoundException(
                detail=f"Address with ID {address_id} not found"
            )

        await address_service.delete(address_uuid)

    @put("/{address_id:str}")
    async def update_address(
        self,
        address_service: AddressService,
        address_id: str,
        data: AddressUpdate
    ) -> AddressResponse:
        try:
            address_uuid = UUID(address_id)
        except ValueError:
            raise ValidationException(detail="Invalid address ID format")

        address = await address_service.update(address_uuid, data)
        if not address:
            raise NotFoundException(
                detail=f"Address with ID {address_id} not found"
            )

        return AddressResponse.model_validate(address)
