from dao.user import UserDAO
from dao.model.user import User


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, id: int) -> User:
        """Получить пользователя по ID"""

        user: User = self.dao.get_one(id)
        return user

    def get_all(self) -> list:
        """Получить всех пользователей"""

        return self.dao.get_all()

    def create(self, data: dict) -> User:
        """Добавить нового пользователя с хешированием пароля"""

        if 'password' in data:
            data['password'] = User.get_hash(data['password'])

        return self.dao.create(data)

    def update(self, id: int, data: dict) -> User:
        """Обновить информацию о пользователе"""

        user = self.get_one(id)

        for key, value in data.items():
            if hasattr(user, key) and key != 'id':
                if key == 'password':
                    value = User().get_hash(value)
                setattr(user, key, value)

        return self.dao.update(user)

    def partially_update(self, data: dict, id: int):
        """Частичное обновление пользователя"""

        user = self.dao.get_one(id)
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return self.dao.update(user)

    def delete(self, id: int) -> None:
        """Удалить"""

        self.get_one(id)
        self.dao.delete(id)

