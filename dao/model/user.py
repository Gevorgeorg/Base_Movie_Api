import hashlib
from marshmallow import Schema, fields
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(100), unique=True, nullable=False)
    password: str = db.Column(db.String(20), nullable=False)
    role: str = db.Column(db.String(20), nullable=False)
    email: str = db.Column(db.String(30), unique=True, nullable=False)
    favorite_genre: str = db.Column(db.String(30))

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

    def __str__(self):
        return self.username

    @staticmethod
    def get_hash(password:str) -> str:
        """Хешировать пароль"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).hex()

    def set_password(self, password:str) -> None:
        """Установить хешированный пароль"""

        self.password = self.get_hash(password)

    def check_password(self, password:str) -> bool:
        """Проверить пароль"""

        return self.password == self.get_hash(password)


class UserSchema(Schema):
    id: int = fields.Int()
    username: str = fields.Str()
    password: str = fields.Str(load_only=True)
    role: str = fields.Str()
    email: str = fields.Str()
    favorite_genre: str = fields.Str()
