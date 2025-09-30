from pydoc import pager

from flask import request
from flask_restx import Resource
from dao.model.movie import MovieSchema
from . import movie_ns, movie_service


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self) -> tuple[list, int]:
        """Вывести все фильмы"""

        page: int = request.args.get('page', type=int)
        director_id: int = request.args.get('director_id', type=int)
        genre_id: int = request.args.get('genre_id', type=int)
        status: str = request.args.get('status', "new")

        movies: list = movie_service.get_all(page, director_id, genre_id, status)
        return MovieSchema(many=True).dump(movies), 200

    def post(self) -> tuple[str, int, dict]:
        """Добавить фильм"""

        req_json = request.json
        new_movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{new_movie.id}"}


@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id: int) -> tuple[dict, int]:
        """Вывести фильм по ид"""

        movie = movie_service.get_one(id)
        return MovieSchema().dump(movie), 200

    def put(self, id: int) -> tuple[str, int]:
        """Обновить фильм"""

        req_json = request.json
        req_json["id"] = id
        movie_service.update(req_json)
        return "", 204

    def patch(self, id: int) -> tuple[str, int]:
        """Частично обновить фильм"""

        req_json = request.json
        req_json["id"] = id
        movie_service.partially_update(req_json)
        return "", 204

    def delete(self, id: int) -> tuple[str, int]:
        """Удалить фильм"""

        movie_service.delete(id)
        return "", 204
