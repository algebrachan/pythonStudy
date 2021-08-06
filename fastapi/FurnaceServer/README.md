# fastapi

## 1.预处理

- [安装虚拟环境](https://gitee.com/mathchan/zvision-work/blob/master/2020-11/python.md)
- install 模块使用类似于js中 package.json这种类型的配置文件

```shell
# 启动虚拟环境
# 在安装包的时候 使用如下 形式安装
pip install fastapi[all] 
pip freeze > requirements.txt
# 当 clone一个项目的时候 只需安装 配置文件中的包
pip install -r requirements.txt
```

- 运行

```shell
uvicorn main:app --reload
uvicorn main:app --host '0.0.0.0' --port 8065 --reload --workers 2
# 退出
ctrl+C
```

- 创建数据库 mysql

```shell

```

- 测试
  - 测试案例

 ```python
 from fastapi.testclient import TestClient
 from main import app
 
 client = TestClient(app)
 def test_base():
 response = client.get("/base")
 assert response.status_code == 200
 ```

- 运行测试代码

 ```shell
 pip install pytest
 pytest
 ```

- 打印日志

  logging引入

- 清除缓存

  ```shell
  py delcache.py
  ```

## 2.目录结构

```txt
│  config.py
│  main.py			# 主程序入口
│  README.md		# 项目说明文档
│  requirements.txt	# 依赖文件
│  test_main.py		# 测试文件入口     
|  delcache.py		# 缓存清理         
├─common			
│  │  entity.py		# RESTful接口统一回复类
│  
├─models			# 持久层，设置数据库中的类
│  │  models.py		
│          
├─routers			# controler层，路由
│  │  base_router.py
│          
├─services			# service层 处理业务逻辑，数据库的crud
│  │  base_service.py
│          
├─utils				# 公用工具层，用来封装公用的函数或公用模块
│      
```

## 3. 部署

```shell
 scp -r fastapi wangchen@10.50.63.63:/home/wangchen
```
