from dao.director import DirectorDAO
from dao.model.director import Director


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, id: int) -> Director:
        """Получить режиссера по ид"""

        director: Director = self.dao.get_one(id)
        return director

    def get_all(self) -> list:
        """Получить всех режиссеров"""

        return self.dao.get_all()

    def create(self, data: dict) -> Director:
        """Создать нового режиссера"""

        return self.dao.create(data)

    def update(self, data: dict, id: int) -> Director:
        """Обновить режиссера"""

        self.get_one(id)
        return self.dao.update(data, id)

    def partially_update(self, data: dict, id: int):
        """Частично обновить режиссера"""

        director = self.dao.get_one(id)
        for key, value in data.items():
            if hasattr(director, key):
                setattr(director, key, value)
        return self.dao.update(director)

    def delete(self, id: int) -> None:
        """Удалить фильм"""

        self.get_one(id)
        self.dao.delete(id)
