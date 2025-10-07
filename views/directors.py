from flask import request
from flask_restx import Resource
from dao.model.director import DirectorSchema
from . import director_ns, director_service, director_model, director_input_model


@director_ns.route('/')
class DirectorsView(Resource):
    @director_ns.marshal_list_with(director_model)
    def get(self) -> tuple[list, int]:
        """Вывести всех режиссеров"""

        directors: list = director_service.get_all()
        return DirectorSchema(many=True).dump(directors), 200

    @director_ns.expect(director_input_model)
    def post(self) -> tuple[str, int, dict]:
        """Добавить режиссера"""

        req_json = request.json
        new_director = director_service.create(req_json)
        return "201", 201, {"location": f"/directors/{new_director.id}"}


@director_ns.route('/<int:id>')
@director_ns.param('id', 'Идентификатор режиссера')
class DirectorView(Resource):
    @director_ns.marshal_with(director_model)
    def get(self, id: int) -> tuple[dict, int]:
        """Вывести одного режиссера по ид"""

        director = director_service.get_one(id)
        return DirectorSchema().dump(director), 200

    @director_ns.expect(director_input_model)
    def put(self, id: int) -> tuple[str, int]:
        """Обновить режиссера"""

        req_json = request.json
        director_service.update(req_json, id)
        return "204", 204

    @director_ns.expect(director_input_model)
    def patch(self, id: int) -> tuple[str, int]:
        """Частично обновить режиссера"""

        req_json = request.json
        director_service.partially_update(req_json, id)
        return "204", 204

    def delete(self, id: int) -> tuple[str, int]:
        """Удалить режиссера"""

        director_service.delete(id)
        return "204", 204