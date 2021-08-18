import scrapy
from firstBlood.items import ImgsItem

class ImgSpider(scrapy.Spider):
    name = 'img'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://sc.chinaz.com/tupian/']

    def parse(self, response):
        div_list = response.xpath('//div[@id="container"]/div')
        for div in div_list:
            src = div.xpath('./div/a/img/@src2').extract_first()
            item = ImgsItem()
            item['src'] = f'https://{src}'
            yield item  # 将item提交给管道
