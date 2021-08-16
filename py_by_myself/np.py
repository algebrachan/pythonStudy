import asyncio
from datetime import datetime
import requests
# import aiohttp
import time

import aiohttp

start = datetime.now()
urls = [
  'http://127.0.0.1:5000/bobo',
  'http://127.0.0.1:5000/jay',
  'http://127.0.0.1:5000/tom',
]

async def get_page(url):
  async with aiohttp.ClientSession() as session:
    async with await session.get(url) as response:
      # text() 方法可以返回字符串形式的响应数据
      # read() 返回二进制
      # json() 返回json对象
      # 注意：获取响应数据操作之前一定要使用await进行手动挂起
      page_text = await response.text()
      print(page_text)

tasks =[]
for url in urls:
  c = get_page(url)
  task = asyncio.ensure_future(c)
  tasks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = datetime.now()

print(f'{(end-start).seconds}s') 


  