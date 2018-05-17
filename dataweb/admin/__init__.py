from flask import Blueprint
#实例化 Blueprint 类，两个参数分别为蓝本的名字和蓝本所在包或模块，第二个通常填 __name__ 即可
admin = Blueprint('admin', __name__)

#要在本文件内导入蓝图的模板py文件否则不会显示配置
from dataweb.admin import adminpy