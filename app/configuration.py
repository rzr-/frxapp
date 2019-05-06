import os

class Config(object):
    DEBUG = False
    TESTING = False
    FLASK_CONFIG = 'production'
    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_PASSWORD_SALT = os.environ['LONG_BIG_PASSWORD_SALT_VERY_SALTED']
    WTF_CSRF_SECRET_KEY = os.environ['SOME_SECRET_KEY']

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    #MAIL_USE_TLS = 'False'
    MAIL_USE_SSL = 'True'
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class TestingConfig(Config):
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
