# 学习Django项目入门

## 项目说明
- "学习笔记"的web应用程序 《Python编程从入门到实践》
- 建立虚拟环境,将该项目的库和别的项目分离
```shell
 # 建立虚拟环境
 pip install virtualnev
 virtualenv new_env
 # 激活虚拟环境
 env\Scripts\activate
 # 停止虚拟环境
 deactivate
 # 使用virtualenvwrapper
 pip install virtualenvwrapper-win
 # 配置环境变量
 
 # 安装Django
 pip install Django
```
- 新建项目
```shell
django-admin startproject learning_log .
# 创建应用程序
python manage.py startapp learning_logs
# 生成迁移文件 进行迁移
python manage.py makemigrations learning_logs
python manage.py migrate
```
- 目录说明

  |    文件     |        说明        |
  | :---------: | :----------------: |
  |   asgi.py   |                    |
  | settings.py | 系统交互和项目管理 |
  |   urls.py   | 网页响应浏览器请求 |
  |   wsgi.py   |  web服务网关接口   |

  

