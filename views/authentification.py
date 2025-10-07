from flask import request
from flask_restx import Resource
from . import auth_ns, auth_service, register_model, login_model, token_model
import logging

logger = logging.getLogger(__name__)


@auth_ns.route('/register')
class RegistrationView(Resource):
    @auth_ns.expect(register_model)
    def post(self) -> tuple[str, int]:
        """Регистрация нового пользователя"""

        try:
            user = auth_service.register_user(request.json)
            logger.info("Пользователь зарегистрирован")
            return "Пользователь зарегистрирован", 201
        except ValueError as er:
            logger.error(f"Ошибка регистрации: {str(er)}")
            return f"error:{str(er)}", 400


@auth_ns.route('/login')
class LoginView(Resource):
    @auth_ns.expect(login_model)
    def post(self) -> tuple[dict, int]:
        """Аутентификация пользователя и генерация токенов"""

        try:
            data: dict = request.json
            tokens: dict = auth_service.auth_user(
                data.get("email"),
                data.get("password")
            )
            logger.info("Вход в систему выполнен успешно")
            return tokens, 201
        except ValueError as er:
            logger.error(f"Ошибка входа в систему: {str(er)}")
            return {"error": str(er)}, 401

    @auth_ns.expect(token_model)
    def put(self) -> tuple[dict, int]:
        """Обновление токенов"""

        try:
            data: dict = request.json
            tokens: dict = auth_service.refresh_tokens(data.get("refresh_token"))
            logger.info("Обновление токенов успешно выполнено")
            return tokens, 201
        except ValueError as er:
            logger.error(f"Ошибка обновления токенов: {str(er)}")
            return {"error": str(er)}, 400
