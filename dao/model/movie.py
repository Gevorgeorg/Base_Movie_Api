from marshmallow import Schema, fields, validate
from setup_db import db


class Movie(db.Model):
    __tablename__ = 'movie'
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(50), nullable=False)
    description: str = db.Column(db.String(255))
    trailer: str = db.Column(db.String(255))
    year: int = db.Column(db.Integer)
    rating: str = db.Column(db.String(7))
    genre_id: int = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre", foreign_keys=[genre_id])
    director_id: int = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director", foreign_keys=[director_id])

    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}')>"

    def __str__(self):
        return self.title


class MovieSchema(Schema):
    id: int = fields.Integer()
    title: str = fields.String(validate=validate.Length(max=50))
    description: str = fields.String(validate=validate.Length(max=255))
    trailer: str = fields.String(validate=validate.Length(max=255))
    year: int = fields.Integer()
    rating: str = fields.String(validate=validate.Length(max=7))
    genre: str = fields.String(attribute="genre.name")
    genre_id: int = fields.Integer(attribute="genre_id")
    director_id: int = fields.Integer(attribute="director.id")
    director: str = fields.String(attribute="director.name")
