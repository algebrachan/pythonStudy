from fastapi import APIRouter, Request, Body
from common.entity import ResponseBase, Error, valid_ip
from common.mvt_req import ReqModifyServer, ReqUpdateFurState
from services.mng_service import *

mng_router = APIRouter()


@mng_router.post('/modify_server', summary="修改服务器")
async def modify_server(item: ReqModifyServer):
    res = ResponseBase()
    if valid_ip(item.server_ip):
        mod_server(item, res)
    else:
        res.error(Error.PARAM_ERR)
    return res


@mng_router.get('/server_lists', summary="获取服务器详细列表")
async def server_lists(ipt: str = '', idx: int = 0, size: int = 10):
    res = ResponseBase()
    get_server_lists(res, ipt, idx, size)
    return res

@mng_router.get('/furnace_lists', summary="获取炉台详细列表")
async def furnace_lists(id: str = '',series: str='', status:str='',idx: int = 0, size: int = 10):
    res = ResponseBase()
    get_furnace_lists(res, id, series,status, idx, size)
    return res

@mng_router.post('/modify_furnace', summary="修改炉台")
async def modify_furnace(item: ReqUpdateFurState):
    res = ResponseBase()
    # mod_furnace(item, res)
    #TODO
    return res
