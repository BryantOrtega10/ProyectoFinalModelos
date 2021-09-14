class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///cine_pruebas.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cine_produccion.sqlite3'


class DevelpmentConfig(Config):
    DEBUG = True
