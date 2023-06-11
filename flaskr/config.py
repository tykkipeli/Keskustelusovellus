import os

env = os.getenv('FLASK_ENV', 'production')
if env == 'development':
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
else:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('://', 'ql://', 1)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY')
