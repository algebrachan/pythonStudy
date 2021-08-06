import requests

requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
requests.adapters.DEFAULT_POOL_TIMEOUT = 10  # 超时时间
requests.adapters.DEFAULT_POOLSIZE = 50  # 修改默认连接池个数
s_reqs = requests.session()
s_reqs.keep_alive = False  # 链接不保活

# dict 转对象
class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

def dict2obj(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    d = Dict()
    for k, v in dictObj.items():
        d[k] = dict2obj(v)
    return d

def str2int(num):
    try:
        return int(num)
    except:
        return 0
    