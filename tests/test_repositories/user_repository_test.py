import pytest
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repo: UserRepository):
        """Тест создания пользователя в репозитории"""
        data = UserCreate(
            username="john",
            email="john@example.com",
            first_name="first name",
            last_name="last name",
            description="test user"
        )

        user = await user_repo.create(data)

        assert user.id is not None
        assert user.username == "john"
        assert user.email == "john@example.com"
        assert user.first_name == "first name"
        assert user.last_name == "last name"
        assert user.description == "test user"

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, user_repo: UserRepository):
        """Тест получения пользователя по email"""
        user_data = UserCreate( 
            username="test",
            email="test@example.com",
            first_name="first name",
            last_name="last name",
            description="test user"
        )
        user = await user_repo.create(user_data)

        found_user = await user_repo.get_by_email("test@example.com")

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == "test@example.com"
        assert found_user.first_name == "first name"
        assert found_user.last_name == "last name"
        assert found_user.description == "test user"

    @pytest.mark.asyncio
    async def test_update_user(self, user_repo: UserRepository):
        """Тест обновления пользователя"""
        user_data = UserCreate(
            username="unique",
            email="unique@example.com",
            first_name="first name",
            last_name="last name",
            description="unique user"
        )
        user = await user_repo.create(user_data)

        update_data = UserUpdate(
            description="new description"
        )
        updated_user = await user_repo.update(
            user.id,
            update_data
        )

        assert updated_user is not None
        assert updated_user.username == "unique"
        assert updated_user.email == "unique@example.com"
        assert updated_user.first_name == "first name"
        assert updated_user.last_name == "last name"
        assert updated_user.description == "new description"
      
    @pytest.mark.asyncio
    async def test_delete_user(self, user_repo: UserRepository):
        """Тест удаления пользователя"""
        user = await user_repo.create(
            UserCreate(
                username="todelete",
                email="delete@example.com",
                first_name="first name",
                last_name="last name",
                description="to be deleted"
            )
        )
       
        found_user = await user_repo.get_by_id(user.id)
        assert found_user is not None

        await user_repo.delete(user.id)

        deleted_user = await user_repo.get_by_id(user.id)
        assert deleted_user is None

    @pytest.mark.asyncio
    async def test_get_by_filter_all_users(self, user_repo: UserRepository):
        """Тест получения всех пользователей"""
        users_data = [
            UserCreate(
                username="user1",
                email="user1@example.com",
                first_name="First1",
                last_name="Last1",
                description="User 1"
            ),
            UserCreate(
                username="user2",
                email="user2@example.com",
                first_name="First2",
                last_name="Last2",
                description="User 2"
            ),
            UserCreate(
                username="user3",
                email="user3@example.com",
                first_name="First3",
                last_name="Last3",
                description="User 3"
            )
        ]

        created_users = []
        for data in users_data:
            user = await user_repo.create(data)
            created_users.append(user)

        all_users = await user_repo.get_by_filter(count=10, page=1)

        assert len(all_users) == 3

        usernames = [user.username for user in all_users]
        assert "user1" in usernames
        assert "user2" in usernames
        assert "user3" in usernames