import json
from datetime import datetime, date, timedelta
from sqlalchemy import and_, desc, func, distinct
from common.entity import ResponseBase, Error
from common.mvt_req import ReqModifyServer
from common.mvt_resp import *
from common.response import *
from config import mysql_session, redis_session, logger
from models.models import ServerList, FurnaceList


def mod_server(item: ReqModifyServer, res: ResponseBase):
    session = mysql_session.session()
    try:
        # 删除相关缓存
        scan = redis_session.scan(match='server_list*')
        for i in scan[1]:
            redis_session.delete(i)
        data = session.query(ServerList).filter(
            ServerList.server_ip == item.server_ip).first()
        if data == None:
            sl = ServerList()
            sl.gmt_create = datetime.now()
            sl.setData(item)
            session.add(sl)
            session.commit()
            res.succ()
            pass
        else:
            data.setData(item)
            session.commit()
            res.succ()
            pass
    except Exception as e:
        res.error(Error.OPTION_ERR)
        logger.error(e)
        pass
    session.close()  # 关闭session
    return res


def get_server_lists(res: ResponseBase, ipt: str, idx: int, size: int):
    session = mysql_session.session()
    data = CommonList()
    r_key = "server_lists_"+ipt
    try:
        if redis_session.exists(r_key):
            # data = redis_session.hash2obj(data.__dict__, r_key)
            data = redis_session.get_redis_str(r_key)
            pass
        else:
            ipt = '%{}%'.format(ipt)
            db_data = session.query(ServerList).filter(
                and_(ServerList.server_ip.like(ipt), ServerList.state > 0)).all()
            for i in db_data:
                re = RespServerList(i).__dict__
                data.list.append(re)
            data.total = len(db_data)
            if len(data.list) > 0:
                # redis_session.set_redis(data.__dict__, r_key, 60*60)
                redis_session.set_redis_str(data.__dict__, r_key, 60*60)
            pass
        res.data = data
    except Exception as e:
        res.error(Error.OPTION_ERR)
        logger.error(e)
        pass

    session.close()  # 关闭session
    return res


def get_furnace_lists(res: ResponseBase, id: str, series: str, status: str, idx: int, size: int):
    session = mysql_session.session()
    data = CommonList()
    # r_key = "furnace_lists_{}_{}".format(series, id)
    r_key = f'furnace_lists_{series}_{id}'
    try:
        if redis_session.exists(r_key):
            data = redis_session.get_redis_str(r_key)
            pass
        else:
            # 多条件查询
            condition = []
            if series != '':
                condition.append(FurnaceList.furnace_series == series)
            if id != '':
                condition.append(FurnaceList.furnace_id == int(id))
            if status != '':
                condition.append(FurnaceList.furnace_state == int(status))
            db_data = session.query(FurnaceList).filter(and_(*condition)).all()
            for i in db_data:
                re = RespFurnaceList(i).__dict__
                data.list.append(re)
            data.total = len(db_data)
            if len(data.list) > 0:
                redis_session.set_redis_str(data.__dict__, r_key, 60)
            pass
        res.data = data
    except Exception as e:
        res.error(Error.OPTION_ERR)
        logger.error(e)
        pass

    session.close()  # 关闭session
    return res
