import json
import time
from datetime import datetime, date, timedelta
from sqlalchemy import and_, desc, func, distinct
from common.entity import ResponseBase, Error, list_model, dict_model,dict_model_index
from common.response import CommonListItem, mysql_init_data
from common.mvt_resp import *
from common.mvt_req import ReqUpdateFurState, ReqUpdateHistoryBroken, ReqUpdateSeriesBroken
from config import mysql_session, redis_session, logger
from utils.common import str2int, dict2obj, s_reqs
from models.models import ServerList, FurnaceList, BrokenHistoryResult


def fur_state(item: ReqUpdateFurState, res: ResponseBase, host: str):
    session = mysql_session.session()
    try:
        data = session.query(FurnaceList).filter(
            FurnaceList.furnace_id == item.furnace_id, FurnaceList.furnace_series == item.furnace_series).first()
        if data == None:
            fl = FurnaceList()
            fl.gmt_create = datetime.now()
            fl.setData(item, host)
            session.add(fl)
            session.commit()
            res.succ()
            pass
        else:
            data.setData(item, host)
            session.commit()
            res.succ()
            pass

    except Exception as e:
        res.error(Error.OPT_ERR)
        logger.error(e)
        pass
    session.close()
    return res.__dict__


def up_history_broken(item: ReqUpdateHistoryBroken, res: ResponseBase, host: str):
    session = mysql_session.session()
    try:
        data = session.query(BrokenHistoryResult).filter(and_(
            BrokenHistoryResult.date == item.date, BrokenHistoryResult.server_ip == host)).first()
        if data == None:
            bhr = BrokenHistoryResult()
            bhr.gmt_update = datetime.now()
            bhr.setData(item, host)
            session.add(bhr)
            session.commit()
            res.succ()
            pass
        else:
            data.setData(item, host)
            session.commit()
            res.succ()
            pass
    except Exception as e:
        res.error(Error.OPT_ERR)
        logger.error(e)
        pass
    # 删除相关缓存
    scan = redis_session.scan(match='history_broken*')
    for i in scan[1]:
        redis_session.delete(i)
    session.close()
    return res.__dict__


def up_series_broken(item: ReqUpdateSeriesBroken, res: ResponseBase):
    try:
        if item.type > 0:
            redis_session.hset(item.r_name_list[item.type-1],
                   item.series, item.broken_nums)
            res.succ()
            pass
        else:
            res.error(Error.PARAM_ERR)
            pass
    except Exception as e:
        res.error(Error.OPT_ERR)
        logger.error(e)
        pass
    return res.__dict__


def series_list(res: ResponseBase):
    session = mysql_session.session()
    data = {'series_list': []}
    r_key = 'series_list'
    try:
        if redis_session.exists(r_key):
            data = redis_session.get_redis_str(r_key)
            pass
        else:
            db_data = session.query(FurnaceList.furnace_series, func.count(
                '*').label("count")).group_by(FurnaceList.furnace_series).all()
            series_list = []
            for i in db_data:
                series_list.append(i[0])
            series_list.sort(key=None, reverse=False)
            data['series_list'] = series_list
            if len(series_list) > 0:
                redis_session.set_redis_str(data,r_key, 60*60*24)
            pass
        pass
    except Exception as e:
        res.error(Error.SERVER_EXCEPTION)
        logger.error(e)
        pass
    session.close()
    res.data = data
    return res.__dict__


def current_fur_list(series: str, res: ResponseBase):
    session = mysql_session.session()
    data = {'fur_list':[],'series':''}
    r_key = f'current_fur_list_{series}'
    try:
        if redis_session.exists(r_key):
            data = redis_session.get_redis_str(r_key)
            pass
        else:
            db_data = session.query(FurnaceList.furnace_id, FurnaceList.furnace_state).filter(
                FurnaceList.furnace_series == series).order_by(FurnaceList.furnace_id).all()
            fur_list = []
            if len(db_data) > 0:
                for i in db_data:
                    fur_list.append(CurrentFurList(series+str(i[0]), i[1]).__dict__)
            data['fur_list'] = fur_list
            data['series'] = series
            if len(fur_list)>0:
                redis_session.set_redis_str(data, r_key, 30)
                pass
            else:
                res.error(Error.NO_DATA)
                pass
    except Exception as e:
        res.error(Error.SERVER_EXCEPTION)
        logger.error(e)
        pass
    session.close()
    res.data = data
    return res.__dict__


def fur_result(furnace_id: str, img_idx: str,furnace_state:str,model_name:str, res: ResponseBase):
    session = mysql_session.session()
    # r_key = 'fur_result_{}_{}'.format(furnace_id, img_idx)
    # 不做缓存
    try:
        # if r.exists(r_key):
        #     data = {'img_origin': '', 'img_detection': '','final_rst':'','img_nums':''}
        #     res.data = hash2obj(data, r_key)
        #     pass
        # 根据furnace_id寻找 A1 服务器地址
        # else:
        series = furnace_id[0]
        id = furnace_id[1:]
        db_data = session.query(FurnaceList.server_ip).filter(
            FurnaceList.furnace_id == id, FurnaceList.furnace_series == series).first()
        server_ip = db_data[0]
        addr = ''
        if img_idx == '':
            addr = 'http://{}:5000/furnace_detection_first?device_id={}&device_state={}&model_name={}'.format(
                server_ip, furnace_id,furnace_state,model_name)
        else:
            addr = 'http://{}:5000/furnace_detection?device_id={}&img_idx={}&device_state={}&model_name={}'.format(
                server_ip, furnace_id, img_idx,furnace_state,model_name)
        resp = s_reqs.get(addr, timeout=5).json()
        res.data = resp
        # set_redis(resp, r_key, 60)
        pass
    except Exception as e:
        res.error(Error.SERVER_EXCEPTION)
        logger.error(e)
        pass
    session.close()
    return res.__dict__


def server_list(res: ResponseBase):
    session = mysql_session.session()
    data = {'server_list': []}
    r_key = 'server_list'
    try:
        if redis_session.exists(r_key):
            data = redis_session.get_redis_str(r_key)
            pass
        else:
            db_data = session.query(ServerList.server_ip).filter(
                ServerList.state > 0).all()
            server_list = []
            for i in db_data:
                server_list.append(i[0])
            data['server_list'] = server_list
            if len(server_list) > 0:
                redis_session.set_redis_str(data, r_key, 60*60*24)
            else:
                res.code = 1
            pass
    except Exception as e:
        res.error(Error.SERVER_EXCEPTION)
        logger.error(e)
        pass
    session.close()
    res.data = data
    return res.__dict__


def server_state(server_ip: str, res: ResponseBase):
    data = {'gpu_info':[],'memory_info':{},'disk_info':{},'cpu_info':{}}
    r_key = f'server_state_{server_ip}'
    try:
        if redis_session.exists(r_key):
            data = redis_session.get_redis_str(r_key)
            pass
        else:
            addr = 'http://{}:5000/server_status'.format(server_ip)
            resp = s_reqs.get(addr, timeout=5)
            res_obj = dict2obj(resp.json())
            data['cpu_info'] = CpuInfo(res_obj.cpu_info).__dict__
            data['memory_info'] = MemoryInfo(res_obj.memory_info).__dict__
            data['disk_info'] = DiskInfo(res_obj.disk_info).__dict__
            for item in res_obj.gpu_info:
                data['gpu_info'].append(GpuInfo(item).__dict__)
            redis_session.set_redis_str(data, r_key, 31)
        res.data = data
    except Exception as e:
        res.error(Error.SERVER_EXCEPTION)
        # logger.error(e)
        pass
    return res.__dict__


def model_state(server_ip: str, res: ResponseBase):
    data = {'model_list': []}
    r_key = f'model_list_{server_ip}'
    try:
        if redis_session.exists(r_key):
            data = redis_session.get_redis_str(r_key)
            pass
        else:
            addr = 'http://{}:5000/model_status'.format(server_ip)
            resp = s_reqs.get(addr, timeout=5)
            res_dict = resp.json()
            model_list = []
            for key in res_dict:
                if key in dict_model_index.keys():
                    model_list.append(RespModelState(key, dict_model_index.get(key), res_dict.get(key)).__dict__)
                continue
            model_list.sort(key=lambda x: x['key'], reverse=False)
            data['model_list'] = model_list
            if len(model_list) > 0:
                redis_session.set_redis_str(data, r_key, 30)
            pass
        res.data = data
    except Exception as e:
        res.error(Error.SERVER_EXCEPTION)
        logger.error(e)
        pass
    return res.__dict__


def online_fur(res: ResponseBase):
    session = mysql_session.session()
    data = {'online_list':[]}
    r_key = 'online_list'
    try:
        if redis_session.exists(r_key):
            data = redis_session.get_redis_str(r_key)
            pass
        else:
            db_data = session.query(FurnaceList.furnace_state, func.count(
                '*').label("count")).filter(FurnaceList.furnace_state < 99).group_by(FurnaceList.furnace_state).order_by(FurnaceList.furnace_state).all()
            # dm_keys_list = list(dict_model.keys())
            # temp_keys_list = []
            # for item in db_data:
            #     temp_keys_list.append(f'{item[0]}')
            #     data.online_list.append(CommonListItem(dict_model[f'{item[0]}'], item[1]).__dict__)
            # d_map = map(int,list(set(dm_keys_list).difference(set(temp_keys_list))))
            # d_set = sorted(list(d_map))
            # for i in d_set:
            #     data.online_list.insert(dm_keys_list.index(f'{i}'),CommonListItem(dict_model[f'{i}'],0).__dict__)
            online_list = mysql_init_data(db_data,dict_model,CommonListItem)
            data['online_list'] = online_list
            if len(online_list) > 0:
                redis_session.set_redis_str(data, r_key, 60)
            pass
    except Exception as e:
        res.error(Error.SERVER_EXCEPTION)
        logger.error(e)
        pass
    session.close()
    res.data = data
    return res.__dict__


def history_broken(type: int, res: ResponseBase):
    session = mysql_session.session()
    data = {'broken_list':[]}
    r_key = f'history_broken_{type}'
    try:
        if redis_session.exists(r_key):
            data = redis_session.get_redis_str(r_key)
            pass
        else:
            dt_ago = (datetime.now()-timedelta(days=30)).date()
            if type == '1':  # shouldering
                db_data = session.query(BrokenHistoryResult.date, func.sum(BrokenHistoryResult.shouldering_broken_nums).label("count")).filter(
                    BrokenHistoryResult.date >= dt_ago).group_by(BrokenHistoryResult.date).order_by(BrokenHistoryResult.date).all()
            elif type == '2':
                db_data = session.query(BrokenHistoryResult.date, func.sum(BrokenHistoryResult.diameter_broken_nums).label("count")).filter(
                    BrokenHistoryResult.date >= dt_ago).group_by(BrokenHistoryResult.date).order_by(BrokenHistoryResult.date).all()
            else:
                db_data = []
                pass
            broken_list = []
            for i in db_data:
                broken_list.append(CommonListItem(
                    str(i[0]), int(i[1])).__dict__)
            data['broken_list'] = broken_list
            if len(broken_list) > 0:
                redis_session.set_redis_str(data, r_key, 60*60*2)
    except Exception as e:
        res.error(Error.SERVER_EXCEPTION)
        logger.error(e)
        pass
    session.close()
    res.data = data
    return res.__dict__


# def series_broken(type: int, res: ResponseBase):
#     session = mysql_session.session()
#     data = RespSeriesBroken()
#     r_name_list = ['broken_shouldering', 'broken_diameter']
#     try:
#         res_dict = redis_session.get_session().hgetall(r_name_list[type-1])
#         for key in res_dict:
#             data.series_brokens.append(
#                 CommonListItem(key, res_dict[key]).__dict__)
#         data.series_brokens.sort(key=lambda x: x['item'], reverse=False)
#         pass
#     except Exception as e:
#         res.error(Error.SERVER_EXCEPTION)
#         logger.error(e)
#         pass
#     res.data = data
#     return res.__dict__


# def my_test(res:ResponseBase):
#     try:
#         addr = 'http://127.0.0.1:8000/test?name=wc'
#         resp = s.get(addr,timeout=3).json()
#         res.data = resp
#         pass
#     except Exception as e:
#         res.error(Error.SERVER_EXCEPTION)
#         logger.error(e)
#         pass
#     return res.__dict__
