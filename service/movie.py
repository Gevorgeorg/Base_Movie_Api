from dao.movie import MovieDAO
from dao.model.movie import Movie


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, id: int) -> Movie:
        """Получить один фильм по ID"""

        movie: Movie = self.dao.get_one(id)
        return movie

    def get_all(self, page=None, director_id=None, genre_id=None, status=None) -> list:
        """Получить все фильмы с возможной фильтрацией"""

        return self.dao.get_all(page, director_id, genre_id, status)

    def create(self, data: dict) -> Movie:
        """Создать новый фильм"""

        return self.dao.create(data)

    def update(self, data: dict, id: int) -> Movie:
        """Обновить фильм"""

        self.get_one(id)
        return self.dao.update(data, id)

    def partially_update(self, data: dict, id: int):
        """Частично обновить информацию о фильме"""

        movie = self.dao.get_one(id)
        for key, value in data.items():
            if hasattr(movie, key):
                setattr(movie, key, value)
        return self.dao.update(movie)

    def delete(self, id: int) -> None:
        """Удалить фильм"""

        self.get_one(id)
        self.dao.delete(id)
