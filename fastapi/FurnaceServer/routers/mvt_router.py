from fastapi import APIRouter, Request, Body
from common.entity import ResponseBase, Error, valid_ip
from common.mvt_req import ReqUpdateFurState, ReqUpdateHistoryBroken, ReqUpdateSeriesBroken
from services.mvt_service import *

mvt_router = APIRouter()


@mvt_router.post('/update_fur_state', summary="更新炉台状态")
async def update_fur_state(item: ReqUpdateFurState, request: Request):
    res = ResponseBase()
    if item.furnace_host != None and valid_ip(item.furnace_host):
        client_host = item.furnace_host
    else:
        client_host = request.client.host
    fur_state(item, res, client_host)
    return res


@mvt_router.post('/update_history_broken', summary="更新断苞历史数据")
async def update_history_broken(item: ReqUpdateHistoryBroken, request: Request):
    res = ResponseBase()
    if item.server_ip != None and valid_ip(item.server_ip):
        client_host = item.server_ip
    else:
        client_host = request.client.host
    up_history_broken(item, res, client_host)
    return res


@mvt_router.post('/update_series_broken', summary="更新当日系列断苞统计")
async def update_series_broken(item: ReqUpdateSeriesBroken):
    res = ResponseBase()
    up_series_broken(item, res)
    return res


@mvt_router.get('/get_series_list', summary="当前系列")
async def get_series_list():
    res = ResponseBase()
    series_list(res)
    return res


@mvt_router.get('/get_fur_result', summary="获取检测结果")
async def get_fur_result(furnace_id: str = '', img_idx: str = '', furnace_state: str = '',model_name: str = ''):
    res = ResponseBase()
    if furnace_id:
        fur_result(furnace_id, img_idx, furnace_state, model_name, res)
    else:
        res.error(Error.PARAM_ERR)
    return res


@mvt_router.get('/get_current_fur_list', summary="获取当前系列的炉台列表")
async def get_current_fur_list(series: str = 'A'):
    res = ResponseBase()
    current_fur_list(series, res)
    return res


@mvt_router.get('/get_server_list', summary="获取服务器列表")
async def get_server_list():
    res = ResponseBase()
    server_list(res)
    return res


@mvt_router.get('/get_server_state', summary="获取服务器状态")
async def get_server_state(server_ip: str = ''):
    res = ResponseBase()
    if valid_ip(server_ip):
        server_state(server_ip, res)
    else:
        res.error(Error.PARAM_ERR)
    return res


@mvt_router.get('/get_model_state', summary="获取模型状态")
async def get_model_state(server_ip: str = ''):
    res = ResponseBase()
    if valid_ip(server_ip):
        model_state(server_ip, res)
    else:
        res.error(Error.PARAM_ERR)
    return res


@mvt_router.get('/get_online_fur', summary="获取当前工艺在线炉台数")
async def get_online_fur():
    res = ResponseBase()
    online_fur(res)
    return res


@mvt_router.get('/get_history_broken', summary="获取断苞历史数据")
async def get_history_broken(type: int):
    res = ResponseBase()
    history_broken(type, res)
    return res


# @mvt_router.get('/get_series_broken', summary="获取系列断苞统计")
# async def get_series_broken(type: int):
#     res = ResponseBase()
#     series_broken(type, res)
#     return res

# @mvt_router.get('/test',summary="测试专用")
# async def my_test_router():
#     res = ResponseBase()
#     my_test(res)
#     return res
