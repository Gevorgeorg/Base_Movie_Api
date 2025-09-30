from dao.genre import GenreDAO
from dao.model.genre import Genre


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, id: int) -> Genre:
        """Получить один жанр по ид"""

        genre: Genre = self.dao.get_one(id)
        return genre

    def get_all(self) -> list:
        """Получить все жанры"""

        return self.dao.get_all()

    def create(self, data: dict) -> Genre:
        """Создать новый жанр"""

        return self.dao.create(data)

    def update(self, data: dict, id: int) -> Genre:
        """Обновить жанр"""

        self.get_one(id)
        return self.dao.update(data, id)

    def partially_update(self, data: dict, id: int):
        """Частично обновить"""

        genre = self.dao.get_one(id)
        for key, value in data.items():
            if hasattr(genre, key):
                setattr(genre, key, value)
        return self.dao.update(genre)

    def delete(self, id: int) -> None:
        """Удалить жанр"""

        self.get_one(id)
        self.dao.delete(id)