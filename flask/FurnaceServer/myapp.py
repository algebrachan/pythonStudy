import threading
import requests
import json
import random
import string
import datetime

series_list = list(string.ascii_uppercase)
series_list.remove('O')
series_list.remove('I')
HOST = 'http://10.50.60.206:8065'

def batch_add_fur():

    for i in series_list:
        for j in range(1, 97):
            body = {
                'furnace_id': j,
                'furnace_series': i,
                'furnace_state': 99,
                'furnace_host': '10.50.63.63'
            }
            r = requests.post(f'{HOST}/api/mvt/update_fur_state',
                              data=json.dumps(body))
            print(r.text)


def batch_add_series_brokens():
    for i in [1, 2]:
        for j in series_list:
            body = {
                "type": i,
                "series": j,
                "broken_nums":  random.randint(1, 10)*10
            }
            r = requests.post(
                'http://10.50.63.63:8065/api/mvt/update_series_broken', data=json.dumps(body))
            print(r.text)


def batch_add_history_broken():
        # update_history_broken 从今天开始前30天
        for j in get_data_list(30):
            body = {
                "date": j,
                "diameter_broken_nums": random.randint(1, 10)*10,
                "shouldering_broken_nums": random.randint(1, 10)*10
            }
            r = requests.post(
                f'{HOST}/api/mvt/update_history_broken', data=json.dumps(body))
            print(r.text)

def interv_add_history_broken():
  body = {
    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
    "diameter_broken_nums": random.randint(50, 100),
    "shouldering_broken_nums": random.randint(60, 100)
  }
  r = requests.post(f'{HOST}/api/mvt/update_history_broken', data=json.dumps(body))
  print(r.text)

def get_probability(rate_list,value_list):
  '''rate为0的概率,两点分布'''
  if not (0.99999<sum(rate_list)<1.00001):
    raise ValueError('the rate_list are not normalized!')
  
  if len(rate_list) != len(value_list):
    raise ValueError('the length of two input lists are not match!')
  
  random_normalized_num= random.random() # random() -> x in the interval [0, 1)
  accumulated_probability= 0.0 # 初始随机变量
  for item in zip(rate_list,value_list):
    accumulated_probability += item[0]
    if random_normalized_num < accumulated_probability:
      return item[1]


def get_data_list(days):
    """返回前days天日期列表"""
    date_list = []
    for i in range(1, days+1):
        day = datetime.datetime.now()-datetime.timedelta(days=i)
        date_to = datetime.datetime(day.year, day.month, day.day)
        date_list.append(str(date_to))
    return date_list

def batch_add_stic_data():
    for furnace_id in ['2B20','2B21','2B22','2B23']:
        now = datetime.datetime.now()
        temp_body = {
            "furnace_id":furnace_id,
            "weld_wt":round(random.random()+random.randint(0,3),2),
            "weld_type":random.randint(1,7),
            "weld_std":get_probability([0.1,0.9],[0,1]),
            "update_time":f'{now}'
        }
        r_temp = requests.post(f'{HOST}/api/anls/update_temp_process', data=json.dumps(temp_body))
        print(r_temp.text)
        seed_body = {
            "furnace_id":furnace_id,
            "seed_wt":round(random.random()+random.randint(1,4),2),
            "seed_lates":round(random.random()+random.randint(200,400),2),
            "seed_type":random.randint(1,5),
            "seed_std":get_probability([0.7,0.12,0.11,0.07],[1,2,3,4]),
            "seed_off":get_probability([0.2,0.8],[1,0]),
            "seed_diam":round(random.random()+random.randint(3,10),2),
            "seed_ddvt":round(random.random()+random.randint(0,2),2),
            "update_time":f'{now}'
        }
        r_seed = requests.post(f'{HOST}/api/anls/update_seed_process', data=json.dumps(seed_body))
        print(r_seed.text)
        shoulder_body = {
            "furnace_id":furnace_id,
            "shoulder_wt":round(random.random()+random.randint(0,4),2),
            "shoulder_len":round(random.random()+random.randint(100,200),2),
            "shoulder_ddvt":round(random.random()+random.randint(2,8),2),
            "shoulder_ldvt":round(random.random()+random.randint(30,70),2),
            "shoulder_powerdec":round(random.random()+random.randint(5,20),2),
            "shoulder_std":get_probability([0.13,0.87],[0,1]),
            "shoulder_off":get_probability([0.65,0.35],[0,1]),
            "shoulder_type":random.randint(1,4),
            "update_time":f'{now}'
        }
        r_shoulder = requests.post(f'{HOST}/api/anls/update_shoulder_process', data=json.dumps(shoulder_body))
        print(r_shoulder.text)
        cyl_body = {
            "furnace_id":furnace_id,
            "cyl_nums":random.randint(1,10),
            "cyl_header_lates":round(random.random()+random.randint(50,100),2),
            "cyl_len":round(random.random()+random.randint(1000,1500),2),
            "cyl_off":get_probability([0.59,0.41],[0,1]),
            "update_time":f'{now}'
        }
        r_cyl = requests.post(f'{HOST}/api/anls/update_cyl_process', data=json.dumps(cyl_body))
        print(r_cyl.text)



if __name__ == '__main__':
    # batch_add_stic_data()
    # batch_add_fur()
    # batch_add_series_brokens()
    # batch_add_history_broken()
    for i in range(10):
      print(get_probability([0.1,0.9],[0,1]))

