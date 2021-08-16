from selenium import webdriver
from lxml import etree

# 实例化一个浏览器对象(传入chrome浏览器驱动)
bro = webdriver.Chrome(executable_path='./chromedriver.exe')
# 让浏览器发起一个指定url对应请求
bro.get('https://www.baidu.com/')

# 获取源码
page_text = bro.page_source

tree = etree.HTML(page_text)
a = tree.xpath('//div[@id="s-top-left"]/a/@href')

print('a',a)