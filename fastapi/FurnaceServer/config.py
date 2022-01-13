import configparser
import os
import platform
from utils.redis import Operation_Redis
# from utils.mysql import Operation_Mysql
from utils.mongodb import Operation_Mongo
from utils.log import Logger

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')
config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding="utf-8")
sections = config.sections()

mongo_session = object
# mysql_session = object
redis_session = object
logger = object

if 'mongodb' in sections:
  mongo_session = Operation_Mongo(
    usr=config.get('mongodb','usr'),
    passwd=config.get('mongodb','pwd'),
    host=config.get('mongodb','host'),
    port=config.getint('mongodb','port'),
    db=config.get('mongodb','db'),
  )
else:
  mongo_session = Operation_Mongo()

# if 'mysql' in sections:
#   mysql_session = Operation_Mysql(
#     usr=config.get('mysql','usr'),
#     pwd=config.get('mysql','pwd'),
#     host=config.get('mysql','host'),
#     port=config.getint('mysql','port'),
#     db=config.get('mysql','db'),
#   )
# else:
#   mysql_session = Operation_Mysql()

if 'redis' in sections:
  redis_session = Operation_Redis(
    host=config.get('redis','host'),
    port=config.getint('redis','port'),
    db=config.getint('redis','db'),
  )
else:
  redis_session = Operation_Redis()

log_path = ''
if(platform.system()=='Windows'):
  log_path = 'D:\\log\\fastapi_log\\'
elif(platform.system()=='Linux'):
  log_path = '/app/log/'
else:
  pass
if(not os.path.exists(log_path)):
    os.mkdir(log_path)

if 'log' in sections:
  logger = Logger(
    log_path+config.get('log','filename'),
    level=config.get('log','level'),
    when=config.get('log','when'),
    interval=config.getint('log','interval'), 
    backCount=config.getint('log','backCount'),
  ).logger
else:
  logger = Logger(log_path+'server.log', when='midnight').logger

if __name__ == '__main__':
    mongo_session.drop_collection("2B20_craft")
    mongo_session.drop_collection("2B21_craft")
    mongo_session.drop_collection("2B22_craft")
    mongo_session.drop_collection("2B23_craft")
    mongo_session.drop_collection("furnace")
    