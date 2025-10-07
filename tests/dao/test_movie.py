from unittest.mock import MagicMock, patch
from dao.movie import MovieDAO
from dao.model.movie import Movie


class TestMovieDAO:
    def setup_method(self):

        with patch('dao.model.director.Director'), patch('dao.model.genre.Genre'):
            self.mock_session = MagicMock()
            self.dao = MovieDAO(self.mock_session)

    def test_get_one(self):

        expected_movie: Movie = Movie(id=1, title="R.R.R.")
        self.mock_session.query.return_value.get.return_value = expected_movie
        movie: Movie = self.dao.get_one(1)
        assert movie == expected_movie
        self.mock_session.query.assert_called_with(Movie)

    def test_get_all(self):

        expected_movies: list = [Movie(id=1), Movie(id=2)]
        self.mock_session.query.return_value.all.return_value = expected_movies
        movie: list = self.dao.get_all()
        assert movie == expected_movies
        self.mock_session.query.assert_called_with(Movie)

    def test_create(self):

        movie_data: dict = {"title": "Shrek"}
        movie: Movie = self.dao.create(movie_data)
        assert isinstance(movie, Movie)
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()

    def test_update(self):

        movie_to_update: Movie = Movie(id=1, title="Updating Movie", year=2020)
        movie: Movie = self.dao.update(movie_to_update)
        self.mock_session.add.assert_called_once_with(movie_to_update)
        self.mock_session.commit.assert_called_once()
        assert movie == movie_to_update

    def test_delete(self):

        movie_to_delete: Movie = Movie(id=1)
        self.mock_session.query.return_value.get.return_value = movie_to_delete
        self.dao.delete(1)
        self.mock_session.delete.assert_called_with(movie_to_delete)
        self.mock_session.commit.assert_called_once()