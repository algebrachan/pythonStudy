from datetime import datetime
from common.entity import ResponseBase, Error
from common.admin_req import ReqUpdateUser,ReqLogin,ReqUpdateServer
from config import redis_session, logger, mongo_session
from utils.common import get_token

def super_admin(username:str,password:str,res:ResponseBase):
  try:
    # 查询数据库是否存在该用户
    search_col={'username':username}
    mongo_dict = mongo_session.select_one_collection('user_info',search_col)
    if mongo_dict == None:
      mongo_dict = {}
    mongo_dict['update'] = datetime.now()
    mongo_dict['username'] = username
    mongo_dict['password'] = password
    mongo_dict['server_ip'] = ''
    mongo_dict['type'] = 0 # 0 超级管理员 1 普通
    mongo_dict['login_time'] = datetime.now()
    mongo_dict['state'] = 1 # 0 不可用 1 可用
    mongo_session.save_collection('user_info',mongo_dict)
    res.succ()
    pass

  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res

def login(item:ReqLogin,res:ResponseBase):
  # denglu 
  data = {'token':'','account':'','type':0}
  try:
    search_col={'username':item.username,'state':1}
    user_dict = mongo_session.select_one_collection('user_info',search_col)
    if user_dict == None:
      res.error(Error.PARAM_ERR,err_msg="用户不存在")
      return res
    if user_dict['password'] != item.password:
      res.error(Error.PARAM_ERR,err_msg="密码错误")
      return res
    # 成功 更新登录时间
    user_dict['login_time'] = datetime.now()
    mongo_session.save_collection('user_info',user_dict)
    # 生成token
    token = get_token(item.username)
    data['token'] = token
    data['account'] = user_dict['username']
    data['type'] = user_dict['type']
    print(data)
    if user_dict['type'] == 1:
      data['server_ip'] = user_dict['server_ip']
    # token存入 redis
    redis_session.set(token,item.username,60*60)
    res.msg = "登录成功"
    res.data = data
    pass
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res

def up_user(admin:str,item:ReqUpdateUser,res:ResponseBase):
  try:
    # 校验权限
    admin_col={'username':admin}
    admin = mongo_session.select_one_collection('user_info',admin_col)
    if admin['type'] != 0:
      res.error(Error.NO_AUTH) # 没有权限
      return res
    # 查询数据库是否存在该用户
    search_col={'username':item.username}
    mongo_dict = mongo_session.select_one_collection('user_info',search_col)
    if mongo_dict == None:
      mongo_dict = {}
    if item.operation == 0: # 新增
      mongo_dict['username'] = item.username
      mongo_dict['password'] = item.password
      mongo_dict['type'] = item.user_type
      mongo_dict['server_ip'] = item.server_ip
      mongo_dict['state'] = 1
      pass
    elif item.operation == 1: # 修改
      mongo_dict['username'] = item.username
      mongo_dict['password'] = item.password
      mongo_dict['type'] = item.user_type
      mongo_dict['server_ip'] = item.server_ip
      pass
    elif item.operation == 2: # 删除
      mongo_dict['username'] = item.username
      mongo_dict['state'] = 0
      pass
    else:
      res.error(Error.OPT_ERR,err_msg='操作数异常') 
      return res
    mongo_dict['update'] = datetime.now()
    mongo_session.save_collection('user_info',mongo_dict)
    res.succ()
    pass

  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res

def user_list(value:str,res:ResponseBase):
  data = {'user_list':[],'total':0}
  try:
    search_col = {'username':{'$regex':f'{value}'},'state':1} # 模糊匹配
    return_type = {'_id':0,'username':1,'login_time':1,'type':1,'state':1}
    mg_data = mongo_session.select_all_collection('user_info',search_col,return_type,sort_col='update',sort='desc')
    if len(mg_data)>0:
      data['user_list'] = mg_data
      data['total'] = len(mg_data)
    res.data = data
    pass
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res

def up_server(admin:str,item:ReqUpdateServer,res:ResponseBase):
  try:
    admin_col={'username':admin}
    admin = mongo_session.select_one_collection('user_info',admin_col)
    if admin['type'] != 0:
      res.error(Error.NO_AUTH)
      return res
    search_col={'server_ip':item.server_ip}
    mongo_dict = mongo_session.select_one_collection('server_info',search_col)
    if mongo_dict == None:
      mongo_dict = {}
    mongo_dict['server_ip'] = item.server_ip
    mongo_dict['server_name'] = item.server_name
    mongo_dict['update'] = datetime.now()
    if item.operation == 0: # 新增
      mongo_dict['alarm'] = 0
      mongo_dict['state'] = 1
      pass
    elif item.operation == 2: # 删除
      mongo_dict['state'] = 0
      pass
    else:
      pass
    mongo_session.save_collection('server_info',mongo_dict)
    res.succ()
    pass
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res

def server_list(value:str,res:ResponseBase):
  data = {'server_list':[],'total':0}
  try:
    search_col = {'server_ip':{'$regex':f'{value}'},'state':1} # 模糊匹配
    return_type = {'_id':0,'update':0}
    mg_data = mongo_session.select_all_collection('server_info',search_col,return_type,sort_col='update',sort='desc')
    if len(mg_data)>0:
      data['server_list'] = mg_data
      data['total'] = len(mg_data)
    res.data = data
    pass
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res


def furnace_lists(id: str, series: str, status: str, idx: int, size: int,res: ResponseBase):
  data={'fur_list':[],'total':0}
  try:
    search_col = {}
    if series != '':search_col['furnace_series'] = series
    if id != '':search_col['furnace_id'] = int(id)
    if status != '':search_col['furnace_state'] = int(status)
    return_type = {'_id':0}
    mg_data = mongo_session.select_all_collection('furnace_list',search_col,return_type,sort_col='furnace_id')
    if len(mg_data)>0:
      data['fur_list'] = mg_data
      data['total'] = len(mg_data)
    res.data = data
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res

if __name__ == '__main__':
    a = 0b101
    b = 0b10
    print(a&b)
    