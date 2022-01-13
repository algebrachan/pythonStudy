from config import logger
class CommonListItem:
    """ 图表类 通用item
    """
    item: str  # 分类的item
    value: int  # 暂时定义为int类型

    def __init__(self, item, value):
        self.item = str(item)
        self.value = value
class CommonFitListItem(CommonListItem):
    """ 分布图 拟合值 item
    """
    item: str 
    value: int
    fit: int 
    def __init__(self,item,value,fit):
        CommonListItem.__init__(self, item, value)
        self.fit = fit

class GroupListItem(CommonListItem):
    """ 分组 item"""
    item: str 
    value: int
    name: str
    def __init__(self,name,item, value):
        CommonListItem.__init__(self, item, value)
        self.name = str(name)

class CommonList:
    """通用列表"""

    def __init__(self):
        self.list = []
        self.total = 0

def mysql_init_data(db_data:list, dict:dict, cls):
  """[summary]
    将dict中没有数据的项 赋值0 返回
  Args:
      db_data (list): [mysql查询原始数据 0项是类型type ]
      dict (dict): [dict字典顺序,key一般对应于 mysql的 0项，一般为数字字符串]
      obj (object): [ list 中 item的类型 ]
  """
  try:
      if cls == CommonListItem:
          res_type_list = []
          dict_keys_list = list(dict.keys())
          temp_keys_list = []
          for item in db_data:
              temp_keys_list.append(f'{item[0]}')
              res_type_list.append(CommonListItem(dict[f'{item[0]}'],item[1]).__dict__)
          # 初始化未添加的内容
          d_map = map(int,list(set(dict_keys_list).difference(set(temp_keys_list))))
          d_set = sorted(list(d_map))
          for i in d_set:
              res_type_list.insert(dict_keys_list.index(f'{i}'),CommonListItem(dict[f'{i}'],0).__dict__)
          return res_type_list
      if cls == 'craft_off':
          res_type_list = []
          dict_keys_list = list(dict.keys())
          temp_keys_list = []
          for item in db_data:
              temp_keys_list.append(f'{item[0]}')
              res_type_list.append(item[1])
          d_map = map(int,list(set(dict_keys_list).difference(set(temp_keys_list))))
          d_set = sorted(list(d_map))
          for i in d_set:
              res_type_list.insert(dict_keys_list.index(f'{i}'),0)
          return res_type_list
      pass

  except Exception as e:
      return []
      
  return []

def mongo_init_data(mg_data:list, dict:dict, cls):
  try:
      res_type_list = []
      total = 0
      dict_keys_list = list(dict.keys())
      temp_keys_list = []
      if cls == CommonListItem:          
          for item in mg_data:
              temp_keys_list.append(f'{item["_id"]}')
              total += item['count']
              res_type_list.append(CommonListItem(dict[f'{item["_id"]}'],item['count']).__dict__)
          # 初始化未添加的内容
          d_map = map(int,list(set(dict_keys_list).difference(set(temp_keys_list))))
          d_set = sorted(list(d_map))
          for i in d_set:
              res_type_list.insert(dict_keys_list.index(f'{i}'),CommonListItem(dict[f'{i}'],0).__dict__)
          return res_type_list,total
      if cls == 'craft_off':
          for item in mg_data:
              temp_keys_list.append(f'{item["_id"]}')
              total += item['count']
              res_type_list.append(item['count'])
          d_map = map(int,list(set(dict_keys_list).difference(set(temp_keys_list))))
          d_set = sorted(list(d_map))
          for i in d_set:
              res_type_list.insert(dict_keys_list.index(f'{i}'),0)
          return res_type_list,total
      pass

  except Exception as e:
      logger.error(e)
      return [],0
      
  return [],0

if __name__ == '__main__':
    # cli = CommonListItem(value=2,item='wc')
    print(0)
    