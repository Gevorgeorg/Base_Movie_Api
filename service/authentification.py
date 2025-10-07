import jwt
import datetime
import calendar
from dao.user import UserDAO
from dao.model.user import User
from config import Config
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def register_user(self, data: dict) -> User:
        """Регистрация нового пользователя"""

        email: str = data.get("email")
        password: str = data.get("password")

        if not email or not password:
            logger.error("Ошибка; Email и пароль обязательны")
            raise ValueError("Email и пароль обязательны")

        existing_user: User = self.dao.get_by_email(email)
        if existing_user:
            logger.error(f"Ошибка: Пользователь с почтой {email} уже существует")
            raise ValueError("Пользователь с таким email уже существует")
        try:
            user_data: dict = {
                "email": email,
                "password": data.get("password"),
                "username": data.get("username"),
                "role": data.get("role", "user"),
                "favorite_genre": data.get("favorite_genre"),
            }
            new_user: User = self.dao.create(user_data)
            new_user.set_password(password)
            self.dao.update(new_user)
            logger.info("Пользователь зарегистрирован")
            return new_user
        except Exception as er:
            logger.error(f"Ошибка регистрации: {str(er)}")
            raise

    def auth_user(self, email: str, password: str) -> dict:
        """Аутентификация ползователя и генерация токенов"""

        if not email or not password:
            logger.error("Ошибка: Email и пароль обязательны")
            raise ValueError("Email и пароль обязательны")

        user: User = self.dao.get_by_email(email)
        if not user or not user.check_password(password):
            logger.error("Ошибка: Неверные учётные данные")
            raise ValueError("Неверные учётные данные")

        try:
            tokens: dict = self.generate_tokens(user)
            logger.info("Пользователь успешно прошел аутентификацию")
            return tokens
        except Exception as er:
            logger.error(f"Ошибка генерации токена: {str(er)}")
            raise

    def refresh_tokens(self, refresh_token: str) -> dict:
        """Обновление токенов"""

        if not refresh_token:
            logger.error("Ошибка: Refresh token обязателен")
            raise ValueError("Refresh token обязателен")

        try:
            data: dict = jwt.decode(refresh_token, Config.SECRET, algorithms=[Config.ALGORITHM])
        except jwt.ExpiredSignatureError:
            logger.error("Refresh token истек")
            raise ValueError("Refresh token истек")
        except jwt.InvalidTokenError:
            logger.error("Невалидный refresh token")
            raise ValueError("Невалидный refresh token")

        email: str = data.get("email")
        user: User = self.dao.get_by_email(email)
        if not user:
            logger.error("Пользователь не найден")
            raise ValueError("Пользователь не найден")

        return self.generate_tokens(user)

    def generate_tokens(self, user: User) -> dict:
        """Генерация токенов"""
        try:
            data: dict = {"email": user.email, "role": user.role}

            min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            data["exp"] = calendar.timegm(min30.timetuple())
            access_token = jwt.encode(data, Config.SECRET, algorithm=Config.ALGORITHM)

            days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
            data["exp"] = calendar.timegm(days130.timetuple())
            refresh_token = jwt.encode(data, Config.SECRET, algorithm=Config.ALGORITHM)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token}
        except Exception as er:
            logger.error(f"Ошибка генерации токена: {str(er)}")
            raise