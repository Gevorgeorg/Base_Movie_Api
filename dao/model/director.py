from setup_db import db
from marshmallow import Schema, fields, validate


class Director(db.Model):
    __tablename__ = 'director'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(55), unique=True, nullable=False)

    def __repr__(self):
        return f"<Director(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class DirectorSchema(Schema):
    id: int = fields.Int()
    name: str = fields.Str(validate=validate.Length(max=55))
