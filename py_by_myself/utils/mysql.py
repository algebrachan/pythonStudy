from sqlalchemy import create_engine  # 建立数据库引擎
from sqlalchemy.orm import sessionmaker,scoped_session  # 建立回话session
from models.models import Base
import time
from datetime import datetime, date

# mysql配置
# db_user = 'furnace'
# db_pwd = 'furnace123456'
# db_host = '127.0.0.1'
# db_port = '3306'
# db_name = 'furnacedb'

# db_connect_string = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
#     db_user, db_pwd, db_host, db_port, db_name)
# engine = create_engine(
#     db_connect_string,
#     max_overflow=5,
#     pool_size=5,
#     pool_timeout=10,
#     pool_recycle=-1
# )  # 创建引擎 echo=True 打印日志
# db_session = sessionmaker(bind=engine)  # 产生会话

class Operation_Mysql(object):
  def __init__(self,usr = 'furnace',pwd = 'furnace123456',host = '127.0.0.1',port = '3306',db = 'furnacedb'):
    db_connect_string = f'mysql+pymysql://{usr}:{pwd}@{host}:{port}/{db}?charset=utf8'
    engine = create_engine(
    db_connect_string,
    max_overflow=5,
    pool_size=5,
    pool_timeout=10,
    pool_recycle=-1
    )  # 创建引擎 echo=True 打印日志
    self.session = sessionmaker(bind=engine)

  def get_session(self):
    ''' 单线程 可使用'''
    return scoped_session(self.session)

mysql_session = Operation_Mysql()

