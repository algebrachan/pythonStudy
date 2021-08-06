class RespCurrentFurList:
    """获取当前系列的炉台
    """
    fur_list: list  # 当前系列炉台列表
    series: str  # 当前系列

    def __init__(self):
        self.fur_list = []
        self.series = ''

    def get_rname(self):
        return "current_fur_list_"


class RespOnlineFur:
    """获取在线炉台
    """

    def __init__(self):
        self.online_list = []

    def get_rname(self):
        return "online_list"


class RespHistoryBroken:
    """ 获取断苞历史数据
    """

    def __init__(self):
        self.broken_list = []

    def get_rname(self):
        return "history_broken_"


class RespSeriesBroken:
    """获取当日系列断苞统计
    """

    def __init__(self):
        self.series_brokens = []


class CurrentFurList:
    def __init__(self, name, state):
        self.name = name
        self.state = state


class RespMeltMaterialState:
    """化料固液面分割当前检测状态
    """
    total: int  # 当前化料炉台数
    conform: int  # 符合检测条件
    imconform: int  # 不符合条件

    def __init__(self):
        self.total = 0
        self.conform = 0
        self.imconform = 0


class RespModelState:
    """模型状态item
    """

    def __init__(self, name, idx, dict):
        self.key = idx
        self.name = name
        self.running_status = dict['running_status']
        self.used_memory = dict['used_memory']
        self.used_gpu = dict['used_gpu']
        self.gpu_id = dict['gpu_id']
        self.detect_speed = dict['detect_speed']
        self.cache_img_nums = dict['cache_img_nums']


class RespDetectionImg:
    """当前工艺过程图片
    """
    origin_img: str  # 原始图url
    detection_img: str  # 处理过后的图片url

    def __init__(self):
        self.origin_img = ''
        self.detection_img = ''


class RespServerState:
    """服务器状态
    """

    def __init__(self):
        self.gpu_info = []
        self.memory_info = {}
        self.disk_info = {}
        self.cpu_info = {}


class GpuInfo:
    def __init__(self, gpuinfo_dict):
        self.gpu_id = gpuinfo_dict['gpu_id']
        self.all_memory = gpuinfo_dict['all_memory']
        self.used_memory = gpuinfo_dict['used_memory']
        self.power = gpuinfo_dict['power']
        self.temperature = gpuinfo_dict['temperature']
        self.rate = round(
            gpuinfo_dict['used_memory']/gpuinfo_dict['all_memory'], 4)
        self.status = gpuinfo_dict['status']


class MemoryInfo:
    def __init__(self, memoryinfo_dict):
        self.used = memoryinfo_dict['used']
        self.total = memoryinfo_dict['total']
        self.rate = round(memoryinfo_dict['percent']/100, 4)
        self.status = memoryinfo_dict['status']


class DiskInfo:
    def __init__(self, diskinfo_dict):
        self.total = diskinfo_dict['total']
        self.used = diskinfo_dict['used']
        self.free = diskinfo_dict['free']
        self.rate = round(diskinfo_dict['percent']/100, 4)
        self.status = diskinfo_dict['status']


class CpuInfo:
    def __init__(self, cpuinfo_dict):
        self.rate = round(cpuinfo_dict['percent']/100, 4)
        self.status = cpuinfo_dict['status']

class RespServerList:

    def __init__(self,data):
        self.server_ip = data.server_ip
        self.state = data.state
        self.server_disk = data.server_disk
        self.cpu = data.server_cpu
        self.server_os = data.server_os
        self.server_name = data.server_name
        self.key = data.key

class RespFurnaceList:
    def __init__(self,data):
        self.furnace_id = data.furnace_id
        self.furnace_series = data.furnace_series
        self.furnace_state = data.furnace_state
        self.server_ip = data.server_ip
        self.gmt_modified = str(data.gmt_modified) if data.gmt_modified != None else ''
        self.key = data.key
