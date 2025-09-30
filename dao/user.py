from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, id: int) -> User:
        """Получить пользователя по ID"""

        return self.session.query(User).get(id)

    def get_all(self) -> list:
        """Получить всех пользователей, с возможной фильтрацией"""

        query = self.session.query(User)
        return query.all()

    def create(self, data: dict) -> User:
        """Создать нового пользователя"""

        user: User = User(**data)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user: User) -> User:
        """Обновить пользователя"""

        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, id: int) -> None:
        """Удалить пользователя"""

        user: User = self.get_one(id)
        self.session.delete(user)
        self.session.commit()
