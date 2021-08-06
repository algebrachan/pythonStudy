from datetime import datetime, date, timedelta
import random
import numpy as np 
from sqlalchemy import and_, desc, func, distinct, case
from common.response import CommonList, CommonListItem, CommonFitListItem, GroupListItem, mysql_init_data
from common.entity import ResponseBase, Error, temp_model, seed_model, shoulder_model
from common.anls_resp import *
from common.anls_req import ReqTempProcess, ReqSeedProcess, ReqShoulderProcess,ReqCylProcess
from config import mysql_session, redis_session, mongo_session, logger
from utils.math import interval_static, calculate_ot, CommonSticOp
from models.models import TempCraft, SeedCraft, ShoulderCraft,CylCraft




def up_temp_process(item: ReqTempProcess, res: ResponseBase):
  # 更新 数据
  session = mysql_session.session()
  try:
    tc = TempCraft()
    tc.setData(item)
    session.add(tc)
    session.commit()
    mongo_session.insert_collection(f'{tc.furnace_id}_craft',tc.chg2mongo())
    res.succ()
    pass
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  session.close()
  return res

def up_seed_process(item: ReqSeedProcess, res: ResponseBase):
  session = mysql_session.session()
  try:
    sc = SeedCraft()
    sc.setData(item)
    session.add(sc)
    session.commit()
    mongo_session.insert_collection(f'{sc.furnace_id}_craft',sc.chg2mongo())
    res.succ()
    pass
    
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  session.close()
  return res

def up_shoulder_process(item: ReqShoulderProcess, res: ResponseBase):
  session = mysql_session.session()
  # 更新 数据
  try:
    # 保存数据库 mysql
    shc = ShoulderCraft()
    shc.setData(item)
    session.add(shc)
    session.commit()
    mongo_session.insert_collection(f'{shc.furnace_id}_craft',shc.chg2mongo())
    res.succ()
    pass
    
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  session.close()
  return res

def up_cyl_process(item: ReqCylProcess, res: ResponseBase):
  session = mysql_session.session()
  # 更新 数据
  try:
    # 保存数据库 mysql
    cc = CylCraft()
    cc.setData(item)
    session.add(cc)
    session.commit()
    mongo_session.insert_collection(f'{cc.furnace_id}_craft',cc.chg2mongo())
    res.succ()
    pass  
  except Exception as e:
    res.error(Error.OPT_ERR)
    logger.error(e)
    pass
  session.close()
  return res



def temp_wt_dist(dtype: int, res: ResponseBase):
  data = {'temp_wt_list': [],'mean':0,'total':0}
  r_key = f'temp_wt_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      condition = []
      condition.append(TempCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(TempCraft.weld_wt).filter(and_(*condition)).all()
      temp_wt_list = []
      if len(db_data)>0:
        l = np.array(db_data)[:,0]
        data['mean'] = round(np.mean(l),4)
        data['total'] = len(l)
        # for key,value in interval_static(l).items():
        #   temp_wt_list.append(CommonFitListItem(key,value,0).__dict__)
        cso = CommonSticOp(l)
        cso.get_dist_fit()
        for item in cso.result:
          temp_wt_list.append(CommonFitListItem(round(item[0],1),int(item[1]),round(item[2],4)).__dict__)

      data['temp_wt_list'] = temp_wt_list
      if len(temp_wt_list) > 0:
        redis_session.set_redis_str(data,r_key, gr_sec(0))
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def temp_wt_group_dist(dtype: int, res: ResponseBase):
  data = {'temp_wtg_list': [],'mean_list':[]}
  r_key = f'temp_wtg_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      temp_wtg_list = []
      mean_list = []
      for i in temp_model.keys():
        condition = []
        condition.append(TempCraft.gmt_update >= get_startdate(dtype))
        condition.append(TempCraft.weld_type == int(i))
        db_data = session.query(TempCraft.weld_wt,TempCraft.weld_type).filter(and_(*condition)).all()
        if len(db_data):
          l = np.array(db_data)[:,0]
          # mean_list.append({'type':temp_model[i],'mean':np.mean(l),'count':len(l)})
          cso = CommonSticOp(l)
          cso.get_dist(interv=1)
          for item in cso.result:
            temp_wtg_list.append(GroupListItem(temp_model[i],item[0],item[1]).__dict__)
          
      data['temp_wtg_list'] = temp_wtg_list
      # data['mean_list'] = mean_list
      if len(temp_wtg_list) > 0 and len(mean_list) > 0:
        # redis_session.set_redis_str(data,r_key, 10)
        redis_session.set_redis_str(data,r_key,gr_sec(0))
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def temp_std(dtype: int, res: ResponseBase):
  data = {'temp_std_list': [],'total':0}
  r_key = f'temp_std_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      temp_std_list = []
      condition = []
      condition.append(TempCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(TempCraft.weld_std,func.count('*')).filter(and_(*condition)).group_by(TempCraft.weld_std).order_by(TempCraft.weld_std).all()
      for child in db_data:
        data['total'] += child[1]
      std_dict = {'0':'控制不达标','1':'控制达标'}
      temp_std_list = mysql_init_data(db_data,std_dict,CommonListItem)
      data['temp_std_list'] = temp_std_list
      if len(temp_std_list) > 0:
        redis_session.set_redis_str(data,r_key, gr_sec(0))
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def temp_type_stic(dtype: int, res: ResponseBase):
  data = {'temp_type_list': [],'total':0}
  r_key = f'temp_type_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      temp_type_list = []
      condition = []
      condition.append(TempCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(TempCraft.weld_type,func.count('*')).filter(and_(*condition)).group_by(TempCraft.weld_type).order_by(TempCraft.weld_type).all()
      for child in db_data:
        data['total'] += child[1]
      # tm_keys_list = list(temp_model.keys())
      # temp_keys_list = []
      # for item in db_data:
      #   temp_keys_list.append(f'{item[0]}')
      #   temp_type_list.append(CommonListItem(temp_model[f'{item[0]}'],item[1]).__dict__)
      # d_set = sort(list(set(tm_keys_list).difference(set(temp_keys_list))))
      # for i in d_set:
      #   temp_type_list.insert(tm_keys_list.index(i),CommonListItem(temp_model[f'{i}'],0).__dict__)
      temp_type_list = mysql_init_data(db_data,temp_model,CommonListItem)
      data['temp_type_list'] = temp_type_list
      if len(temp_type_list) > 0:
        redis_session.set_redis_str(data,r_key, gr_sec(0))
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def temp_history_stdr(res: ResponseBase):
  data = {'temp_stdr_list':[]}
  try:
    temp_stdr_list = []
    search_col={'date':{'$gte':datetime.today()-timedelta(days=30)},'craft':'weld'}
    return_type={'_id':0,'craft':0}
    mg_data = mongo_session.select_all_collection('std_stic',search_col,return_type,sort_col='date')
    for item in mg_data:
      date = item['date'].strftime("%m-%d")
      total = item['std'] + item['std_o']
      value = 0
      if total != 0:
        value = round(item['std']/total,4)
      temp_stdr_list.append(CommonListItem(date,value*100).__dict__)

    data['temp_stdr_list'] = temp_stdr_list
    pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  res.data = data
  return res

def temp_ot(dtype: int, res: ResponseBase):
  data = {'temp_ot_list':[]}
  r_key = f'temp_ot_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      temp_ot_list = []
      for i in temp_model.keys():
        condition = []
        condition.append(TempCraft.gmt_update >= get_startdate(dtype))
        condition.append(TempCraft.weld_type == int(i))
        db_data = session.query(TempCraft.weld_wt,TempCraft.weld_type).filter(and_(*condition)).all()
        # 计算超时
        if len(db_data)>0:
          l = np.array(db_data)[:,0]
          rest = calculate_ot(l,2)
          temp_ot_list.append(GroupListItem('超时',temp_model[i],rest[0]).__dict__)
          temp_ot_list.append(GroupListItem('未超时',temp_model[i],rest[1]).__dict__)
        else:
          temp_ot_list.append(GroupListItem('超时',temp_model[i],0).__dict__)
          temp_ot_list.append(GroupListItem('未超时',temp_model[i],0).__dict__)

      data['temp_ot_list'] = temp_ot_list
      if len(temp_ot_list) > 0:
        redis_session.set_redis_str(data,r_key, 60)
      pass
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def seed_lates_dist(dtype: int, res: ResponseBase):
  data = {'seed_lates_list': []}
  r_key = f'seed_lates_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      condition = []
      condition.append(SeedCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(SeedCraft.seed_lates).filter(and_(*condition)).all()
      seed_lates_list = []
      if len(db_data)>0:
        l = np.array(db_data)[:,0]
        # for key,value in interval_static(l).items():
        #   seed_lates_list.append(CommonFitListItem(key,value,0).__dict__)
        cso = CommonSticOp(l)
        cso.get_dist_fit(50)
        for item in cso.result:
          seed_lates_list.append(CommonFitListItem(item[0],item[1],round(item[2],4)).__dict__)
      data['seed_lates_list'] = seed_lates_list
      if len(seed_lates_list) > 0:
        redis_session.set_redis_str(data,r_key, 1)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def seed_wt_dist(dtype: int, res: ResponseBase):
  data = {'seed_wt_list': [],'mean':0,'total':0}
  r_key = f'seed_wt_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      condition = []
      condition.append(SeedCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(SeedCraft.seed_wt).filter(and_(*condition)).all()
      seed_wt_list = []
      if len(db_data)>0:
        l = np.array(db_data)[:,0]
        data['mean'] = round(np.mean(l),4)
        data['total'] = len(l)
        # for key,value in interval_static(l).items():
        #   seed_wt_list.append(CommonFitListItem(key,value,0).__dict__)
        cso = CommonSticOp(l)
        cso.get_dist_fit()
        for item in cso.result:
          seed_wt_list.append(CommonFitListItem(item[0],item[1],round(item[2],4)).__dict__)
      data['seed_wt_list'] = seed_wt_list
      if len(seed_wt_list) > 0:
        redis_session.set_redis_str(data,r_key, 1)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def seed_std(dtype: int, res: ResponseBase):
  data = {'seed_std_list': [],'total':0}
  r_key = f'seed_std_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      seed_std_list = []
      condition = []
      condition.append(SeedCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(SeedCraft.seed_std,func.count('*')).filter(and_(*condition)).group_by(SeedCraft.seed_std).order_by(SeedCraft.seed_std).all()
      for child in db_data:
        data['total'] += child[1]
      std_dict = {'1':'达标','2':'直径超标','3':'拉速超标','4':'两者都超标'}
      seed_std_list = mysql_init_data(db_data,std_dict,CommonListItem)
      data['seed_std_list'] = seed_std_list
      if len(seed_std_list) > 0:
        redis_session.set_redis_str(data,r_key, 1)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def seed_type_stic(dtype: int, res: ResponseBase):
  data = {'seed_type_list': [], 'total':0}
  r_key = f'seed_type_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      seed_type_list = []
      condition = []
      condition.append(SeedCraft.gmt_update >= get_startdate(dtype))
      condition.append(SeedCraft.seed_type <= 4)
      db_data = session.query(SeedCraft.seed_type,func.count('*')).filter(and_(*condition)).group_by(SeedCraft.seed_type).order_by(SeedCraft.seed_type).all()
      for child in db_data:
        data['total'] += child[1]
      # db_data = session.query(SeedCraft.seed_type,func.count(case(whens=((SeedCraft.seed_type.in_([1,2,3,4]),1),),else_=0))).filter(and_(*condition)).group_by(SeedCraft.seed_type).all()
      # sm_keys_list = list(seed_model.keys())
      # temp_keys_list = []
      # for item in db_data:
      #   temp_keys_list.append(f'{item[0]}')
      #   seed_type_list.append(CommonListItem(seed_model[f'{item[0]}'],item[1]).__dict__)
      
      # # 初始化未添加的内容
      # d_map = map(int,list(set(sm_keys_list).difference(set(temp_keys_list))))
      # d_set = sorted(list(d_map))
      # for i in d_set:
      #   seed_type_list.insert(sm_keys_list.index(f'{i}'),CommonListItem(seed_model[f'{i}'],0).__dict__)
      seed_type_list = mysql_init_data(db_data,seed_model,CommonListItem)
      data['seed_type_list'] = seed_type_list
      if len(seed_type_list) > 0:
        redis_session.set_redis_str(data,r_key, 60)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def seed_history_stdr(res: ResponseBase):
  data = {'seed_stdr_list':[]}
  try:
    seed_stdr_list = []
    search_col={'date':{'$gte':datetime.today()-timedelta(days=30)},'craft':'seed'}
    return_type={'_id':0,'craft':0}
    mg_data = mongo_session.select_all_collection('std_stic',search_col,return_type,sort_col='date')
    for item in mg_data:
      date = item['date'].strftime("%m-%d")
      total = item['std'] + item['l_o'] + item['s_o'] + item['b_o']
      value = 0
      if total != 0:
        value = round(item['std']/total,4)
      seed_stdr_list.append(CommonListItem(date,value*100).__dict__)
    data['seed_stdr_list'] = seed_stdr_list
    pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  res.data = data
  return res

def seed_ddvt_dist(dtype: int, res: ResponseBase):
  data = {'seed_ddvt_list': []}
  r_key = f'seed_ddvt_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      condition = []
      condition.append(SeedCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(SeedCraft.seed_ddvt).filter(and_(*condition)).all()
      seed_ddvt_list = []
      if len(db_data)>0:
        l = np.array(db_data)[:,0]
        # for key,value in interval_static(l,interv=10).items():
        #   seed_ddvt_list.append(CommonFitListItem(key,value,0).__dict__)
        cso = CommonSticOp(l)
        cso.get_dist_fit(.5)
        for item in cso.result:
          seed_ddvt_list.append(CommonFitListItem(item[0],item[1],round(item[2],4)).__dict__)
      data['seed_ddvt_list'] = seed_ddvt_list
      if len(seed_ddvt_list) > 0:
        redis_session.set_redis_str(data,r_key, 1)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def shoulder_len_dist(dtype: int, res: ResponseBase):
  data = {'shoulder_len_list': []}
  r_key = f'shoulder_len_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      condition = []
      condition.append(ShoulderCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(ShoulderCraft.shoulder_len).filter(and_(*condition)).all()
      shoulder_len_list = []
      if len(db_data)>0:
        l = np.array(db_data)[:,0]
        # for key,value in interval_static(l).items():
        #   shoulder_len_list.append(CommonFitListItem(key,value,0).__dict__)
        cso = CommonSticOp(l)
        cso.get_dist_fit(20)
        for item in cso.result:
          shoulder_len_list.append(CommonFitListItem(item[0],item[1],round(item[2],4)).__dict__)
      data['shoulder_len_list'] = shoulder_len_list
      if len(shoulder_len_list) > 0:
        redis_session.set_redis_str(data,r_key, 1)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def shoulder_wt_dist(dtype: int, res:ResponseBase):
  data = {'shoulder_wt_list': [], 'mean':0, 'total':0}
  r_key = f'shoulder_wt_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      condition = []
      condition.append(ShoulderCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(ShoulderCraft.shoulder_wt).filter(and_(*condition)).all()
      shoulder_wt_list = []
      if len(db_data)>0:
        l = np.array(db_data)[:,0]
        data['mean'] = round(np.mean(l),4)
        data['total'] = len(l)
        # for key,value in interval_static(l).items():
        #   shoulder_wt_list.append(CommonFitListItem(key,value,0).__dict__)
        cso = CommonSticOp(l)
        cso.get_dist_fit()
        for item in cso.result:
          shoulder_wt_list.append(CommonFitListItem(item[0],item[1],round(item[2],4)).__dict__)
      data['shoulder_wt_list'] = shoulder_wt_list
      if len(shoulder_wt_list) > 0:
        redis_session.set_redis_str(data,r_key, 1)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def shoulder_std(dtype: int, res: ResponseBase):
  data = {'shoulder_std_list': [],'total':0}
  r_key = f'shoulder_std_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      shoulder_std_list = []
      condition = []
      condition.append(ShoulderCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(ShoulderCraft.shoulder_std,func.count('*')).filter(and_(*condition)).group_by(ShoulderCraft.shoulder_std).order_by(ShoulderCraft.shoulder_std).all()
      for child in db_data:
        data['total'] += child[1]
      std_dict = {'0':'控制不达标','1':'控制达标'}
      shoulder_std_list = mysql_init_data(db_data,std_dict,CommonListItem)
      data['shoulder_std_list'] = shoulder_std_list
      if len(shoulder_std_list) > 0:
        redis_session.set_redis_str(data,r_key, 60)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def shoulder_type_stic(dtype: int, res: ResponseBase):
  data = {'shoulder_type_list': [], 'total': 0}
  r_key = f'shoulder_type_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      shoulder_type_list = []
      condition = []
      condition.append(ShoulderCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(ShoulderCraft.shoulder_type,func.count('*')).filter(and_(*condition)).group_by(ShoulderCraft.shoulder_type).order_by(ShoulderCraft.shoulder_type).all()
      for child in db_data:
        data['total'] += child[1]
      shoulder_type_list = mysql_init_data(db_data,shoulder_model,CommonListItem)
      data['shoulder_type_list'] = shoulder_type_list
      if len(shoulder_type_list) > 0:
        redis_session.set_redis_str(data,r_key, 1)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def shoulder_history_stdr(res: ResponseBase):
  data = {'shoulder_stdr_list':[]}
  try:
    shoulder_stdr_list = []
    search_col = {'date':{'$gte':datetime.today()-timedelta(days=30)},'craft':'shoulder'}
    return_type = {'_id':0,'craft':0}
    mg_data = mongo_session.select_all_collection('std_stic',search_col,return_type,sort_col='date')
    for item in mg_data:
      date = item['date'].strftime("%m-%d")
      total = item['std'] + item['std_o']
      value = 0
      if total != 0:
        value = round(item['std']/total,4)
      shoulder_stdr_list.append(CommonListItem(date,value*100).__dict__)
    data['shoulder_stdr_list'] = shoulder_stdr_list
    pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  res.data = data
  return res

def shoulder_dvt_dist(dvt: str, dtype: int, res: ResponseBase):
  data = {'shoulder_dvt_list': []}
  r_key = f'shoulder_dvt_list_{dvt}_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      condition = []
      condition.append(ShoulderCraft.gmt_update >= get_startdate(dtype))
      db_data = []
      if dvt == 'l':
        db_data = session.query(ShoulderCraft.shoulder_ldvt).filter(and_(*condition)).all()
      if dvt == 'd':
        db_data = session.query(ShoulderCraft.shoulder_ddvt).filter(and_(*condition)).all()
      shoulder_dvt_list = []
      if len(db_data)>0:
        l = np.array(db_data)[:,0]
        # for key,value in interval_static(l).items():
        #   shoulder_dvt_list.append(CommonListItem(key,value).__dict__)
        cso = CommonSticOp(l)
        if dvt == 'd':
          cso.get_dist_fit(2)
        elif dvt == 'l':
          cso.get_dist_fit(10)

        for item in cso.result:
          shoulder_dvt_list.append(CommonFitListItem(item[0],item[1],round(item[2],4)).__dict__)
      data['shoulder_dvt_list'] = shoulder_dvt_list
      if len(shoulder_dvt_list) > 0:
        redis_session.set_redis_str(data,r_key, 1)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def shoulder_pd_dist(dtype: int,res: ResponseBase):
  data = {'shoulder_pd_list': []}
  r_key = f'shoulder_pd_list_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      condition = []
      condition.append(ShoulderCraft.gmt_update >= get_startdate(dtype))
      db_data = session.query(ShoulderCraft.shoulder_powerdec).filter(and_(*condition)).all()
      shoulder_pd_list = []
      if len(db_data)>0:
        l = np.array(db_data)[:,0]
        cso = CommonSticOp(l)
        cso.get_dist(5)
        for item in cso.result:
          shoulder_pd_list.append(CommonListItem(item[0],item[1]).__dict__)
      data['shoulder_pd_list'] = shoulder_pd_list
      if len(shoulder_pd_list) > 0:
        redis_session.set_redis_str(data,r_key, 1)
      pass
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def craft_off_prop(dtype: int,craft: str,res: ResponseBase):
  data = {'seed_off':0,'seed_total':0,'shoulder_off':0,'shoulder_total':0}
  r_key = f'craft_off_{craft}_{dtype}'
  session = mysql_session.session()
  try:
    if redis_session.exists(r_key):
      data = redis_session.get_redis_str(r_key)
      pass
    else:
      # 查询数据库
      condition = []
      db_data = []
      if craft == 'shoulder':
        condition.append(ShoulderCraft.gmt_update >= get_startdate(dtype))
        db_data = session.query(ShoulderCraft.shoulder_off,func.count('*')).filter(and_(*condition)).group_by(ShoulderCraft.shoulder_off).order_by(ShoulderCraft.shoulder_off).all()
        if len(db_data)>0:
          l = np.array(db_data)[:,1]
          data['shoulder_off'] = int(l[1])
          data['shoulder_total'] = int(l[0] + l[1])

      if craft == 'seed':
        condition.append(SeedCraft.gmt_update >= get_startdate(dtype))
        db_data = session.query(SeedCraft.seed_off,func.count('*')).filter(and_(*condition)).group_by(SeedCraft.seed_off).order_by(SeedCraft.seed_off).all()
        if len(db_data)>0:
          l = np.array(db_data)[:,1]
          data['seed_off'] = int(l[1])
          data['seed_total'] = int(l[0] + l[1])
      
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  session.close()
  res.data = data
  return res

def single_shoulder_history_len(furnace_id, res: ResponseBase):
  data = {'single_shoulder_len':[]}
  try:
    single_shoulder_len = []
    search_col = {'craft':'shoulder','gmt_update':{'$gte':datetime.today()-timedelta(days=30)}}
    return_type = {'_id':0,'gmt_update':1,'shoulder_len':1}
    mg_data = mongo_session.select_all_collection(f'{furnace_id}_craft',search_col,return_type,sort_col='gmt_update')
    for item in mg_data:
      date = item['gmt_update'].strftime("%m-%d %H:%M")
      value = item['shoulder_len']
      single_shoulder_len.append(CommonListItem(date,value).__dict__)
    data['single_shoulder_len'] = single_shoulder_len
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  res.data = data
  return res

def single_seed_history_lates(furnace_id, res: ResponseBase):
  data = {'single_seed_lates':[]}
  try:
    single_seed_lates = []
    search_col = {'craft':'seed','gmt_update':{'$gte':datetime.today()-timedelta(days=30)}}
    return_type = {'_id':0,'gmt_update':1,'seed_lates':1}
    mg_data = mongo_session.select_all_collection(f'{furnace_id}_craft',search_col,return_type,sort_col='gmt_update')
    for item in mg_data:
      date = item['gmt_update'].strftime("%m-%d %H:%M")
      value = item['seed_lates']
      single_seed_lates.append(CommonListItem(date,value).__dict__)
    data['single_seed_lates'] = single_seed_lates
  except Exception as e:
    res.error(Error.SERVER_EXCEPTION)
    logger.error(e)
    pass
  res.data = data
  return res





def get_startdate(type:int):
  now = date.today()
  if type == 1:
    return datetime(now.year, now.month, 1)
  elif type == 2:
    return datetime(now.year, now.month, now.day, 0)
  else:
    # 默认当月
    return datetime(now.year, now.month, 1)

def gr_sec(sec):
  return random.randint(0,59)+int(sec)
