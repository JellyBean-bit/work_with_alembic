import pytest
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schemas import ProductCreate, ProductUpdate


class TestProductRepository:
    @pytest.mark.asyncio
    async def test_create_product(self, product_repo: ProductRepository):
        """Тест создания продукта"""
        data = ProductCreate(
            name="Test Product",
            price=99.99,
            description="Test description",
            stock=10
        )

        product = await product_repo.create(data)

        assert product.id is not None
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.description == "Test description"
        assert product.stock == 10

    @pytest.mark.asyncio
    async def test_get_product_by_id(self, product_repo: ProductRepository):
        """Тест получения продукта по ID"""
        product = await product_repo.create(
            ProductCreate(
                name="Test Product",
                price=99.99,
                description="Test description",
                stock=10
            )
        )

        found_product = await product_repo.get_by_id(product.id)

        assert found_product is not None
        assert found_product.id == product.id
        assert found_product.name == "Test Product"
        assert found_product.price == 99.99

    @pytest.mark.asyncio
    async def test_get_product_by_name(self, product_repo: ProductRepository):
        """Тест получения продукта по названию"""
        await product_repo.create(
            ProductCreate(
                name="Unique Product",
                price=50.0,
                description="Unique product",
                stock=5
            )
        )

        found_product = await product_repo.get_by_name("Unique Product")

        assert found_product is not None
        assert found_product.name == "Unique Product"
        assert found_product.price == 50.0

    @pytest.mark.asyncio
    async def test_update_product_partial(
        self,
        product_repo: ProductRepository
    ):
        """Тест обновления продукта"""
        product = await product_repo.create(
            ProductCreate(
                name="Product",
                price=100.0,
                description="Description",
                stock=20
            )
        )

        update_data = ProductUpdate(price=150.0)

        updated_product = await product_repo.update(product.id, update_data)

        assert updated_product is not None
        assert updated_product.name == "Product"
        assert updated_product.price == 150.0
        assert updated_product.description == "Description"
        assert updated_product.stock == 20

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repo: ProductRepository):
        """Тест удаления продукта"""
        product = await product_repo.create(
            ProductCreate(
                name="To Delete",
                price=10.0,
                description="To be deleted",
                stock=1
            )
        )

        found_product = await product_repo.get_by_id(product.id)
        assert found_product is not None

        await product_repo.delete(product.id)

        deleted_product = await product_repo.get_by_id(product.id)
        assert deleted_product is None

    @pytest.mark.asyncio
    async def test_get_by_filter_all_products(
        self,
        product_repo: ProductRepository
    ):
        """Тест получения всех продуктов"""
        products_data = [
            ProductCreate(name="Product 1", price=10.0, stock=5),
            ProductCreate(name="Product 2", price=20.0, stock=10),
            ProductCreate(name="Product 3", price=30.0, stock=15),
        ]

        for data in products_data:
            await product_repo.create(data)

        all_products = await product_repo.get_by_filter(count=10, page=1)

        assert len(all_products) == 3
        product_names = [p.name for p in all_products]
        assert "Product 1" in product_names
        assert "Product 2" in product_names
        assert "Product 3" in product_names
