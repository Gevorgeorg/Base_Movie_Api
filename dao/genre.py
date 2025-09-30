from dao.model.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, id: int) -> Genre:
        """Получить один жанр по ид"""

        return self.session.query(Genre).get(id)

    def get_all(self) -> list:
        """Получить все жанры"""

        return self.session.query(Genre).all()

    def create(self, data: dict) -> Genre:
        """Добавить новый жанр"""

        new: Genre = Genre(**data)
        self.session.add(new)
        self.session.commit()
        return new

    def update(self, genre: Genre) -> Genre:
        """Обновить информацию о жанре"""

        self.session.add(genre)
        self.session.commit()
        return genre

    def delete(self, id: int) -> None:
        """Удалить жанр"""

        genre: Genre = self.get_one(id)
        self.session.delete(genre)
        self.session.commit()
