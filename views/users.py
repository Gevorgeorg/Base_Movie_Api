from flask import request
from flask_restx import Resource
from auth_decorators import auth_required, admin_required
from dao.model.user import UserSchema
from . import user_ns, user_service


@user_ns.route('/')
class UsersView(Resource):

    def get(self) -> tuple[list, int]:
        """Вывести всех пользователей"""

        users: list = user_service.get_all()
        result = UserSchema(many=True).dump(users)
        return result, 200

    def post(self) -> tuple[str, int, dict]:
        """Добавить пользователя"""

        req_json = request.json
        new_user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{new_user.id}"}


@user_ns.route('/<int:id>')
class UserView(Resource):

    @auth_required
    def get(self, id: int) -> tuple[dict, int]:
        """Вывести пользователя по ид"""

        user = user_service.get_one(id)
        result = UserSchema().dump(user)
        return result, 200

    @admin_required
    def put(self, id: int) -> tuple[str, int]:
        """Обновить пользователя"""

        req_json = request.json
        user_service.update(id, req_json)
        return "", 204

    @admin_required
    def patch(self, id: int) -> tuple[str, int]:
        """Частично обновить"""

        req_json = request.json
        user_service.partially_update(id, req_json)
        return "", 204

    @admin_required
    def delete(self, id: int) -> tuple[str, int]:
        """Удалить пользователя"""

        user_service.delete(id)
        return "", 204
