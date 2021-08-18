import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sunPro.items import SunproItem

class SunSpider(CrawlSpider):
    name = 'sun'
    start_urls = ['https://wz.sun0769.com/political/index/politicsNewest']

    # 连接提取器
    link = LinkExtractor(allow=r'id=1&page=\d+')

    rules = (
        # 规则解析器
        # follow=True: 可以将链接提取器继续作用到连接提取到的url中，实现全栈爬取
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_list= response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in li_list:
            id = li.xpath('./span[1]/text()').extract_first()
            state = li.xpath('./span[2]/text()').extract_first()
            title = li.xpath('./span[3]/a/text()').extract_first()
            time1 = li.xpath('./span[4]/text()').extract_first()
            time2 = li.xpath('./span[5]/text()').extract_first()
            item = SunproItem()
            item['id'] = id.strip()
            item['state'] = state.strip()
            item['title'] = title.strip()
            item['time1'] = time1.strip()
            item['time2'] = time2.strip()
            yield item

