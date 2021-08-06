from datetime import datetime
from enum import Flag
from sqlalchemy.sql.expression import false, update
from pydantic import BaseModel
from typing import Optional

class ReqTempProcess(BaseModel):
  """ 一次稳温工艺
  """
  furnace_id: str       # 炉台id 必传
  weld_wt: float = 0    # 稳温工时 h
  weld_type: int = 0    # 稳温类型 
  weld_std: bool = 0 # 稳温达标
  update_time: datetime # 工艺更新时间 
  server_ip: Optional[str] = None  # 可选

  def valid(self):
    if self.weld_type not in range(1,8):
      return False
    return True

class ReqSeedProcess(BaseModel):
  """ 一次引晶工艺
  """
  furnace_id: str       # 炉台id 必传
  seed_wt: float = 0    # 引晶工时 h
  seed_lates: float = 0 # 末期拉速
  seed_type: int = 0    # 引晶类型
  seed_std: int = 0     # 引晶达标 
  seed_off: bool = 0    # 是否引断
  seed_diam: float = 0  # 引晶直径
  seed_ddvt: float = 0  # 直径极差
  update_time: datetime # 工艺更新时间 
  server_ip: Optional[str] = None  # 可选

  def valid(self):
    if self.seed_type not in range(1,6):
      return False
    return True

class ReqShoulderProcess(BaseModel):
  """ 一次放肩工艺
  """
  furnace_id: str           # 炉台id 必传
  shoulder_wt: float = 0    # 放肩工时
  shoulder_len: float = 0   # 放肩长度
  shoulder_ddvt: float = 0  # 放肩直径偏差
  shoulder_ldvt: float = 0  # 放肩长度偏差
  shoulder_powerdec: float = 0  # 放肩功率降幅
  shoulder_off: bool = 0    # 是否扩断
  shoulder_std: bool = 0    # 放肩达标
  shoulder_type: int = 0    # 放肩类型
  update_time: datetime     # 工艺更新时间 
  server_ip: Optional[str] = None  # 可选

  def valid(self):
    if self.shoulder_type not in range(1,5):
      return False
    return True

class ReqCylProcess(BaseModel):
  """ 一次等径工艺
  """
  furnace_id: str           # 炉台id 必传
  cyl_nums: int = 0
  cyl_header_lates: float = 0
  cyl_len: float = 0
  cyl_off: bool =0
  update_time: datetime     # 工艺更新时间 
  server_ip: Optional[str] = None  # 可选