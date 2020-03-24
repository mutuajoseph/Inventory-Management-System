class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:wamzy@127.0.0.1:5432/charts'
    SECRET_KEY = 'some-random-key'
    JWT_SECRET_KEY = 'some-secret-key'

class ProductionConfig():
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:wamzy@127.0.0.1:5432/RMS'

