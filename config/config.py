class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:wamzy@127.0.0.1:5432/charts'
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    JWT_SECRET_KEY = 'some-secret-key'

class ProductionConfig():
    SQLALCHEMY_DATABASE_URI = 'postgres://pcdqdnreapwvmm:15b3f90225665ba6512e182b97863bdbcbcc574503e03622ce856f573439aacd@ec2-54-159-112-44.compute-1.amazonaws.com:5432/d848k7580t8pdn'
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

