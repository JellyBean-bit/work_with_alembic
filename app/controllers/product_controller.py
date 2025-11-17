from litestar import Controller, get, post, delete, put
from litestar.exceptions import NotFoundException, ValidationException
from typing import List
from uuid import UUID

from app.services.product_service import ProductService
from app.schemas.product_schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)


class ProductController(Controller):
    path = "/products"

    @get("/id/{product_id:str}")
    async def get_product_by_id(
        self, product_service: ProductService, product_id: str
    ) -> ProductResponse:
        try:
            product_uuid = UUID(product_id)
        except ValueError:
            raise ValidationException(detail="Invalid product ID format")

        product = await product_service.get(product_uuid)
        if not product:
            raise NotFoundException(
                detail=f"Product with ID {product_id} not found"
            )
        return ProductResponse.model_validate(product)
    
    @get("/name/{name:str}")
    async def get_product_by_name(
        self, product_service: ProductService, name: str
    ) -> ProductResponse:
        product = await product_service.get_by_name(name)
        if not product:
            raise NotFoundException(
                detail=f"Product with name {name} not found"
            )
        return ProductResponse.model_validate(product)

    @get()
    async def get_products(
        self,
        product_service: ProductService
    ) -> List[ProductResponse]:
        products = await product_service.get_by_filter(count=100, page=1)
        return [ProductResponse.model_validate(p) for p in products]

    @post()
    async def create_product(
        self, product_service: ProductService, data: ProductCreate
    ) -> ProductResponse:
        product = await product_service.create(data)
        return ProductResponse.model_validate(product)

    @delete("/{product_id:str}")
    async def delete_product(
        self,
        product_service: ProductService,
        product_id: str
    ) -> None:
        try:
            product_uuid = UUID(product_id)
        except ValueError:
            raise ValidationException(detail="Invalid product ID format")

        product = await product_service.get(product_uuid)
        if not product:
            raise NotFoundException(
                detail=f"Product with ID {product_id} not found"
            )

        await product_service.delete(product_uuid)

    @put("/{product_id:str}")
    async def update_product(
        self,
        product_service: ProductService,
        product_id: str,
        data: ProductUpdate
    ) -> ProductResponse:
        try:
            product_uuid = UUID(product_id)
        except ValueError:
            raise ValidationException(detail="Invalid product ID format")

        product = await product_service.update(product_uuid, data)
        if not product:
            raise NotFoundException(
                detail=f"Product with ID {product_id} not found"
            )

        return ProductResponse.model_validate(product)
