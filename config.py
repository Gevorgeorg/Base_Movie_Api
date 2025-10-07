import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET = os.getenv('SECRET')
    ALGORITHM = os.getenv('ALGORITHM')
    JWT_ALGORITHM = os.getenv('ALGORITHM')
    PWD_HASH_SALT = os.getenv('PWD_HASH_SALT').encode('utf-8')
    PWD_HASH_ITERATIONS = int(os.getenv('PWD_HASH_ITERATIONS'))
