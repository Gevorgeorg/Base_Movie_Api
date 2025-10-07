from flask_restx import Namespace, fields
from dao.director import DirectorDAO
from service.authentification import AuthService
from service.director import DirectorService
from dao.genre import GenreDAO
from service.genre import GenreService
from dao.movie import MovieDAO
from service.movie import MovieService
from dao.user import UserDAO
from service.user import UserService
from setup_db import db

user_ns = Namespace('users', description='Операции по управлению пользователями')
user_model = user_ns.model('User', {
    'id': fields.Integer(readOnly=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'role': fields.String(description='User role'),
    'email': fields.String(required=True, description='User email'),
    'favorite_genre': fields.String(description='User favorite genre'),})
user_input_model = user_ns.model('UserInput', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='User password'),
    'role': fields.String(description='User role'),
    'email': fields.String(required=True, description='User email'),
    'favorite_genre': fields.String(description='User favorite genre'),})
user_dao = UserDAO(session=db.session)
user_service = UserService(dao=user_dao)

movie_ns = Namespace('movies', description='Операции с фильмами')
movie_model = movie_ns.model('Movie', {
    'id': fields.Integer(readOnly=True, description='Movie ID'),
    'title': fields.String(required=True, description='Movie title'),
    'description': fields.String(description='Movie description'),
    'trailer': fields.String(description='Movie trailer URL'),
    'year': fields.Integer(description='Release year'),
    'rating': fields.String(description='Rating'),
    'genre': fields.String(description='Genre name'),
    'genre_id': fields.Integer(description='Genre ID'),
    'director': fields.String(description='Director name'),
    'director_id': fields.Integer(description='Director ID')})
movie_input_model = movie_ns.model('MovieInput', {
    'title': fields.String(required=True, description='Movie title'),
    'description': fields.String(description='Movie description'),
    'trailer': fields.String(description='Movie trailer URL'),
    'year': fields.Integer(description='Release year'),
    'rating': fields.String(description='Rating'),
    'genre_id': fields.Integer(description='Genre ID'),
    'director_id': fields.Integer(description='Director ID')})
movie_dao = MovieDAO(session=db.session)
movie_service = MovieService(dao=movie_dao)

director_ns = Namespace('directors', description='Операции с режиссерами')
director_model = director_ns.model('Director', {
    'id': fields.Integer(readOnly=True, description='Director ID'),
    'name': fields.String(required=True, description='Director name')})
director_input_model = director_ns.model('DirectorInput', {
    'name': fields.String(required=True, description='Director name')})
director_dao = DirectorDAO(session=db.session)
director_service = DirectorService(dao=director_dao)

genre_ns = Namespace('genres', description='Операции с жанрами')
genre_model = genre_ns.model('Genre', {
    'id': fields.Integer(readOnly=True, description='Genre ID'),
    'name': fields.String(required=True, description='Genre name')})
genre_input_model = genre_ns.model('GenreInput', {
    'name': fields.String(required=True, description='Genre name')})
genre_dao = GenreDAO(session=db.session)
genre_service = GenreService(dao=genre_dao)

auth_ns = Namespace('auth', description='Операции аутентификации')
login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')})
register_model = auth_ns.model('Register', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')})
token_model = auth_ns.model('Token', {
    'access_token': fields.String(description='JWT Access Token'),
    'refresh_token': fields.String(description='JWT Refresh Token')})
auth_service = AuthService(dao=user_dao)
