from dao.user import UserDAO
from dao.model.user import User
from flask import abort


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
            data['password'] = User.get_hash(data.get('password'))

        return self.dao.create(data)

    def update(self, data: dict, id: int) -> User:
        """Обновить пароль"""

        try:
            user: User = self.get_one(id)

            if 'password_1' not in data or 'password_2' not in data:
                raise ValueError("Необходимо предоставить текущий и новый пароль")

            if not user.check_password(data.get('password_1')):
                raise ValueError("Неверный текущий пароль")

            user.set_password(data.get('password_2'))

            return self.dao.update(user)

        except ValueError as er:
            abort(400, str(er))

    def partially_update(self, data: dict, id: int):
        """Частичное обновление пользователя"""

        user: User = self.dao.get_one(id)
        user.username = data.get("username")
        user.favorite_genre = data.get("favorite_genre")

        return self.dao.update(user)

    def delete(self, id: int) -> None:
        """Удалить"""

        self.get_one(id)
        self.dao.delete(id)
