from flask import request
from flask_restx import Resource
from dao.model.genre import GenreSchema
from . import genre_ns, genre_service, genre_model, genre_input_model


@genre_ns.route('/')
class GenresView(Resource):
    @genre_ns.marshal_list_with(genre_model)
    def get(self) -> tuple[list, int]:
        """Вывести все жанры"""

        genres: list = genre_service.get_all()
        return GenreSchema(many=True).dump(genres), 200

    @genre_ns.expect(genre_input_model)
    def post(self) -> tuple[str, int, dict]:
        """Добавить жанр"""

        req_json = request.json
        new_genre = genre_service.create(req_json)
        return "201", 201, {"location": f"/genres/{new_genre.id}"}


@genre_ns.route('/<int:id>')
@genre_ns.param('id', 'Идентификатор жанра')
class GenreView(Resource):
    @genre_ns.marshal_with(genre_model)
    def get(self, id: int) -> tuple[dict, int]:
        """Вывести жанр по ид"""

        genre = genre_service.get_one(id)
        return GenreSchema().dump(genre), 200

    @genre_ns.expect(genre_input_model)
    def put(self, id: int) -> tuple[str, int]:
        """Обновить"""

        req_json = request.json
        genre_service.update(req_json, id)
        return "204", 204

    @genre_ns.expect(genre_input_model)
    def patch(self, id: int) -> tuple[str, int]:
        """Частично обновить жанр"""

        req_json = request.json
        genre_service.partially_update(req_json, id)
        return "204", 204

    def delete(self, id: int) -> tuple[str, int]:
        """Удалить жанр"""

        genre_service.delete(id)
        return "204", 204
