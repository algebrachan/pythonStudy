import scrapy


class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    start_urls = ['http://www.521609.com/meinvxiaohua/']

    page_num = 2

    def parse(self, response):
        li_list = response.xpath('//div[@id="content"]/div[2]/div[2]/ul/li')
        for li in li_list:
            img_name = li.xpath('./a[2]/b/text() | ./a[2]/text()').extract_first()
            print(img_name)
        
        if self.page_num <= 11:
            new_url = f'http://www.521609.com/meinvxiaohua/list12{self.page_num}.html'
            print('new_url',new_url)
            self.page_num += 1
            # 手动请求,callback专门用于回调解析函数
            yield scrapy.Request(url=new_url,callback=self.parse)
    
