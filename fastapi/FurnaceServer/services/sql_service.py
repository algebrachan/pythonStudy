from utils.mysql import db_session
from sqlalchemy import and_, desc
from models.models import DetectionResult
from utils.common import dict2obj
from utils.log import logger
from datetime import datetime, date, timedelta
import requests


def add_diameter_detection_result():
    """ 更新每天 测试结果
    """
    session = db_session()
    try:
        # 请求的url 和 类型是可以 提取共用的
        r = requests.get('http://10.50.63.63:5000/today_detection')
        res = dict2obj(r.json())
        # 根据时间查询数据库
        data = session.query(DetectionResult).filter(
            and_(DetectionResult.date == res.date, DetectionResult.type == 2)).first()

        if data == None:
            # 若没有该条数据 就新增
            dr = DetectionResult()
            dr.setData(res, 2)
            session.add(dr)
            session.commit()
            pass
        else:
            # 有数据 就更新
            data.setData(res, 2)
            session.commit()
            pass
    except Exception as e:
        logger.error(e)
        pass
    session.close()  # 关闭session


def get_one_detection_result(date: str, type: int):
    """
    param:date 查询日期
    param:type 查询类型 1 shoulder 2 diameter
    """
    session = db_session()
    data = None
    try:
        data = session.query(DetectionResult).filter(
            and_(DetectionResult.date <= date, DetectionResult.type == type)).order_by(desc(DetectionResult.date)).first()
        pass
    except Exception as e:
        logger.error(e)
        pass
    session.close()
    return data


def get_history_broken_nums(type: int, days: int):
    """
    param:type 查询类型 1 shoulder 2 diameter
    param:days 多少天的时间
    """
    session = db_session()
    data = None
    try:
        # 10天前的数据
        dt_ago = (datetime.now()-timedelta(days=days)).date()
        data = session.query(DetectionResult).filter(
            and_(DetectionResult.type == type, DetectionResult.date >= dt_ago)).order_by(DetectionResult.date).all()
        pass
    except Exception as e:
        logger.error(e)
        pass
    session.close()
    return data
