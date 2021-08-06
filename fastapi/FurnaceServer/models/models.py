from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, Date, DateTime, TIMESTAMP,Float
import time
from common.anls_req import ReqTempProcess, ReqSeedProcess, ReqShoulderProcess, ReqCylProcess
from datetime import *

from pymongo import mongo_client

# from config import Base
Base = declarative_base()

class ServerList(Base):
    """[server_list table]

    Args:
        key 自增ID
        gmt_create 创建时间
        gmt_modified 修改时间
        server_ip ip地址
        server_name 名称
        server_cpu cpu
        server_os 操作系统
        server_disk 硬盘
        state 状态 0不可用 1可用
    """
    __tablename__ = 'server_list'
    key = Column(BigInteger, primary_key=True, autoincrement=True)
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime)
    server_ip = Column(String, nullable=False, default='')
    server_name = Column(String, nullable=False, default='')
    server_cpu = Column(String, nullable=False, default='')
    server_os = Column(String, nullable=False, default='')
    server_disk = Column(String, nullable=False, default='')
    state = Column(Integer, nullable=False, default=0)

    def setData(self, data: object):
        self.server_ip = data.server_ip
        self.state = data.state
        if(data.server_name != None):
            self.server_name = data.server_name  # 非None添加
        if(data.server_cpu != None):
            self.server_cpu = data.server_cpu
        if(data.server_os != None):
            self.server_os = data.server_os
        if(data.server_disk != None):
            self.server_disk = data.server_disk

class FurnaceList(Base):
    """[furnace_list table]

    Args:
        key 自增ID
        gmt_create 创建时间
        gmt_modified 修改时间
        furnace_id 炉台ID
        furnace_series 系列
        furnace_state 炉台状态
        running_time 运行时间
        server_ip 服务器ip

    """
    __tablename__ = 'furnace_list'
    key = Column(BigInteger, primary_key=True, autoincrement=True)
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime)
    furnace_id = Column(Integer, nullable=False, default=0)
    furnace_series = Column(String, nullable=False, default='')
    furnace_state = Column(Integer, nullable=False, default=0)
    running_time = Column(Integer, nullable=False, default=0)
    server_ip = Column(String, nullable=False, default='')

    def setData(self, data: object, host: str):
        self.furnace_id = data.furnace_id
        self.furnace_series = data.furnace_series
        self.furnace_state = data.furnace_state
        self.server_ip = host
        if(data.running_time != None):
            self.running_time = data.running_time

class BrokenHistoryResult(Base):
    """[broken_history_result]
        key 自增ID
        gmt_create 创建时间
        gmt_modified 修改时间
        date 统计时间
        server_ip 服务器地址
        diameter_broken_nums
        shouldering_broken_nums 
    """
    __tablename__ = 'broken_history_result'
    key = Column(BigInteger, primary_key=True, autoincrement=True)
    gmt_update = Column(DateTime)
    date = Column(Date, nullable=False, default='1970-01-01')
    server_ip = Column(String, nullable=False, default='')
    diameter_broken_nums = Column(Integer, nullable=False, default=0)
    shouldering_broken_nums = Column(Integer, nullable=False, default=0)

    def setData(self, data: object, host: str):
        self.date = data.date
        self.diameter_broken_nums = data.diameter_broken_nums
        self.shouldering_broken_nums = data.shouldering_broken_nums
        self.server_ip = host

class TempCraft(Base):
    """[temp_craft]
    Args:
        key 自增ID
        gmt_create 创建时间
        gmt_update 工艺过程更新时间
        server_ip 炉台服务器ip地址
        furnace_id 炉台id
        weld_wt 稳温工时 h
        weld_wt 稳温类型 :
            1：初始复投稳温
            2：初始稳温
            3：复投稳温
            4：引断稳温
            5：扩断稳温
            6：断苞稳温
        weld_std 是否达标 
    """
    __tablename__ = "temp_craft"
    key = Column(BigInteger,primary_key=True,autoincrement=True)
    gmt_create = Column(DateTime)
    gmt_update = Column(DateTime)
    server_ip = Column(String, nullable=False, default='')
    furnace_id = Column(String, nullable=False, default='')
    weld_wt = Column(Float, nullable=False, default=0)
    weld_type = Column(Integer, nullable=False, default=0)
    weld_std = Column(Integer, nullable=False, default=0)

    def setData(self, data: ReqTempProcess):
      self.gmt_create = datetime.now()
      self.gmt_update = data.update_time
      self.server_ip = data.server_ip
      self.furnace_id = data.furnace_id
      self.weld_wt = data.weld_wt
      self.weld_type = data.weld_type
      self.weld_std = int(data.weld_std)
    
    def chg2mongo(self):
      mongo_dict = {}
      mongo_dict['gmt_update'] = self.gmt_update
      mongo_dict['weld_wt'] = self.weld_wt
      mongo_dict['weld_type'] = self.weld_type
      mongo_dict['weld_std'] = self.weld_std
      mongo_dict['craft'] = 'weld'
      return mongo_dict
 
class SeedCraft(Base):
    """[seed_craft]
    Args:
        key 自增ID
        gmt_create 创建时间
        gmt_update 工艺过程更新时间
        server_ip 炉台服务器ip地址
        furnace_id 炉台id
        seed_wt 引晶工时 h
        seed_lates 末期拉速 mm/hr
        seed_type 引晶类型 
            1：引断二次引晶
            2：熔料后引晶
            3：断苞后引晶
            4：扩断后引晶  
        seed_diam 引晶直径 mm
        seed_ddvt 引晶后段100mm直径极差 mm
        seed_std 是否达标
    """
    __tablename__ = "seed_craft"
    key = Column(BigInteger,primary_key=True,autoincrement=True)
    gmt_create = Column(DateTime)
    gmt_update = Column(DateTime)
    server_ip = Column(String, nullable=False, default='')
    furnace_id = Column(String, nullable=False, default='')
    seed_wt = Column(Float, nullable=False, default=0)
    seed_lates = Column(Float, nullable=False, default=0)
    seed_type = Column(Integer, nullable=False, default=0)
    seed_diam = Column(Float, nullable=False, default=0)
    seed_ddvt = Column(Float, nullable=False, default=0)
    seed_std = Column(Integer, nullable=False, default=0)
    seed_off = Column(Integer,nullable=False, default=0)

    def setData(self, data: ReqSeedProcess):
      self.gmt_create = datetime.now()
      self.gmt_update = data.update_time
      self.server_ip = data.server_ip
      self.furnace_id = data.furnace_id
      self.seed_wt = data.seed_wt
      self.seed_lates = data.seed_lates
      self.seed_type = data.seed_type
      self.seed_diam = data.seed_diam
      self.seed_ddvt = data.seed_ddvt
      self.seed_std = data.seed_std
      self.seed_off = int(data.seed_off)

    def chg2mongo(self):
      mongo_dict = {}
      mongo_dict['gmt_update'] = self.gmt_update
      mongo_dict['seed_wt'] = self.seed_wt
      mongo_dict['seed_lates'] = self.seed_lates
      mongo_dict['seed_type'] = self.seed_type
      mongo_dict['seed_diam'] = self.seed_diam
      mongo_dict['seed_ddvt'] = self.seed_ddvt
      mongo_dict['seed_std'] = self.seed_std
      mongo_dict['seed_off'] = self.seed_off
      mongo_dict['craft'] = 'seed'
      return mongo_dict

class ShoulderCraft(Base):
    """[summary]

    Args:
        key 自增ID
        gmt_create 创建时间
        gmt_update 工艺过程更新时间
        server_ip 炉台服务器ip地址
        furnace_id 炉台id
        shoulder_wt 放肩工时 h
        shoulder_len 放肩长度 h
        shoulder_ddvt 放肩直径偏差 mm
        shoulder_ldvt 放肩长度偏差 mm
        shoulder_type = 放肩类型
           1：熔料后扩肩
           2：断苞后扩肩
           3：扩断后二次扩肩
    """
    __tablename__ = "shoulder_craft"
    key = Column(BigInteger,primary_key=True,autoincrement=True)
    gmt_create = Column(DateTime)
    gmt_update = Column(DateTime)
    server_ip = Column(String, nullable=False, default='')
    furnace_id = Column(String, nullable=False, default='')
    shoulder_wt = Column(Float, nullable=False, default=0)
    shoulder_len = Column(Float, nullable=False, default=0)
    shoulder_ddvt = Column(Float, nullable=False, default=0)
    shoulder_ldvt = Column(Float, nullable=False, default=0)
    shoulder_powerdec = Column(Float, nullable=False, default=0)
    shoulder_type = Column(Integer, nullable=False, default=0)
    shoulder_std = Column(Integer, nullable=False, default=0)
    shoulder_off = Column(Integer, nullable=False, default=0)

    def setData(self, data: ReqShoulderProcess):
      self.gmt_create = datetime.now()
      self.gmt_update = data.update_time
      self.server_ip = data.server_ip
      self.furnace_id = data.furnace_id
      self.shoulder_wt = data.shoulder_wt
      self.shoulder_len = data.shoulder_len
      self.shoulder_ddvt = data.shoulder_ddvt
      self.shoulder_ldvt = data.shoulder_ldvt
      self.shoulder_powerdec = data.shoulder_powerdec
      self.shoulder_type = data.shoulder_type
      self.shoulder_std = int(data.shoulder_std)
      self.shoulder_off = int(data.shoulder_off)
    
    def chg2mongo(self):
      mongo_dict = {}
      mongo_dict['gmt_update'] = self.gmt_update
      mongo_dict['shoulder_wt'] = self.shoulder_wt
      mongo_dict['shoulder_len'] = self.shoulder_len
      mongo_dict['shoulder_ddvt'] = self.shoulder_ddvt
      mongo_dict['shoulder_ldvt'] = self.shoulder_ldvt
      mongo_dict['shoulder_powerdec'] = self.shoulder_powerdec
      mongo_dict['shoulder_type'] = self.shoulder_type
      mongo_dict['shoulder_std'] = self.shoulder_std
      mongo_dict['shoulder_off'] = self.shoulder_off
      mongo_dict['craft'] = 'shoulder'
      return mongo_dict

class CylCraft(Base):

    __tablename__ = "cyl_craft"
    key = Column(BigInteger,primary_key=True,autoincrement=True)
    gmt_create = Column(DateTime)
    gmt_update = Column(DateTime)
    server_ip = Column(String, nullable=False, default='')
    furnace_id = Column(String, nullable=False, default='')
    cyl_nums = Column(Integer, nullable=False, default=0)
    cyl_header_lates = Column(Float, nullable=False, default=0)
    cyl_len = Column(Float, nullable=False, default=0)
    cyl_off = Column(Integer,nullable=False, default=0)

    def setData(self, data: ReqCylProcess):
      self.gmt_create = datetime.now()
      self.gmt_update = data.update_time
      self.server_ip = data.server_ip
      self.furnace_id = data.furnace_id
      self.cyl_nums = data.cyl_nums
      self.cyl_header_lates = data.cyl_header_lates
      self.cyl_len = data.cyl_len
      self.cyl_off = int(data.cyl_off)

    def chg2mongo(self):
      mongo_dict = {}
      mongo_dict['gmt_update'] = self.gmt_update
      mongo_dict['cyl_nums'] = self.cyl_nums
      mongo_dict['cyl_header_lates'] = self.cyl_header_lates
      mongo_dict['cyl_len'] = self.cyl_len
      mongo_dict['cyl_off'] = self.cyl_off
      mongo_dict['craft'] = 'cyl'
      return mongo_dict
