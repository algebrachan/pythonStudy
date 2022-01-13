from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReqUpRealtimeServer(BaseModel):
  """更新服务器实时数据"""
  server_ip: Optional[str] = None   # 可选
  cpu_info: dict = {}               # cpu信息
  memory_info: dict = {}            # 内存信息
  disk_info: dict = {}              # 磁盘信息
  gpu_info: list = []               # 显卡信息 列表
  model_info: dict = {}             # 模型状态

class ReqUpRealtimeModel(BaseModel):
  """更新模型实时数据"""
  server_ip: Optional[str] = None   # 可选
  model_list: list = []             # 模型列表

class ReqUpAlarmInfo(BaseModel):
  """更新告警信息"""
  fur_series: str       # 系列号
  fur_id: int           # 炉台号
  alarm_time: datetime  # 预警时间
  alarm_craft: int      # 工步
  alarm_func: str       # 功能
  alarm_result: str     # 预警结果
  server_ip: Optional[str] = None  # 可选

class ReqUpFurInfo(BaseModel):
  """更新炉台实时状态"""
  furnace_id: int        # 炉台id
  furnace_series: str    # 炉台系列
  furnace_state: int = 0 # 炉台状态
  server_ip: Optional[str] = None # 炉台服务器地址
  online: int = 1         # 0 离线 1 在线 
