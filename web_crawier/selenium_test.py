from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions

# 实现可视化界面
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])

# 实例化一个浏览器对象(传入chrome浏览器驱动)
bro = webdriver.Chrome(executable_path='./chromedriver.exe',chrome_options=chrome_options,options=option)
# 无可视化界面
bro.get('https://www.baidu.com/')
sleep(2)
bro.save_screenshot('baidu.png')

sleep(5)
bro.quit()