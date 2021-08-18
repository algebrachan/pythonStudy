import scrapy
from selenium import webdriver
from wangyPro.items import WangyproItem

class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    start_urls = ['https://news.163.com/']

    models_urls = [] 

    # 实例化一个浏览器对象
    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='F:\\wc\\test\\pytest\\pythonStudy\\web_crawier\\chromedriver.exe')

    def parse(self, response):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        alist = [2,3]
        for index in alist:
            model_url = li_list[index].xpath('./a/@href').extract_first()
            self.models_urls.append(model_url)
        # 依次对每个板块对应页面请求
        for url in self.models_urls: 
            print('url',url)
            yield scrapy.Request(url,callback=self.parse_model)

    def parse_model(self, response):
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div')
        print('div_list',div_list)
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            item = WangyproItem()
            item['title'] = title
            yield scrapy.Request(url=new_detail_url,callback=self.parse_detail,meta={'item':item})

    def parse_detail(self, response):
        content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        content = ''.join(content)
        item = response.meta['item']
        item['content'] = content

        yield item

    def closed(self, spider):
        self.bro.quit()

        


