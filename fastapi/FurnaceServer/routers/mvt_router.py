from fastapi import APIRouter, Request
from datetime import datetime
from common.entity import ResponseBase, Error, valid_ip
from services.mvt_service import *

mvt_router = APIRouter()

@mvt_router.post('/update_realtime_server',summary="更新服务器实时数据")
async def update_realtime_server(item:ReqUpRealtimeServer,request:Request):
  if item.server_ip == None or not valid_ip(item.server_ip):
    item.server_ip = request.client.host
  return up_realtime_server(item,res = ResponseBase())

@mvt_router.post('/update_realtime_model',summary="更新模型实时数据")
async def update_realtime_model(item:ReqUpRealtimeModel,request:Request):
  if item.server_ip == None or not valid_ip(item.server_ip):
    item.server_ip = request.client.host
  return up_realtime_model(item,res = ResponseBase())


@mvt_router.post('/update_alarm_info',summary="更新告警信息")
async def update_alarm_info(item:ReqUpAlarmInfo,request:Request):
  if item.server_ip == None or not valid_ip(item.server_ip):
    item.server_ip = request.client.host
  return up_alarm_info(item,res = ResponseBase())

@mvt_router.post('/update_furnace_info',summary="更新炉台实时状态")
async def update_furnace_info(item:ReqUpFurInfo,request:Request):
  if item.server_ip == None or not valid_ip(item.server_ip):
    item.server_ip = request.client.host
  return up_furnace_info(item,res = ResponseBase())

@mvt_router.get('/get_alarm_info_list',summary="查看预警列表")
async def get_alarm_info_list(fur_series:str = '',fur_id: str = '',alarm_func:str = ''):
  return alarm_info_list(fur_series,fur_id,alarm_func,res = ResponseBase())

@mvt_router.get('/get_alarm_info_simplify',summary="查看预警列表简化")
async def get_alarm_info_simplify(count:int = 1):
  return alarm_info_simplify(count,res = ResponseBase())

@mvt_router.get('/get_server_list',summary="查看服务器列表详情")
async def get_server_list(count:int = 8):
  return server_list(count,res = ResponseBase())
  
@mvt_router.get('/get_server_state',summary="获取服务器状态")
async def get_server_state(server_ip:str = ''):
  res = ResponseBase()
  if not valid_ip(server_ip):
    res.error(Error.PARAM_ERR)
    return res
  return server_state(server_ip,res)

@mvt_router.get('/get_model_state',summary="获取模型状态")
async def get_model_state(server_ip:str = ''):
  res = ResponseBase()
  if not valid_ip(server_ip):
    res.error(Error.PARAM_ERR)
    return res
  return model_state(server_ip,res)

@mvt_router.get('/get_history_broken',summary="获取断苞历史数据")
async def get_history_broken(days:int = 30,server_ip:str = ''):
  return history_broken(days,server_ip,res = ResponseBase())

@mvt_router.get('/get_broken_info',summary="获取断苞详情数据")
async def get_broken_info(date:str,craft:str=''):
  date = datetime.strptime(date,'%Y-%m-%d')
  return broken_info(date,craft,res = ResponseBase())

@mvt_router.get('/get_online_fur', summary="获取当前工艺在线炉台数")
async def get_online_fur(server_ip:str = ''):
  res = ResponseBase()
  if not valid_ip(server_ip):
    res.error(Error.PARAM_ERR)
    return res
  return online_fur(server_ip,res = ResponseBase())

@mvt_router.get('/get_series_list', summary="当前系列")
async def get_series_list(server_ip:str = ''):
  return series_list(server_ip,res = ResponseBase())

@mvt_router.get('/get_current_fur_list', summary="获取当前系列的炉台列表")
async def get_current_fur_list(series: str = '',server_ip: str = ''):
  return current_fur_list(series,server_ip, res= ResponseBase())

@mvt_router.get('/get_fur_result', summary="获取检测结果")
async def get_fur_result(fur_series: str = '',fur_id: str = '',device_state: str = '',model_name:str = ''):
  res = ResponseBase()
  if fur_id and fur_series:
    fur_result(fur_series, fur_id, device_state, model_name, res)
    pass
  else:
    res.error(Error.PARAM_ERR)
  return res