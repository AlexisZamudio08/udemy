#This is a config file taken by the flask main app.
from dotenv import load_dotenv
import os

from gevent import config

load_dotenv('../.venv')

#This key is used to encrypt the session data is needed.
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    DEBUG = True
    #UPLOADS = "PATH_TO_UPLOADS_DEV"
    SESSION_COOKIE_SECURE = False

    
class TestingConfig(Config):
    TESTING = True
    #UPLOADS = "PATH_TO_UPLOADS_TEST"

class ProductionConfig(Config):
    DEBUG = False
    #UPLOADS = "PATH_TO_UPLOADS_PROD"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

