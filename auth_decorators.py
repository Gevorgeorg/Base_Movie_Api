from flask import request
from flask_restx import abort
import jwt
from config import Config


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data: str = request.headers.get('Authorization')
        token: str = data.split('Bearer ')[-1]
        try:
            jwt.decode(token, Config.SECRET, algorithms=Config.ALGORITHM)
        except Exception as er:
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data: str = request.headers.get('Authorization')
        token: str = data.split('Bearer ')[-1]
        try:
            user: dict = jwt.decode(token, Config.SECRET, algorithms=Config.ALGORITHM)
            role: str = user.get('role')
        except Exception as er:
            abort(401)
        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper
