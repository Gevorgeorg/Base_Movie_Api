from marshmallow import Schema, fields

from setup_db import db


class Genre(db.Model):
    __tablename__ = 'genre'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class GenreSchema(Schema):
    id: int = fields.Int()
    name: str = fields.Str()
