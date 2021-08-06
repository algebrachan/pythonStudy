from main import app
from flask import request
from common.entity import ResponseBase, Error, valid_ip
from common.mvt_req import ReqUpdateFurState, ReqUpdateHistoryBroken, ReqUpdateSeriesBroken
from services.mvt_service import *

MVT_PRE_FIX = '/api/mvt'

@app.route(f'{MVT_PRE_FIX}/update_fur_state', methods=["POST"])
async def update_fur_state():
    res = ResponseBase()
    item = ReqUpdateFurState(**request.get_json())
    if item.furnace_host != None and valid_ip(item.furnace_host):
        client_host = item.furnace_host
    else:
        client_host = request.remote_addr
    fur_state(item, res, client_host)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/update_history_broken', methods=["POST"])
async def update_history_broken():
    res = ResponseBase()
    item = ReqUpdateHistoryBroken(**request.get_json())
    if item.server_ip != None and valid_ip(item.server_ip):
        client_host = item.server_ip
    else:
        client_host = request.remote_addr
    up_history_broken(item, res, client_host)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/update_series_broken', methods=["POST"])
async def update_series_broken():
    res = ResponseBase()
    item = ReqUpdateSeriesBroken(**request.get_json())
    up_series_broken(item, res)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/get_series_list', methods=["GET"])
async def get_series_list():
    res = ResponseBase()
    series_list(res)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/get_fur_result', methods=["GET"])
async def get_fur_result():
    res = ResponseBase()
    furnace_id = request.args.get('furnace_id','')
    img_idx = request.args.get('img_idx','')
    furnace_state = request.args.get('furnace_state','')
    model_name = request.args.get('model_name','')
    if furnace_id:
        fur_result(furnace_id, img_idx, furnace_state, model_name, res)
    else:
        res.error(Error.PARAM_ERR)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/get_current_fur_list', methods=["GET"])
async def get_current_fur_list():
    res = ResponseBase()
    series = request.args.get('series','A')
    current_fur_list(series, res)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/get_server_list', methods=["GET"])
async def get_server_list():
    res = ResponseBase()
    server_list(res)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/get_server_state', methods=["GET"])
async def get_server_state():
    res = ResponseBase()
    server_ip = request.args.get('server_ip','')
    if valid_ip(server_ip):
        server_state(server_ip, res)
    else:
        res.error(Error.PARAM_ERR)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/get_model_state', methods=["GET"])
async def get_model_state():
    res = ResponseBase()
    server_ip = request.args.get('server_ip','')
    if valid_ip(server_ip):
        model_state(server_ip, res)
    else:
        res.error(Error.PARAM_ERR)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/get_online_fur', methods=["GET"])
async def get_online_fur():
    res = ResponseBase()
    online_fur(res)
    return res.__dict__


@app.route(f'{MVT_PRE_FIX}/get_history_broken', methods=["GET"])
async def get_history_broken():
    res = ResponseBase()
    type = request.args.get('type',1)
    history_broken(type, res)
    return res.__dict__

