import time 
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def task_test():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

def task_2():
    print('wc')

def run_schd():
    try:
        schedular =  BackgroundScheduler(timezone="Asia/Shanghai")   # 后台
        schedular.add_job(task_test , 'interval', seconds=5)  # 以 interval 间隔性执行
        schedular.add_job(task_2,'interval',seconds=10)  # 以 interval 间隔性执行
        schedular.start()
    except Exception as e:
        print(e)
        pass

if __name__ == 'utils.apscheduler':
    # run_schd()
    pass
    