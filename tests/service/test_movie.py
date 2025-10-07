from dao.movie import MovieDAO
from service.movie import MovieService
from dao.model.movie import Movie
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture()
def movie_dao() -> MovieDAO:
    with patch('dao.model.director.Director'), patch('dao.model.genre.Genre'):

        movie_dao: MovieDAO = MovieDAO(None)

        movie_one: Movie = Movie(id=1, title='Shrek', description='Shrek',
                                 trailer='https://video-preview.s3.yandex.net/GKOvWgIAAAA.mp4', year=1999, rating="R",
                                 genre_id=5, director_id=4)
        movie_two: Movie = Movie(id=2, title='Shrek 2', description='Shrek 2',
                                 trailer='https://video-preview.s3.yandex.net/pZnATQIAAAA.mp4', year=2001, rating="B",
                                 genre_id=6, director_id=5)
        new_movie: Movie = Movie(id=3, title='New', description='something', trailer='https://pronhub.com', year=2007,
                                 rating="G", genre_id=7, director_id=6)
        updated_movie: Movie = Movie(id=1, title='NewShrek', description='SuperNewShrek',
                                     trailer='https://video-preview.s3.yandex.net/GKOvWgIAAAA.mp4', year=1999, rating="R",
                                     genre_id=5, director_id=4)

        movie_dao.get_one = MagicMock(return_value=movie_one)
        movie_dao.get_all = MagicMock(return_value=[movie_one, movie_two])
        movie_dao.create = MagicMock(return_value=new_movie)
        movie_dao.update = MagicMock(return_value=updated_movie)
        movie_dao.delete = MagicMock(return_value=None)

        return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao: MagicMock) -> None:
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self) -> None:
        movie: Movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.title == 'Shrek'
        assert movie.id == 1
        assert movie.year == 1999

    def test_get_all(self) -> None:
        movies: list = self.movie_service.get_all()
        assert movies is not None
        assert len(movies) == 2

    def test_create(self) -> None:
        new_movie: dict = {"title": "New",
                           "description": "something",
                           "trailer": "https://pronhub.com",
                           "year": 2007,
                           "rating": "G",
                           "genre_id": 7,
                           "director_id": 6}
        movie: Movie = self.movie_service.create(new_movie)
        assert movie.id == 3
        assert movie.title == "New"
        assert movie.description == "something"

    def test_update(self) -> None:
        updated_movie: dict = {"title": "NewShrek",
                               "description": "SuperNewShrek",
                               "trailer": "https://video-preview.s3.yandex.net/GKOvWgIAAAA.mp4",
                               "year": 1999,
                               "rating": "R",
                               "genre_id": 5,
                               "director_id": 4}
        movie: Movie = self.movie_service.update(1,updated_movie)
        assert movie.id == 1
        assert movie.title == "NewShrek"
        assert movie.rating == "R"

    def test_delete(self) -> None:
        self.movie_service.delete(1)
