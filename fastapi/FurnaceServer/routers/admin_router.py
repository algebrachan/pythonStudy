from fastapi import APIRouter, Request
from common.entity import ResponseBase, Error, valid_ip
from fastapi.routing import serialize_response
from services.admin_service import *
from config import redis_session

admin_router = APIRouter()

@admin_router.get('/add_super_admin',summary="开发人员预留新增超级管理员账号接口")
async def add_super_admin(username:str = 'admin',password:str = '123456'):
  return super_admin(username,password,res = ResponseBase())

@admin_router.post('/login',summary="登录")
async def user_login(item:ReqLogin):
  res = ResponseBase()
  admin = token2user(item.token)
  if admin != None: return res
  return login(item,res)

@admin_router.post('/update_user',summary="修改用户密码")
async def update_user(item:ReqUpdateUser):
  res = ResponseBase()
  # 校验 token
  admin = token2user(item.token)
  if admin != None:
    up_user(admin,item,res)
    pass
  else:
    res.error(Error.TOKEN_OT)
    pass
  return res

@admin_router.get('/get_user_list',summary="查看用户列表")
async def get_user_list(value:str = ''):
  return user_list(value,res = ResponseBase())
  
@admin_router.post('/update_server',summary="更新服务器")
async def update_server(item:ReqUpdateServer):
  res = ResponseBase()
  admin = token2user(item.token)
  if admin == None:
    res.error(Error.TOKEN_OT)
    return res
  if not valid_ip(item.server_ip):
    res.error(Error.PARAM_ERR,err_msg='服务器ip地址错误')
    return res
  return up_server(admin,item,res)
  
@admin_router.get('/get_server_list',summary="查看服务器列表")
async def get_server_list(value:str = ''):
  return server_list(value,res = ResponseBase())

@admin_router.get('/get_furnace_lists',summary="获取炉台详情列表")
async def get_furnace_lists(id: str='',series: str='',status:str='',idx:int=0,size:int=10):
  return furnace_lists(id,series,status,idx,size,res=ResponseBase())


def token2user(token:str):
  if token == '':return None
  return redis_session.get(token)
  

