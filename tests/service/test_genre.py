from dao.genre import GenreDAO
from service.genre import GenreService
from dao.model.genre import Genre
from unittest.mock import MagicMock
import pytest


@pytest.fixture()
def genre_dao()->GenreDAO:
    genre_dao: GenreDAO = GenreDAO(None)

    genre_one: Genre = Genre(id=1, name='Biba')
    genre_two: Genre = Genre(id=2, name='Boba')
    new_genre: Genre = Genre(id=3, name='newcomer')
    updated_genre: Genre = Genre(id=1, name='Bobr')

    genre_dao.get_one = MagicMock(return_value=genre_one)
    genre_dao.get_all = MagicMock(return_value=[genre_one, genre_two])
    genre_dao.create = MagicMock(return_value=new_genre)
    genre_dao.update = MagicMock(return_value=updated_genre)
    genre_dao.delete = MagicMock(return_value=None)

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao: MagicMock) -> None:
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self) -> None:
        genre: Genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.name == 'Biba'
        assert genre.id == 1

    def test_get_all(self) -> None:
        genres: list = self.genre_service.get_all()
        assert genres is not None
        assert len(genres) == 2

    def test_create(self) -> None:
        new_genre: dict = {"name": "newcomer"}
        genre: Genre = self.genre_service.create(new_genre)
        assert genre.id == 3
        assert genre.name == "newcomer"

    def test_update(self) -> None:
        updated_genre: dict = {"id": 1, "name": "Bobr"}
        genre: Genre = self.genre_service.update(updated_genre,1)
        assert genre.id == 1
        assert genre.name == "Bobr"

    def test_delete(self) -> None:
        self.genre_service.delete(1)
