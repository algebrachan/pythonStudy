from datetime import datetime,timedelta
import json
from common.entity import ResponseBase, Error,dict_model,valid_ip
from common.mvt_req import ReqUpRealtimeServer,ReqUpRealtimeModel,ReqUpAlarmInfo,ReqUpFurInfo
from common.response import GroupListItem,CommonListItem,mongo_init_data
from config import redis_session, logger, mongo_session
from utils.common import s_reqs

def up_realtime_server(item:ReqUpRealtimeServer,res:ResponseBase):
  try:
    search_col={'server_ip':item.server_ip}
    mongo_dict = mongo_session.select_one_collection('server_info',search_col)
    if mongo_dict == None:
      mongo_dict = {}
      mongo_dict['server_ip'] = item.server_ip
      mongo_dict['server_name'] = ''
      mongo_dict['state'] = 1
    # 初始化
    temp_alarm = 0
    cpu_info = {}
    memory_info = {}
    disk_info = {} 
    gpu_info = []
    model_info = {}
    # 赋值
    cpu_info['percent'] = item.cpu_info.get('percent',0)
    cpu_info['status'] = item.cpu_info.get('status',0)
    if cpu_info['status'] == 1: temp_alarm |= 0b1

    memory_info['total'] = item.memory_info.get('total',0)
    memory_info['used'] = item.memory_info.get('used',0)
    memory_info['percent'] = item.memory_info.get('percent',0)
    memory_info['status'] = item.memory_info.get('status',0)
    if memory_info['status'] == 1: temp_alarm |= 0b10

    disk_info['total'] = item.disk_info.get('total',0)
    disk_info['used'] = item.disk_info.get('used',0)
    disk_info['free'] = item.disk_info.get('free',0)
    disk_info['percent'] = item.disk_info.get('percent',0)
    disk_info['status'] = item.disk_info.get('status',0)
    if disk_info['status'] == 1: temp_alarm |= 0b100

    for child in item.gpu_info:
      gpu_child = {}
      gpu_child['gpu_id'] = child.get('gpu_id','')
      gpu_child['total'] = child.get('total',0)
      gpu_child['used'] = child.get('used',0)
      gpu_child['percent'] = child.get('percent',0)
      gpu_child['power'] = child.get('power',0)
      gpu_child['temp'] = child.get('temp',0)
      gpu_child['status'] = child.get('status',0)
      if gpu_child['status'] == 1: temp_alarm |= 0b1000
      gpu_info.append(gpu_child)
    
    model_info['status'] = item.model_info.get('status',0)
    if model_info['status'] == 1 : temp_alarm |= 0b10000

    # 存 redis
    redis_session.hset(f'{item.server_ip}','cpu_info',json.dumps(cpu_info))
    redis_session.hset(f'{item.server_ip}','memory_info',json.dumps(memory_info))
    redis_session.hset(f'{item.server_ip}','disk_info',json.dumps(disk_info))
    redis_session.hset(f'{item.server_ip}','gpu_info',json.dumps(gpu_info))
    redis_session.hset(f'{item.server_ip}','model_info',json.dumps(model_info))
    redis_session.expire(f'{item.server_ip}',60*60) # 缓存一个小时
    # 存 mongodb
    mongo_dict['alarm'] = temp_alarm
    mongo_dict['update'] = datetime.now()
    mongo_session.save_collection('server_info',mongo_dict)
    res.succ()
    pass
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass

  return res

def up_realtime_model(item:ReqUpRealtimeModel,res:ResponseBase):
  try:
    model_list = []
    for child in item.model_list:
      model_child = {}
      model_child['name'] = child.get('name','')
      model_child['running_status'] = child.get('running_status',0)
      model_child['used_memory'] = child.get('used_memory',0)
      model_child['used_gpu'] = child.get('used_gpu',0)
      model_child['detect_speed'] = child.get('detect_speed',0)
      model_child['cache_img_nums'] = child.get('cache_img_nums',0)
      model_list.append(model_child)
    redis_session.hset(f'{item.server_ip}','model_list',json.dumps(model_list))
    redis_session.expire(f'{item.server_ip}',60*60)
    res.succ()
    pass
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res
    
def up_alarm_info(item:ReqUpAlarmInfo,res:ResponseBase):
  try:
    mongo_dict = {}
    redis_session.incr('alarm_info_index')
    index = redis_session.get('alarm_info_index')
    mongo_dict['index'] = int(index)
    mongo_dict['update'] = datetime.now()
    mongo_dict['fur_series'] = item.fur_series
    mongo_dict['fur_id'] = item.fur_id
    mongo_dict['alarm_time'] = item.alarm_time
    mongo_dict['alarm_craft'] = item.alarm_craft
    mongo_dict['alarm_func'] = item.alarm_func
    mongo_dict['alarm_result'] = item.alarm_result
    mongo_dict['server_ip'] = item.server_ip
    mongo_session.insert_collection('alarm_info',mongo_dict)
    res.succ()
    pass
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res

def up_furnace_info(item:ReqUpFurInfo,res:ResponseBase):
  try:
    search_col={'furnace_series':item.furnace_series,'furnace_id':item.furnace_id}
    mongo_dict = mongo_session.select_one_collection('furnace_list',search_col)
    if mongo_dict == None:
      mongo_dict = {}
    mongo_dict['update'] = datetime.now()
    mongo_dict['furnace_series'] = item.furnace_series
    mongo_dict['furnace_id'] = item.furnace_id
    mongo_dict['furnace_state'] = item.furnace_state
    mongo_dict['server_ip'] = item.server_ip
    mongo_dict['online'] = item.online
    mongo_session.save_collection('furnace_list',mongo_dict)
    res.succ()
    pass
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  return res

def alarm_info_list(fur_series:str,fur_id:str,alarm_func:str,res:ResponseBase):
  data = {'alarm_info_list':[],'total':0}
  try:
    # search_col = {'username':{'$regex':f'{value}'},'state':1} # 模糊匹配
    search_col = {}
    if fur_series != '': search_col['fur_series'] = fur_series
    if fur_id != '': search_col['fur_id'] = int(fur_id)
    if alarm_func != '': search_col['alarm_func'] = alarm_func
    return_type = {'_id':0,'update':0}
    mg_data = mongo_session.select_all_collection('alarm_info',search_col,return_type,sort_col='alarm_time', sort='desc')
    if len(mg_data)>0:
      data['alarm_info_list'] = mg_data
      data['total'] = len(mg_data)
    res.data = data
    pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  return res

def alarm_info_simplify(count,res:ResponseBase):
  data = {'alarm_info_list':[]}
  try:
    search_col = {}
    return_type = {'_id':0,'update':0}
    mg_data = mongo_session.select_all_collection('alarm_info',search_col,return_type,limit_num=count,sort_col='alarm_time', sort='desc')
    if len(mg_data)>0:
      data['alarm_info_list'] = mg_data
      data['total'] = len(mg_data)
    res.data = data
    pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  return res

def server_list(count:int,res:ResponseBase):
  data = {'server_list_r':[],'server_list_l':[]}
  try:
    total_server_list = []
    search_col={'state':1} # 服务器状态可用
    return_type = {'_id':0,'server_ip':1,'alarm':1,'server_name':1}
    mg_data = mongo_session.select_all_collection('server_info',search_col,return_type,limit_num=count,sort_col='update',sort='desc')
    for child in mg_data:
      if child['alarm'] != 0 : 
        child['server_state'] = 1
      else:
        child['server_state'] = 0
      # 根据server_ip 查找 count
      pipeline = [
        {'$match':{'server_ip':child['server_ip']}},
        {'$group':{'_id':"$server_ip",'count':{'$sum':1}}},
        {'$sort':{'_id':1}}
      ]
      child_data = mongo_session.aggregate_coolection('furnace_list',pipeline)
      l = list(child_data)
      if len(l) == 0:
        child['fur_count'] = 0
      else:
        child['fur_count'] = l[0]['count']
      total_server_list.append(child)
    # 补全处理
    for i in range(count - len(mg_data)):
      temp = {}
      temp['server_ip'] = f'0.0.0.{i}'
      temp['server_name'] = ""
      temp['alarm'] = 0
      temp['server_state'] = 0
      temp['fur_count'] = 0
      total_server_list.append(temp)
    # 拆分处理
    median = int(count/2)
    data['server_list_l'] = total_server_list[0:median]
    data['server_list_r'] = total_server_list[median:]
    res.data = data
    pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  return res

def server_state(server_ip:str,res:ResponseBase):
  data = {'cpu_info':{},'memory_info':{},'disk_info':{},'gpu_info':[]}
  try:
    if redis_session.exists(server_ip) == 0:
      # 不存在
      res.error(Error.NO_DATA)
      return res
    h1 = redis_session.hget(server_ip,'cpu_info')
    if h1:
      data['cpu_info'] = json.loads(h1)
      pass
    h2 = redis_session.hget(server_ip,'memory_info')
    if h2:
      data['memory_info'] = json.loads(h2)
      pass
    h3 = redis_session.hget(server_ip,'gpu_info')
    if h3:
      data['gpu_info'] = json.loads(h3)
      pass
    h4 = redis_session.hget(server_ip,'disk_info')
    if h4:
      data['disk_info'] = json.loads(h4)
      pass
    res.data = data
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  return res

def model_state(server_ip:str,res:ResponseBase):
  data = {'model_list':[]}
  try:
    if redis_session.exists(server_ip) == 0:
      res.error(Error.NO_DATA)
      return res
    h = redis_session.hget(server_ip,'model_list')
    if h:
      data['model_list'] = json.loads(h)
      pass
    res.data = data
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  return res

def history_broken(days:int,server_ip:str,res:ResponseBase):
  data = {'broken_list':[]}
  try:
    broken_list = []
    search_col = {'date':{'$gte':datetime.today()-timedelta(days)},'server_ip':server_ip}
    return_type = {'_id':0,'update':0}
    mg_data = mongo_session.select_all_collection('history_broken',search_col,return_type,sort_col='date')
    for child in mg_data:
      date = child['date'].strftime("%Y-%m-%d")
      broken_list.append(GroupListItem('等径',date,child['diameter']).__dict__)
      broken_list.append(GroupListItem('放肩',date,child['shoulder']).__dict__)
    data['broken_list'] = broken_list
    res.data = data
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  return res

def broken_info(date:datetime,craft:str,res:ResponseBase):
  data = {'broken_list':[]}
  try:
    search_col = {'alarm_time':{'$gte':date,'$lt':date+timedelta(days=1)}}
    if craft == '': 
      search_col['alarm_craft'] = {'$in':[9,11]}
      pass
    else:
      search_col['alarm_craft'] = int(craft)
      pass
    return_type = {'_id':0,'update':0}
    mg_data = mongo_session.select_all_collection('alarm_info',search_col,return_type,sort_col='update',sort='desc')
    if len(mg_data)>0:
      data['broken_list'] = mg_data
      data['total'] = len(mg_data)
    res.data = data
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  return res

def online_fur(server_ip:str,res:ResponseBase):
  data = {'online_list':[]}
  try:
    pipeline = [
      {'$match':{'furnace_state':{'$in':[4,5,9,11,12,20,28,29]},'online':1,'server_ip':server_ip}},
      {'$group':{'_id':"$furnace_state",'count':{'$sum':1}}},
      {'$sort':{'_id':1}}
    ]
    mg_data = mongo_session.aggregate_coolection('furnace_list',pipeline)
    data['online_list'],data['total'] = mongo_init_data(mg_data,dict_model,CommonListItem)
    pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  res.data = data
  return res

def series_list(server_ip:str,res: ResponseBase):
  data = {'series_list':[]}
  series_list = []
  try:
    pipeline = [
      {'$group':{'_id':"$furnace_series",'count':{'$sum':1}}},
      {'$sort':{'_id':1}},
    ]
    if valid_ip(server_ip):
      pipeline.insert(0,{'$match':{'server_ip':server_ip}})
    
    mg_data = mongo_session.aggregate_coolection('furnace_list',pipeline)
    for item in mg_data:
      series_list.append(item['_id'])
    data['series_list'] = series_list
    res.data = data
    pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  return res

def current_fur_list(series: str,server_ip:str, res: ResponseBase):
  data = {'fur_list':[],'series':series}
  fur_list = []
  try:
    search_col = {'furnace_series':series,'server_ip':server_ip,'online':1}
    return_type = {'_id':0,'update':0,'server_ip':0}
    mg_data = mongo_session.select_all_collection('furnace_list',search_col,return_type,sort_col='furnace_id')
    if len(mg_data)>0:
      for item in mg_data:
        child = {}
        child['s'] = series
        child['id'] = item["furnace_id"]
        child['name'] = f'{series}{item["furnace_id"]}'
        child['state'] = item["furnace_state"]
        fur_list.append(child)
      data['fur_list'] = fur_list
    else:
      res.error(Error.NO_DATA)
      pass
    res.data = data
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  return res

def fur_result(furnace_series: str, furnace_id: str, device_state:str,model_name:str, res: ResponseBase):
  try:
    data = {'img_list':[]}
    search_col={'furnace_id':int(furnace_id),'furnace_series':furnace_series}
    mongo_dict = mongo_session.select_one_collection('furnace_list',search_col)
    if mongo_dict == None: raise Exception('furnace is not exist')
    server_ip = mongo_dict.get('server_ip','127.0.0.1')
    device_id = furnace_series + furnace_id
    addr = f'http://{server_ip}:5000/furnace_realtime_detection?device_id={device_id}&device_state={device_state}&model_name={model_name}'
    resp = s_reqs.get(addr, timeout=1).json()
    res.data = resp
    pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION,e.__str__())
    logger.error(e)
    pass
  return res