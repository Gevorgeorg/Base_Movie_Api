from flask_restx import Namespace
from dao.director import DirectorDAO
from service.director import DirectorService
from dao.genre import GenreDAO
from service.genre import GenreService
from dao.movie import MovieDAO
from service.movie import MovieService
from dao.user import UserDAO
from service.user import UserService
from setup_db import db

auth_ns: Namespace = Namespace('auth')

user_ns = Namespace('users')
user_dao = UserDAO(session=db.session)
user_service = UserService(dao=user_dao)

movie_ns = Namespace('movies')
movie_dao = MovieDAO(session=db.session)
movie_service = MovieService(dao=movie_dao)

director_ns = Namespace('directors')
director_dao = DirectorDAO(session=db.session)
director_service = DirectorService(dao=director_dao)

genre_ns = Namespace('genres')
genre_dao = GenreDAO(session=db.session)
genre_service = GenreService(dao=genre_dao)
