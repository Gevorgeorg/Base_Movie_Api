from flask import Flask, render_template
from flask_restx import Api, cors
from flask_cors import CORS

from config import Config
from setup_db import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns
from views.authentification import auth_ns

api = Api(
    title="Flask Course Project 3",
    doc="/docs",
    description="API для управления фильмами"
)


def create_app() -> Flask:
    app = Flask(__name__, static_folder='static', template_folder='templates')
    CORS(app)
    app.config.from_object(Config)

    @app.route('/')
    def index():
        """Главная страница"""

        return render_template('index.html')

    register_extensions(app)
    return app


def register_extensions(app) -> None:
    db.init_app(app)
    with app.app_context():
        db.create_all()

    api.init_app(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


app = create_app()

if __name__ == '__main__':
    app.run(port=25000, debug=True)
