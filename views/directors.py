from flask import request
from flask_restx import Resource
from dao.model.director import DirectorSchema
from . import director_ns, director_service


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self) -> tuple[list, int]:
        """Вывести всех режиссеров"""

        directors: list = director_service.get_all()
        return DirectorSchema(many=True).dump(directors), 200

    def post(self) -> tuple[str, int, dict]:
        """Добавить режиссера"""

        req_json = request.json
        new_director = director_service.create(req_json)
        return "", 201, {"location": f"/directors/{new_director.id}"}


@director_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id: int) -> tuple[dict, int]:
        """Вывести одного режиссера по ид"""

        director = director_service.get_one(id)
        return DirectorSchema().dump(director), 200

    def put(self, id: int) -> tuple[str, int]:
        """Обновить режиссера"""

        req_json = request.json
        req_json["id"] = id
        director_service.update(req_json)
        return "", 204

    def patch(self, id: int) -> tuple[str, int]:
        """Частично обновить режиссера"""

        req_json = request.json
        req_json["id"] = id
        director_service.partially_update(req_json)
        return "", 204

    def delete(self, id: int) -> tuple[str, int]:
        """Удалить режиссера"""

        director_service.delete(id)
        return "", 204
