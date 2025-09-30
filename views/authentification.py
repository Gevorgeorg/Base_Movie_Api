from flask import request
from flask_restx import Resource
import jwt
import datetime
import calendar
from dao.model.user import User
from setup_db import db
from flask import abort
from constants import SECRET, ALGORITHM
from . import auth_ns


@auth_ns.route('/register')
class RegistrationView(Resource):
    def post(self) -> tuple[str, int]:
        """Регистрация нового пользователя"""

        req_json = request.json
        email: str = req_json.get("email", None)
        password: str = req_json.get("password", None)

        if None in [email, password]:
            abort(400, "Email и пароль обязательны")

        user: User = db.session.query(User).filter(User.email == email).first()
        if user:
            return "Пользователь с таким email уже существует", 400

        new_user: User = User(
            email=email,
            password=password,
            username=req_json.get("username", None),
            role=req_json.get("role", None),
            favorite_genre=req_json.get("favorite_genre", None),
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return "Пользователь зарегистрирован", 201

    @auth_ns.route('/login')
    class LoginView(Resource):
        def post(self) -> tuple[dict, int]:
            """Аутентификация пользователя и генерация токенов"""

            req_json = request.json
            email: str = req_json.get("email", None)
            password: str = req_json.get("password", None)

            if None in [email, password]:
                abort(400, "Email и пароль обязательны")

            user: User = db.session.query(User).filter(User.email == email).first()

            if user is None:
                return {"error": "Неверные учётные данные"}, 401

            if not user.check_password(password):
                return {"error": "Неверные учётные данные"}, 401

            data: dict = {"email": user.email, "role": user.role}

            min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            data["exp"] = calendar.timegm(min30.timetuple())
            access_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)

            days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
            data["exp"] = calendar.timegm(days130.timetuple())
            refresh_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)

            tokens: dict = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return tokens, 201

        def put(self) -> tuple[dict, int]:
            """Обновление токенов"""

            req_json = request.json
            refresh_token = req_json.get("refresh_token")
            if refresh_token is None:
                abort(400, "Refresh token обязателен")

            try:
                data: dict = jwt.decode(jwt=refresh_token, key=SECRET, algorithms=ALGORITHM)
            except Exception as er:
                abort(400, "Невалидный refresh token")

            email: str = data.get("email")

            user: User = db.session.query(User).filter(User.email == email).first()
            if user is None:
                abort(400, "Пользователь не найден")

            data: dict = {"email": user.email, "role": user.role}

            min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            data["exp"] = calendar.timegm(min30.timetuple())
            access_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)

            days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
            data["exp"] = calendar.timegm(days130.timetuple())
            refresh_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)

            tokens: dict = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return tokens, 201
