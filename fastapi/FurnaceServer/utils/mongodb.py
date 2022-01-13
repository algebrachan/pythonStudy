import pymongo
import sys
from datetime import datetime, timedelta

class Operation_Mongo(object):
  def __init__(self, usr='admin', passwd=123456, host='127.0.0.1', port=27017, db='furnace'):
    self.connect_client = pymongo.MongoClient(f"mongodb://{usr}:{passwd}@{host}:{port}/")
    self.mydb = self.connect_client[db] # 连接指定数据库
  
  def insert_collection(self,collection_name,value): # 单个插入
    mycol = self.mydb[collection_name]
    mycol_id = mycol.insert_one(value)
    return mycol_id.inserted_id # 返回 _id

  def insert_batch_collection(self,collection_name,value_list):
    mycol = self.mydb[collection_name]
    mycol_id = mycol.insert_many(value_list)
    return mycol_id.inserted_ids

  def save_collection(self,collection_name,value):
    '''保存，若_id不存在则插入''' 
    mycol = self.mydb[collection_name]
    mycol_id = mycol.save(value)
    return mycol_id


  def select_one_collection(self,collection_name,search_col=None,return_type=None):#获取一条数据
    my_col=self.mydb[collection_name]
    try:
      result = my_col.find_one(search_col,return_type)  # 这里只会返回一个对象，数据需要自己取
      return result
    except TypeError as e:
      print('查询条件只能是dict类型')
      return None

  def select_all_collection(self,collection_name,search_col=None,return_type=None,limit_num=sys.maxsize,sort_col='None_sort',sort='asc'):
    my_col = self.mydb[collection_name]
    try:
      if sort_col==False or sort_col=='None_sort':
        results=my_col.find(search_col,return_type).limit(limit_num)#这里只会返回一个对象，数据需要自己取
      else:
        sort_flag = 1
        if sort == 'desc':
          sort_flag = -1
        results = my_col.find(search_col,return_type).sort(sort_col,sort_flag).limit(limit_num)  # 这里只会返回一个对象，数据需要自己取
      result_all = [i for i in results]#将获取到的数据添加至list
      return result_all
    except TypeError as e:
      print('查询条件只能是dict类型')
      return None

  def update_one_collecton(self,collection_name,search_col,update_col):
    my_col = self.mydb[collection_name]
    try:
      relust = my_col.update_one(search_col,update_col)
      return relust
    except TypeError as e:
      print('查询条件与需要修改的字段只能是dict类型')
      return None

  def update_batch_collecton(self,collection_name,search_col,update_col):
    my_col = self.mydb[collection_name]
    try:
      relust = my_col.update_many(search_col,update_col)
      return relust
    except TypeError as e:
      print('查询条件与需要修改的字段只能是dict类型')
      return None

  def aggregate_coolection(self,collection_name,pipeline):
    my_col = self.mydb[collection_name]
    try:
      relust = my_col.aggregate(pipeline)
      return relust
    except TypeError as e:
      print('聚合函数')
      return None

  def delete_one_collection(self,collection_name,search_col):#删除集合中的文档
    my_col = self.mydb[collection_name]
    try:
      relust = my_col.delete_one(search_col)
      return relust
    except TypeError as e:
      print('查询条件与需要修改的字段只能是dict类型')
      return None

  def delete_batch_collection(self,collection_name,search_col):#删除集合中的多个文档
    my_col = self.mydb[collection_name]
    try:
      relust = my_col.delete_many(search_col)
      return relust
    except TypeError as e:
      print('查询条件与需要修改的字段只能是dict类型')
      return None

  def drop_collection(self,collection_name):
    my_col = self.mydb[collection_name]
    result = my_col.drop()
    return result

  def get_connections(self):#获取所有的connections
    return self.mydb.list_collection_names()

  def close_connect(self):
    self.connect_client.close()
    return 'mongo连接已关闭'
  
  def __del__(self):
    self.close_connect()


mongo_session = Operation_Mongo()

if __name__ == '__main__':
  pipeline = [
    {'$match':{'date':{'$gte':datetime.today()-timedelta(days=31)},'mode':'diameter'}},
    {'$group':{'_id':"$date",'total_warn':{'$sum':"$warning_nums"},'total_error':{'$sum':"$error_nums"},'total_missed':{'$sum':"$missed_nums"}}},
    {'$sort':{'_id':1}}
  ]
  res = mongo_session.aggregate_coolection('alarm_desc',pipeline)
  for i in res:
    print(i)
  mongo_session.close_connect()


