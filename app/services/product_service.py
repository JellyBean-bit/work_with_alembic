from uuid import UUID
from typing import List

from app.repositories.product_repository import ProductRepository
from app.schemas.product_schemas import ProductCreate, ProductUpdate
from app.models.product import Product


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get(self, product_id: UUID) -> Product | None:
        return await self.product_repo.get_by_id(product_id)

    async def get_by_filter(
        self,
        count: int,
        page: int,
        **kwargs
    ) -> List[Product]:
        return await self.product_repo.get_by_filter(count, page, **kwargs)

    async def get_by_name(self, name: str) -> Product | None:
        return await self.product_repo.get_by_name(name)

    async def create(self, data: ProductCreate) -> Product:
        return await self.product_repo.create(data)

    async def update(
        self,
        product_id: UUID,
        data: ProductUpdate
    ) -> Product | None:
        return await self.product_repo.update(product_id, data)

    async def delete(self, product_id: UUID) -> None:
        return await self.product_repo.delete(product_id)
