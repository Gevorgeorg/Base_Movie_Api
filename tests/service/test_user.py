from dao.user import UserDAO
from service.user import UserService
from dao.model.user import User
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture()
def user_dao() -> UserDAO:
    user_dao: UserDAO = UserDAO(None)

    user_one: User = User(
        id=1, username='Vovan', password='hashed_password_1',
        role='user', email='Vovan@mail.ru', favorite_genre='comedy'
    )
    user_two: User = User(
        id=2, username='Ivan', password='hashed_password_2',
        role='admin', email='Ivan@google.com', favorite_genre='drama'
    )
    new_user: User = User(
        id=3, username='new_user', password='hashed_password_3',
        role='user', email='newuser@mail.ru', favorite_genre='comedy'
    )
    updated_user: User = User(
        id=1, username='updated_user', password='new_password',
        role='user', email='updated@google.com', favorite_genre='drama'
    )

    user_dao.get_one = MagicMock(return_value=user_one)
    user_dao.get_all = MagicMock(return_value=[user_one, user_two])
    user_dao.create = MagicMock(return_value=new_user)
    user_dao.update = MagicMock(return_value=updated_user)
    user_dao.delete = MagicMock(return_value=None)
    user_one.check_password = MagicMock(return_value=True)
    user_two.check_password = MagicMock(return_value=True)
    return user_dao


class TestUserService:
    @pytest.fixture(autouse=True)
    def user_service(self, user_dao: MagicMock) -> None:
        self.user_service = UserService(dao=user_dao)

    def test_get_one(self) -> None:
        user: User = self.user_service.get_one(1)
        assert user is not None
        assert user.username == 'Vovan'
        assert user.id == 1
        assert user.email == 'Vovan@mail.ru'
        assert user.role == 'user'

    def test_get_all(self) -> None:
        users: list = self.user_service.get_all()
        assert users is not None
        assert len(users) == 2
        assert users[0].username == 'Vovan'
        assert users[1].username == 'Ivan'

    def test_create(self) -> None:
        new_user: dict = {
            "username": "new_user",
            "password": "test_password",
            "role": "user",
            "email": "newuser@mail.ru",
            "favorite_genre": "comedy"
        }
        user: User = self.user_service.create(new_user)
        assert user.id == 3
        assert user.username == "new_user"
        assert user.email == "newuser@mail.ru"

    def test_update(self) -> None:
        password_data: dict = {
            "password_1": "old_password",
            "password_2": "new_password"
        }
        user: User = self.user_service.update(password_data, 1)
        assert user.id == 1
        assert user.password == password_data.get("password_2")

    def test_partially_update(self) -> None:
        updated_user: dict = {
            "username": "updated_user",
            "favorite_genre": "drama"
        }
        user: User = self.user_service.partially_update(updated_user, 1)
        assert user.id == 1
        assert user.username == "updated_user"
        assert user.favorite_genre == "drama"

    def test_delete(self) -> None:
        self.user_service.delete(1)
