import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'movies.db')


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET = os.getenv('SECRET')
    ALGORITHM = os.getenv('ALGORITHM')
    JWT_ALGORITHM = os.getenv('ALGORITHM')
    PWD_HASH_SALT = os.getenv('PWD_HASH_SALT').encode('utf-8')
    PWD_HASH_ITERATIONS = int(os.getenv('PWD_HASH_ITERATIONS'))
