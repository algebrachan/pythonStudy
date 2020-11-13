"""定义 learning_logs的URL模式
    """
from django.conf.urls import url
from views import index
import sys
sys.path.append("..")


urlpatterns = [
    # 主页
    url(r'^$', index, name='index'),
]
