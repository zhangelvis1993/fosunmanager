import os

basedir = os.path.abspath(os.path.dirname(__file__))

class config:
    UPLOADED_XDOCS_DEST = basedir + '/uploads'
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DatabaseConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mysql+pymysql://root:123456@localhost:3306/school?charset=utf8' #mysql+pymysql://username:password@server/db
    # pymysql不会建立数据库，所以要先建好才能连接然后建表

config = {
    'default': DatabaseConfig
}

'''
class DatabaseConfig2(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'test')

class DatabaseConfig3(config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

...

config = {    
    'db1': DatabaseConfig,
    'db2': DatabaseConfig2,
    'db3': DatabaseConfig3,
}

'''