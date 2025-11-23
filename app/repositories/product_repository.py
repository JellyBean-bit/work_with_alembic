from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product_schemas import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: UUID) -> Product | None:
        result = await self.session.execute(select(Product).filter_by(id=product_id))
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int, page: int, **kwargs):
        stmt = (
            select(Product).filter_by(**kwargs).limit(count).offset((page - 1) * count)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_name(self, name: str):
        stmt = select(Product).filter(Product.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update(self, product_id: UUID, data: ProductUpdate):
        product = await self.get_by_id(product_id)
        if not product:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product_id: UUID):
        product = await self.get_by_id(product_id)
        if not product:
            return None

        await self.session.delete(product)
        await self.session.commit()
