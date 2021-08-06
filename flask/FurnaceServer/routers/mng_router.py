from main import app
from flask import request
from common.entity import ResponseBase, Error, valid_ip
from common.mvt_req import ReqModifyServer, ReqUpdateFurState
from services.mng_service import *

MNG_PRE_FIX = '/api/mng'

@app.route(f'{MNG_PRE_FIX}/modify_server', methods=["POST"])
async def modify_server():
    res = ResponseBase()
    item = ReqModifyServer(**request.get_json())
    if valid_ip(item.server_ip):
        mod_server(item, res)
    else:
        res.error(Error.PARAM_ERR)
    return res.__dict__


@app.route(f'{MNG_PRE_FIX}/server_lists', methods=["GET"])
async def server_lists():
    res = ResponseBase()
    ipt = request.args.get('ipt','')
    idx = request.args.get('idx',0)
    size = request.args.get('size',10)
    get_server_lists(res, ipt, idx, size)
    return res.__dict__

@app.route(f'{MNG_PRE_FIX}/furnace_lists', methods=["GET"])
async def furnace_lists():
    res = ResponseBase()
    id = request.args.get('id','')
    series = request.args.get('series','')
    status = request.args.get('status','')
    idx = request.args.get('idx',0)
    size = request.args.get('size',10)
    get_furnace_lists(res, id, series,status, idx, size)
    return res.__dict__

@app.route(f'{MNG_PRE_FIX}/modify_furnace', methods=["POST"])
async def modify_furnace():
    res = ResponseBase()
    item = ReqUpdateFurState(**request.get_json())
    # mod_furnace(item, res)
    #TODO
    return res.__dict__
