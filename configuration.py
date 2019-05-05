class Config(object):
    DEBUG = False
    TESTING = False
    FLASK_CONFIG = 'production'
    SECRET_KEY = 'SECRET_KEY'
    SECURITY_PASSWORD_SALT = 'LONG_BIG_PASSWORD_SALT_VERY_SALTED'
    WTF_CSRF_SECRET_KEY = 'SOME_SECRET_KEY'

    SQLALCHEMY_DATABASE_URI = 'mysql://address_to_the_databease'
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '465'
    #MAIL_USE_TLS = 'False'
    MAIL_USE_SSL = 'True'
    MAIL_USERNAME = 'email'
    MAIL_PASSWORD = 'email_password'
    MAIL_DEFAULT_SENDER = 'default_sender'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://address_to_the_databease'

class TestingConfig(Config):
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
