from main import app
from flask import request
from common.entity import ResponseBase, Error, valid_ip
from services.anls_service import *
from common.anls_req import ReqTempProcess, ReqSeedProcess, ReqShoulderProcess,ReqCylProcess

ANLS_PRE_FIX = '/api/anls'

@app.route(f'{ANLS_PRE_FIX}/update_temp_process', methods=["POST"])
async def temp_process():
    res = ResponseBase()
    item = ReqTempProcess(**request.get_json())
    if item.server_ip == None or not valid_ip(item.server_ip):
        item.server_ip = request.remote_addr
    if item.valid():
      up_temp_process(item, res)
    else:
      res.error(Error.PARAM_ERR)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/update_seed_process', methods=["POST"])
async def seed_process():
    res = ResponseBase()
    item = ReqSeedProcess(**request.get_json())
    if item.server_ip == None or not valid_ip(item.server_ip):
        item.server_ip = request.remote_addr
    if item.valid():
      up_seed_process(item, res)
    else:
      res.error(Error.PARAM_ERR)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/update_shoulder_process', methods=["POST"])
async def shoulder_process():
    res = ResponseBase()
    item = ReqShoulderProcess(**request.get_json())
    if item.server_ip == None or not valid_ip(item.server_ip):
        item.server_ip = request.remote_addr
    if item.valid():
      up_shoulder_process(item, res)
    else:
      res.error(Error.PARAM_ERR)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/update_cyl_process', methods=["POST"])
async def cyl_process():
    res = ResponseBase()
    item = ReqCylProcess(**request.get_json())
    if item.server_ip == None or not valid_ip(item.server_ip):
        item.server_ip = request.remote_addr
    up_cyl_process(item,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_temp_wt_dist',methods=["GET"])
async def get_temp_wt_dist():
    res = ResponseBase()
    type = request.args.get('type',1)
    temp_wt_dist(type, res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_temp_wt_group_dist',methods=["GET"])
async def get_temp_wt_group_dist():
    res = ResponseBase()
    type = request.args.get('type',2)
    temp_wt_group_dist(type, res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_temp_std',methods=["GET"])
async def get_temp_std():
    res = ResponseBase()
    type = request.args.get('type',1)
    temp_std(type, res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_temp_type_stic',methods=["GET"])
async def get_temp_type_stic():
    res = ResponseBase()
    type = request.args.get('type',2)
    temp_type_stic(type, res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_temp_history_stdr',methods=["GET"])
async def get_temp_history_stdr():
    res = ResponseBase()
    temp_history_stdr(res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_temp_ot',methods=["GET"])
async def get_temp_ot():
    res = ResponseBase()
    type = request.args.get('type',2)
    temp_ot(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_seed_lates_dist',methods=["GET"])
async def get_seed_lates_dist():
    res = ResponseBase()
    type = request.args.get('type',1)
    seed_lates_dist(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_seed_wt_dist',methods=["GET"])
async def get_seed_wt_dist():
    res = ResponseBase()
    type = request.args.get('type',2)
    seed_wt_dist(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_seed_std',methods=["GET"])
async def get_seed_std():
    res = ResponseBase()
    type = request.args.get('type',1)
    seed_std(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_seed_type_stic',methods=["GET"])
async def get_seed_type_stic():
    res = ResponseBase()
    type = request.args.get('type',2)
    seed_type_stic(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_seed_history_stdr',methods=["GET"])
async def get_seed_history_stdr():
    res = ResponseBase()
    seed_history_stdr(res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_seed_ddvt_dist',methods=["GET"])
async def get_seed_ddvt_dist():
    res = ResponseBase()
    type = request.args.get('type',2)
    seed_ddvt_dist(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_shoulder_len_dist',methods=["GET"])
async def get_shoulder_len_dist():
    res = ResponseBase()
    type = request.args.get('type',1)
    shoulder_len_dist(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_shoulder_wt_dist',methods=["GET"])
async def get_shoulder_wt_dist():
    res = ResponseBase()
    type = request.args.get('type',1)
    shoulder_wt_dist(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_shoulder_std',methods=["GET"])
async def get_shoulder_std():
    res = ResponseBase()
    type = request.args.get('type',1)
    shoulder_std(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_shoulder_type_stic',methods=["GET"])
async def get_shoulder_type_stic():
    res = ResponseBase()
    type = request.args.get('type',2)
    shoulder_type_stic(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_shoulder_history_stdr',methods=["GET"])
async def get_shoulder_history_stdr():
    res = ResponseBase()
    shoulder_history_stdr(res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_shoulder_dvt_dist',methods=["GET"])
async def get_shoulder_dvt_dist():
    res = ResponseBase()
    dvt = request.args.get('dvt','')
    type = request.args.get('type',2)
    if dvt in ['l','d']:
        shoulder_dvt_dist(dvt,type,res)
    else:
        res.error(Error.PARAM_ERR)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_shoulder_pd_dist',methods=["GET"])
async def get_shoulder_pd_dist():
    res = ResponseBase()
    type = request.args.get('type',2)
    shoulder_pd_dist(type,res)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_craft_off_prop',methods=["GET"])
async def get_craft_off_prop():
    res = ResponseBase()
    type = request.args.get('type',1)
    craft = request.args.get('craft','')
    if craft in ['seed','shoulder']:
        craft_off_prop(type,craft,res)
    else:
        res.error(Error.PARAM_ERR)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_single_shoulder_history_len',methods=["GET"])
async def get_single_shoulder_history_len():
    res = ResponseBase()
    furnace_id = request.args.get('furnace_id','')
    if furnace_id:
        single_shoulder_history_len(furnace_id,res)
    else:
        res.error(Error.PARAM_ERR)
    return res.__dict__

@app.route(f'{ANLS_PRE_FIX}/get_single_seed_history_lates',methods=["GET"])
async def get_single_seed_history_lates(furnace_id: str = ''):
    res = ResponseBase()
    furnace_id = request.args.get('furnace_id','')
    if furnace_id:
        single_seed_history_lates(furnace_id,res)
    else:
        res.error(Error.PARAM_ERR)
    return res.__dict__