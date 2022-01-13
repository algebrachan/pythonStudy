import logging
import redis
import json

class Operation_Redis(object):
  def __init__(self,host='127.0.0.1', port=6379, db=1):
    pool = redis.ConnectionPool(host = host, port = port, db = db, decode_responses=True)
    self.__connect_client = redis.Redis(connection_pool=pool)
  
  def get_session(self):
    return self.__connect_client

  def exists(self,*names):
    return self.__connect_client.exists(*names)
  
  def scan(self,**kwargs):# 模糊匹配
    return self.__connect_client.scan(**kwargs)

  def delete(self,*names):
    return self.__connect_client.delete(*names)

  def incr(self,key):
    return self.__connect_client.incr(key)

  def hash2obj(self, obj: object, name: str):
    """json转化存储方法 hset 传入的是__dict__ 对象
    """
    resp = self.__connect_client.hgetall(name)
    try:
      if any(resp):
        for key in obj:
          obj[key] = json.loads(resp[key])
    except Exception as e:
      print('e',e)
      pass
    return obj

  def __obj2hash(self, obj: object, name: str):
    """对象转json hset
    """
    try:
      for key in obj:
        self.__connect_client.hset(name, key, json.dumps(obj[key]))
      return True
    except print(0):
        pass
    return False

  def set(self,key,str,sec):
    """字符串缓存"""
    return self.__connect_client.set(key,str,sec)

  def get(self,key):
    return self.__connect_client.get(key)

  def hset(self,name,key,value):
    return self.__connect_client.hset(name,key,value)
  
  def hget(self,name,key):
    return self.__connect_client.hget(name,key)

  def set_redis_str(self,dict_obj,key,sec):
    ''' 数据缓存 '''
    self.__connect_client.set(key,json.dumps(dict_obj),sec)
    pass

  def get_redis_str(self,key):
    resp = self.__connect_client.get(key)
    res = {}
    try:
      if resp:
        res = json.loads(resp)
    except print(0):
      pass
    return res

  def set_redis(self, obj, key, sec):
    self.__obj2hash(obj, key)
    self.__connect_client.expire(key, sec)  # 过期时间
  
  def expire(self,key,sec):
    return self.__connect_client.expire(key,sec)

  def close(self):
    self.__connect_client.close()

  def __del__(self):
    self.close()
  
redis_session = Operation_Redis()


