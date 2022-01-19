import os
from pathlib import Path


BASE_DIR = Path(__file__).parent

SECRET = os.environ.get('SECRET')


SQL_ENGINE = os.environ.get('SQL_ENGINE')
SQL_USER = os.environ.get('SQL_USER')
SQL_PASSWORD = os.environ.get('SQL_PASSWORD')
SQL_HOST = os.environ.get('SQL_HOST')
SQL_PORT = os.environ.get('SQL_PORT')
SQL_DATABASE = os.environ.get('SQL_DATABASE')