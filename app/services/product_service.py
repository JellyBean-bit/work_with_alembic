import json
from typing import List
from uuid import UUID

from app.models.product import Product
from app.redis_client import redis_client
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schemas import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def _get_product_cache_key(self, product_id: UUID) -> str:
        return f"product:{product_id}"

    def _get_product_name_cache_key(self, name: str) -> str:
        return f"product:name:{name}"

    def _get_products_all_cache_key(self) -> str:
        return "products:all"

    async def get(self, product_id: UUID) -> Product | None:
        cache_key = self._get_product_cache_key(product_id)
        cached_data = await redis_client.get(cache_key)

        if cached_data:
            product_dict = json.loads(cached_data)
            return Product(**product_dict)

        product = await self.product_repo.get_by_id(product_id)

        if product:
            product_dict = {
                "id": str(product.id),
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "stock": product.stock,
                "status": product.status,
                "created_at": product.created_at.isoformat(),
                "updated_at": product.updated_at.isoformat(),
            }
            await redis_client.set(cache_key, json.dumps(product_dict), expire=600)

        return product

    async def get_by_filter(self, count: int, page: int, **kwargs) -> List[Product]:
        cache_key = f"products:filter:{count}:{page}:{hash(frozenset(kwargs.items()))}"
        cached_data = await redis_client.get(cache_key)

        if cached_data:
            products_list = json.loads(cached_data)
            return [Product(**p) for p in products_list]

        products = await self.product_repo.get_by_filter(count, page, **kwargs)

        if products:
            products_data = []
            for product in products:
                product_dict = {
                    "id": str(product.id),
                    "name": product.name,
                    "price": product.price,
                    "description": product.description,
                    "stock": product.stock,
                    "status": product.status,
                    "created_at": product.created_at.isoformat(),
                    "updated_at": product.updated_at.isoformat(),
                }
                products_data.append(product_dict)

            await redis_client.set(cache_key, json.dumps(products_data), expire=600)

        return products

    async def get_by_name(self, name: str) -> Product | None:
        name_cache_key = self._get_product_name_cache_key(name)
        cached_product_id = await redis_client.get(name_cache_key)

        if cached_product_id:
            return await self.get(UUID(cached_product_id))

        product = await self.product_repo.get_by_name(name)

        if product:
            await redis_client.set(name_cache_key, str(product.id), expire=600)
            await self.get(product.id)
        return product

    async def create(self, data: ProductCreate) -> Product:
        product = await self.product_repo.create(data)

        await redis_client.delete(self._get_products_all_cache_key())

        await redis_client.delete_pattern("products:filter:*")

        return product

    async def update(self, product_id: UUID, data: ProductUpdate) -> Product | None:

        old_product = await self.product_repo.get_by_id(product_id)

        product = await self.product_repo.update(product_id, data)

        if product:
            if old_product:
                await redis_client.delete(
                    self._get_product_name_cache_key(old_product.name)
                )

            await redis_client.delete(self._get_product_cache_key(product_id))

            await redis_client.delete(self._get_products_all_cache_key())

            await redis_client.delete_pattern("products:filter:*")

            if data.name and old_product and data.name != old_product.name:
                await redis_client.set(
                    self._get_product_name_cache_key(data.name),
                    str(product_id),
                    expire=600,
                )

        return product

    async def delete(self, product_id: UUID) -> None:

        product = await self.product_repo.get_by_id(product_id)

        if product:

            await redis_client.delete(self._get_product_cache_key(product_id))
            await redis_client.delete(self._get_product_name_cache_key(product.name))
            await redis_client.delete(self._get_products_all_cache_key())
            await redis_client.delete_pattern("products:filter:*")

        return await self.product_repo.delete(product_id)
