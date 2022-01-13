from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from config import mongo_session,logger

class CommonStd(object):
    def __init__(self, date, craft):
        self.date = date
        self.craft = craft
        self.std = 0
        self.std_o = 0
class SeedStd(CommonStd):
    def __init__(self, *args):
        CommonStd.__init__(self,*args)
        self.l_o = 0
        self.s_o = 0
        self.b_o = 0
        


def task_2():
    print('wc')


def regular_broken_stic():
  try:
    now = datetime.now()
    before = now - timedelta(days=1) # 一天前
    # 查询 在线服务器
    search_col = {'state':1} # 模糊匹配
    return_type = {'_id':0,'server_ip':1}
    mg_data = mongo_session.select_all_collection('server_info',search_col,return_type)
    for child in mg_data:
      pipeline = [
        {'$match':{'alarm_time':{'$gte':before,'$lt':now},'alarm_craft':{'$in':[9,11]},'server_ip':child['server_ip']}},
        {'$group':{'_id':"$alarm_craft",'count':{'$sum':1}}},
        {'$sort':{'_id':1}}
      ]
      broken_stic = mongo_session.aggregate_coolection('alarm_info',pipeline)
      mongo_dict = {}
      mongo_dict['shoulder'] = 0
      mongo_dict['diameter'] = 0
      for item in broken_stic:
        if item['_id'] == 9: 
          mongo_dict['shoulder'] = item['count']
        elif item['_id'] == 11: 
          mongo_dict['diameter'] = item['count']
        else: pass
      mongo_dict['date'] = now
      mongo_dict['update'] = datetime.now()
      mongo_dict['server_ip'] = child['server_ip']
      mongo_session.insert_collection('history_broken',mongo_dict)
  except Exception as e:
    logger.error(e)
    pass
  return None

def regular_std_stic():
  try:
      # 查询数据库 当天的数据
      now = datetime.now()
      before = now - timedelta(days=1) # 一天前
      # save_time = now - timedelta(minutes=10)
      cdt_weld = [
        {'$match':{'update':{'$gte':before,'$lt':now}}},
        {'$group':{'_id':"$weld_std",'count':{'$sum':1}}},
        {'$sort':{'_id':1}}
      ]
      mg_weld = mongo_session.aggregate_coolection('weld_craft',cdt_weld)
      mg_weld_obj = CommonStd(now,'weld')
      for item in mg_weld:
        if item['_id'] == 0: mg_weld_obj.std_o = item['count']
        elif item['_id'] == 1: mg_weld_obj.std = item['count']
        else: pass
      # cdt_weld = []
      # cdt_weld.append(TempCraft.gmt_update >= before)
      # cdt_weld.append(TempCraft.gmt_update < now)
      # db_weld = session.query(TempCraft.weld_std,func.count('*')).filter(and_(*cdt_weld)).group_by(TempCraft.weld_std).all()
      # mg_weld_obj = CommonStd(now,'weld')
      # for item in db_weld:
      #     if item[0] == 0: mg_weld_obj.std_o = item[1]
      #     elif item[0] == 1: mg_weld_obj.std = item[1]
      #     else: pass
      # 更新
      logger.error('update_weld',mg_weld_obj.__dict__)
      mongo_session.insert_collection('std_stic',mg_weld_obj.__dict__)


      cdt_seed = [
        {'$match':{'update':{'$gte':before,'$lt':now}}},
        {'$group':{'_id':"$seed_std",'count':{'$sum':1}}},
        {'$sort':{'_id':1}}
      ]
      mg_seed = mongo_session.aggregate_coolection('seed_craft',cdt_seed)
      mg_seed_obj = SeedStd(now,'seed')
      for item in mg_seed:
        if item['_id'] == 1: mg_seed_obj.std = item['count']
        elif item['_id'] == 2: mg_seed_obj.l_o = item['count']
        elif item['_id'] == 3: mg_seed_obj.s_o = item['count']
        elif item['_id'] == 4: mg_seed_obj.b_o = item['count']
        else: pass
      logger.error('update_seed',mg_seed_obj.__dict__)
      mongo_session.insert_collection('std_stic',mg_seed_obj.__dict__)

      cdt_shoulder = [
        {'$match':{'update':{'$gte':before,'$lt':now}}},
        {'$group':{'_id':"$seed_std",'count':{'$sum':1}}},
        {'$sort':{'_id':1}}
      ]
      mg_shoulder = mongo_session.aggregate_coolection('shoulder_craft',cdt_shoulder)
      mg_shoulder_obj = CommonStd(now,'shoulder')
      for item in mg_shoulder:
        if item['_id'] == 0: mg_shoulder_obj.std_o = item[1]
        elif item['_id'] == 1: mg_shoulder_obj.std = item[1]
        else: pass
      logger.error('update_seed',mg_shoulder_obj.__dict__)
      mongo_session.insert_collection('std_stic',mg_shoulder_obj.__dict__)

  except Exception as e:
      logger.error(e)
      pass
  return None

def run_schd():
    try:
        schedular =  BackgroundScheduler(timezone="Asia/Shanghai")   # 后台
        # schedular.add_job(regular_broken_stic , 'interval',minutes=2)  # 以 interval 间隔性执行
        # schedular.add_job(regular_std_stic,'cron',hour=23, minute=59)  # 以 cron 间隔性执行
        schedular.add_job(regular_broken_stic,'cron',hour=23, minute=59)  # 以 cron 间隔性执行
        schedular.start()
    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':
    # run_schd()
    # regular_broken_stic()
    print(0)


    