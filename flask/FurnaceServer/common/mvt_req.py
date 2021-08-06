from pydantic import BaseModel, constr, validator
from typing import Optional
import re


class ReqModifyServer(BaseModel):
    """修改服务器信息请求体
    """
    server_ip: str  # 服务器ip地址 必填
    server_name: Optional[str] = None  # 可选，
    server_cpu: Optional[str] = None
    server_os: Optional[str] = None
    server_disk: Optional[str] = None
    state: int = 1  # 服务器状态 0不可用 1可用 设置0为删除


class ReqUpdateFurState(BaseModel):
    """ 更新炉台状态
    """
    furnace_id: int  # 炉台ID必填
    furnace_series: str
    furnace_state: int = 0  # 默认0为空闲
    running_time: int = 0
    furnace_host: Optional[str] = None  # 可选



class ReqUpdateHistoryBroken(BaseModel):
    """ 更新断苞历史数据
    """ 
    # 1：放肩 2：等径
    date: str  # 统计日期 必填
    diameter_broken_nums: int = 0  # 检出等径断苞数量
    shouldering_broken_nums: int = 0  # 检出扩肩断苞数量
    server_ip:Optional[str] = None # 可选


class ReqUpdateSeriesBroken(BaseModel):
    """ 更新当日系列断苞统计
    """
    type: int = 0  # 类型 1：放肩 2：等径
    series: str  # 系列名
    broken_nums: int = 0  # 检出断苞数量
    r_name_list: list = ['broken_shouldering', 'broken_diameter']


