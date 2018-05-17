from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, patch_request_class
import os


#单独初始化db可以防止大型项目中db被多个文件引用造成的循环引用，但会无法在视图函数以外的地方使用
'''#初始化对象
db = SQLAlchemy()

#工厂化
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app) #相当于db = SQLAlchemy(app)

    #注册蓝图
    from dataweb.admin import admin as main_blueprint
    app.register_blueprint(main_blueprint)

    return app'''

app = Flask(__name__)
app.config.from_object(config['default'])
config['default'].init_app(app)
loginmanager = LoginManager()
loginmanager.session_protection = 'strong'
loginmanager.login_view = 'main.admin_login'
loginmanager.login_message = '請先登入賬號！'
loginmanager.init_app(app)
db = SQLAlchemy(app)
xdocs = UploadSet('xdocs', DOCUMENTS)
configure_uploads(app, xdocs)
patch_request_class(app)

from dataweb.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from dataweb.main import main as main_blueprint
app.register_blueprint(main_blueprint)