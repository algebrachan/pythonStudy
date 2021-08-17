import scrapy
from firstBlood.items import FirstbloodItem

class FirstSpider(scrapy.Spider):
    # 爬虫文件的名称：就是爬虫源文件的一个唯一标识
    name = 'first'
    # 允许的域名：用来限定start_urls列表中哪些url可以进行请求发送
    # allowed_domains = ['www.baidu.com']

    # 起始的url列表：被scrapy自动发送请求
    start_urls = ['https://www.qiushibaike.com/text/']

    # 用于解析数据
    def parse(self, response):
      # 解析：作者的名称+段子内容
      # print(response)
      div_list = response.xpath('//div[starts-with(@id,"qiushi_tag")]')
      for div in div_list:
        # xpath返回的是列表，但是列表元素一定是Selector类型的对象
        # extract可以将Selector对象中data参数存储的字符串提取出来
        author = div.xpath('./div[1]/a[2]/h2/text()')[0].extract()
        content = div.xpath('./a[1]/div[@class="content"]//text()').extract()
        content = ''.join(content)

        item = FirstbloodItem()
        item['author'] = author
        item['content'] = content.strip()
        yield item # 将item提交给管道

      
      



      