import os
from datetime import datetime
from datetime import timedelta

class Config():
    DEBUG = True
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///library.db" 
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "secretkey"
    JWT_SECRET_KEY = 'your-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    CACHE_TYPE =  'simple'
    