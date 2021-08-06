from fastapi import APIRouter, Request, Body
from common.entity import ResponseBase, Error, valid_ip
from services.anls_service import *
from common.anls_req import ReqTempProcess, ReqSeedProcess, ReqShoulderProcess,ReqCylProcess


anls_router = APIRouter()

@anls_router.post('/update_temp_process', summary="更新一次稳温")
async def temp_process(item: ReqTempProcess, request: Request):
    res = ResponseBase()
    if item.server_ip == None or not valid_ip(item.server_ip):
        item.server_ip = request.client.host   
    if item.valid():
      up_temp_process(item, res)
    else:
      res.error(Error.PARAM_ERR)
    return res

@anls_router.post('/update_seed_process', summary="更新一次引晶")
async def seed_process(item: ReqSeedProcess, request: Request):
    res = ResponseBase()
    if item.server_ip == None or not valid_ip(item.server_ip):
        item.server_ip = request.client.host
    if item.valid():
      up_seed_process(item, res)
    else:
      res.error(Error.PARAM_ERR)
    return res

@anls_router.post('/update_shoulder_process', summary="更新一次放肩")
async def shoulder_process(item: ReqShoulderProcess, request: Request):
    res = ResponseBase()
    if item.server_ip == None or not valid_ip(item.server_ip):
        item.server_ip = request.client.host
    if item.valid():
      up_shoulder_process(item, res)
    else:
      res.error(Error.PARAM_ERR)
    return res

@anls_router.post('/update_cyl_process', summary="更新一次等径")
async def cyl_process(item: ReqCylProcess, request: Request):
    res = ResponseBase()
    if item.server_ip == None or not valid_ip(item.server_ip):
        item.server_ip = request.client.host
    up_cyl_process(item,res)
    return res

@anls_router.get('/get_temp_wt_dist',summary="获取当月稳温总工时")
async def get_temp_wt_dist(type: int = 1):
    res = ResponseBase()
    temp_wt_dist(type, res)
    return res

@anls_router.get('/get_temp_wt_group_dist',summary="获取当日稳温工时分组分布")
async def get_temp_wt_group_dist(type: int = 2):
    res = ResponseBase()
    temp_wt_group_dist(type, res)
    return res

@anls_router.get('/get_temp_std',summary="获取当月稳温炉台达标数")
async def get_temp_std(type: int = 1):
    res = ResponseBase()
    temp_std(type, res)
    return res

@anls_router.get('/get_temp_type_stic',summary="获取当日稳温炉台类型统计")
async def get_temp_type_stic(type: int = 2):
    res = ResponseBase()
    temp_type_stic(type, res)
    return res

@anls_router.get('/get_temp_history_stdr',summary="历史引晶达标率,最近一个月")
async def get_temp_history_stdr():
    res = ResponseBase()
    temp_history_stdr(res)
    return res

@anls_router.get('/get_temp_ot',summary="获取当日稳温工时超时比例")
async def get_temp_ot(type: int = 2):
    res = ResponseBase()
    temp_ot(type,res)
    return res

@anls_router.get('/get_seed_lates_dist',summary="获取当月末期平均拉速分布")
async def get_seed_lates_dist(type: int = 1):
    res = ResponseBase()
    seed_lates_dist(type,res)
    return res

@anls_router.get('/get_seed_wt_dist',summary="获取当日引晶工时分布")
async def get_seed_wt_dist(type: int = 2):
    res = ResponseBase()
    seed_wt_dist(type,res)
    return res

@anls_router.get('/get_seed_std',summary="获取当月达标率")
async def get_seed_std(type: int = 1):
    res = ResponseBase()
    seed_std(type,res)
    return res

@anls_router.get('/get_seed_type_stic',summary="获取当日引晶炉台类型统计")
async def get_seed_type_stic(type: int = 2):
    res = ResponseBase()
    seed_type_stic(type,res)
    return res

@anls_router.get('/get_seed_history_stdr',summary="获取历史引晶达标率")
async def get_seed_history_stdr():
    res = ResponseBase()
    seed_history_stdr(res)
    return res

@anls_router.get('/get_seed_ddvt_dist',summary="获取当日引晶直径极差")
async def get_seed_ddvt_dist(type: int = 2):
    res = ResponseBase()
    seed_ddvt_dist(type,res)
    return res

@anls_router.get('/get_shoulder_len_dist',summary="获取当月放肩长度分布")
async def get_shoulder_len_dist(type: int = 1):
    res = ResponseBase()
    shoulder_len_dist(type,res)
    return res

@anls_router.get('/get_shoulder_wt_dist',summary="获取当月放肩工时分布")
async def get_shoulder_wt_dist(type: int = 1):
    res = ResponseBase()
    shoulder_wt_dist(type,res)
    return res

@anls_router.get('/get_shoulder_std',summary="获取当月达标率")
async def get_shoulder_std(type: int = 1):
    res = ResponseBase()
    shoulder_std(type,res)
    return res

@anls_router.get('/get_shoulder_type_stic',summary="获取当日放肩炉台类型统计")
async def get_shoulder_type_stic(type: int = 2):
    res = ResponseBase()
    shoulder_type_stic(type,res)
    return res

@anls_router.get('/get_shoulder_history_stdr',summary="获取历史放肩达标率")
async def get_shoulder_history_stdr():
    res = ResponseBase()
    shoulder_history_stdr(res)
    return res

@anls_router.get('/get_shoulder_dvt_dist',summary="获取当日放肩直径/长度偏差分布")
async def get_shoulder_dvt_dist(dvt: str = '',type: int = 2):
    res = ResponseBase()
    if dvt in ['l','d']:
        shoulder_dvt_dist(dvt,type,res)
    else:
        res.error(Error.PARAM_ERR)
    return res

@anls_router.get('/get_shoulder_pd_dist',summary="放肩功率降幅")
async def get_shoulder_pd_dist(type: int = 2):
    res = ResponseBase()
    shoulder_pd_dist(type,res)
    return res

@anls_router.get('/get_craft_off_prop',summary="扩断引断比例")
async def get_craft_off_prop(type: int = 1,craft = ''):
    res = ResponseBase()
    if craft in ['seed','shoulder']:
        craft_off_prop(type,craft,res)
    else:
        res.error(Error.PARAM_ERR)
    return res

@anls_router.get('/get_single_shoulder_history_len',summary="获取某炉台的历史放肩长度曲线图")
async def get_single_shoulder_history_len(furnace_id: str = ''):
    res = ResponseBase()
    if furnace_id:
        single_shoulder_history_len(furnace_id,res)
    else:
        res.error(Error.PARAM_ERR)
    return res

@anls_router.get('/get_single_seed_history_lates',summary="获取某炉台的历史末期拉速曲线图")
async def get_single_seed_history_lates(furnace_id: str = ''):
    res = ResponseBase()
    if furnace_id:
        single_seed_history_lates(furnace_id,res)
    else:
        res.error(Error.PARAM_ERR)
    return res
 
