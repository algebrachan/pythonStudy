from pydantic import BaseModel
from typing import Optional

class ReqUpdateUser(BaseModel):
  """
  修改用户密码
  """
  username: str   # 操作的用户名 必传
  password: str = '' 
  token: str = ''
  operation: int = 0 # 操作 0新增 1修改 2删除
  user_type: int = 3 # 0:超级管理员，1:视觉后台管理员，2:数据分析管理员，3:普通用户
  server_ip: str = ''
  
class ReqLogin(BaseModel):
  """登录"""
  username: str
  password: str
  token: str = ''

class ReqUpdateServer(BaseModel):
  """修改服务器"""
  server_ip: str
  server_name: str = ''
  token: str = ''
  operation: int = 0 # 操作 0新增 1修改 2删除

