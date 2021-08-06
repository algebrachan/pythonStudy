from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import and_, desc, func, distinct, case
from config import mongo_session,logger,mysql_session
from models.models import TempCraft ,SeedCraft, ShoulderCraft
from myapp import batch_add_stic_data,interv_add_history_broken

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

def regular_std_stic():
  session = mysql_session.session()
  try:
      print('wc')
      # 查询数据库 当天的数据
      now = datetime.now()
      before = now - timedelta(days=1) # 一天前
      # save_time = now - timedelta(minutes=10)

      cdt_weld = []
      cdt_weld.append(TempCraft.gmt_update >= before)
      cdt_weld.append(TempCraft.gmt_update < now)
      db_weld = session.query(TempCraft.weld_std,func.count('*')).filter(and_(*cdt_weld)).group_by(TempCraft.weld_std).all()
      mg_weld_obj = CommonStd(now,'weld')
      for item in db_weld:
          if item[0] == 0: mg_weld_obj.std_o = item[1]
          elif item[0] == 1: mg_weld_obj.std = item[1]
          else: pass
      # 更新
      logger.error('update_weld',mg_weld_obj.__dict__)
      mongo_session.insert_collection('std_stic',mg_weld_obj.__dict__)

      cdt_seed = []
      cdt_seed.append(SeedCraft.gmt_update >= before)
      cdt_seed.append(SeedCraft.gmt_update < now)
      db_seed = session.query(SeedCraft.seed_std,func.count('*')).filter(and_(*cdt_seed)).group_by(SeedCraft.seed_std).all()
      mg_seed_obj = SeedStd(now,'seed')
      for item in db_seed:
          if item[0] == 1: mg_seed_obj.std = item[1]
          elif item[0] == 2: mg_seed_obj.l_o = item[1]
          elif item[0] == 3: mg_seed_obj.s_o = item[1]
          elif item[0] == 4: mg_seed_obj.b_o = item[1]
          else: pass
      # 更新
      logger.error('update_seed',mg_seed_obj.__dict__)
      mongo_session.insert_collection('std_stic',mg_seed_obj.__dict__)

      cdt_shoulder = []
      cdt_shoulder.append(ShoulderCraft.gmt_update >= before)
      cdt_shoulder.append(ShoulderCraft.gmt_update < now)
      db_shoulder = session.query(ShoulderCraft.shoulder_std,func.count('*')).filter(and_(*cdt_shoulder)).group_by(ShoulderCraft.shoulder_std).all()
      mg_shoulder_obj = CommonStd(now,'shoulder')
      for item in db_shoulder:
          if item[0] == 0: mg_shoulder_obj.std_o = item[1]
          elif item[0] == 1: mg_shoulder_obj.std = item[1]
          else: pass
      # 更新
      logger.error('update_shoulder',mg_shoulder_obj.__dict__)
      mongo_session.insert_collection('std_stic',mg_shoulder_obj.__dict__)

  except Exception as e:
      logger.error(e)
      pass
  session.close()
  return None

def run_schd():
    try:
        schedular =  BackgroundScheduler(timezone="Asia/Shanghai")   # 后台
        schedular.add_job(batch_add_stic_data , 'interval',minutes=10)  # 以 interval 间隔性执行
        schedular.add_job(regular_std_stic,'cron',hour=23, minute=59)  # 以 cron 间隔性执行
        schedular.add_job(interv_add_history_broken,'cron',hour=23, minute=59)  # 以 cron 间隔性执行
        schedular.start()
    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':
    run_schd()

# if __name__ == '__main__':
#     run_schd()

    