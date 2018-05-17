from dataweb.database import *
from dataweb import db

#插入数据
#x = Tablename(attribute=value...)
#db.session.add(x)
#db.session.commit()

#查询数据
#result = Tablename.query.filter(Tablename.attribute == value).first() 精确查询，查找出第一项符合value的数据
#filter_by: 需要指定某一个值，类似于SQL语句中的where操作；filter： 可以模糊化和关系化，> < in not or等等
#result = Tablename.query.all() 查询表的全部数据

#修改数据
#result.attribute = replace_value 基于上述精确查找后的结果，用替代数据覆盖原数据
#db.session.commit()

#删除数据
#db.session.delete(result) 基于上述精确查找后的结果，刪除数据
#db.session.commit()
