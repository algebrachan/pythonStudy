# 学习Django项目入门

## 项目说明
- "学习笔记"的web应用程序
- 建立虚拟环境,将该项目的库和别的项目分离
```shell
 # 建立虚拟环境
 python -m venv ll_env
 # 激活虚拟环境
 ll_env\Scripts\activate
 # 停止虚拟环境
 deactivate
 # 安装Django
 pip install Django
```
- 新建项目
```shell
django-admin startproject learning_log .
```
- 目录说明

  |    文件     |        说明        |
  | :---------: | :----------------: |
  |   asgi.py   |                    |
  | settings.py | 系统交互和项目管理 |
  |   urls.py   | 网页响应浏览器请求 |
  |   wsgi.py   |  web服务网关接口   |

  
