import logging  # 日志模块
from logging.handlers import TimedRotatingFileHandler
import datetime   # 时间模块



# 获取今天的日期
today_date = str(datetime.date.today())
# # 创建logger记录器
# # 创建logger记录器
# logging.basicConfig(filename=path+'server.log', level=logging.INFO, filemode='a',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger('test') # 用来分类
# logger.setLevel(logging.ERROR)

# # 创建一个控制台处理器，并将日志级别设置为debug

# ch = logging.StreamHandler()

# ch.setLevel(logging.ERROR)

# # 创建formatter格式化器
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# # 将formatter 添加到ch处理器
# ch.setFormatter(formatter)

# # 将ch添加到logger
# logger.addHandler(ch)


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='error', when='midnight', interval=4, backCount=5, fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
        self.logger = logging.getLogger()
        formaat_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()
        sh.setFormatter(formaat_str)
        th = TimedRotatingFileHandler(
            filename=filename, interval=interval, when=when, backupCount=backCount, encoding='utf-8')
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(formaat_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
