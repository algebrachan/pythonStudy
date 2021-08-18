import scrapy

# boss直聘存在反爬策略

class BossSpider(scrapy.Spider):
    name = 'boss'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=python&city=101210100&industry=&position=100109']

    def parse_detail(self, response):
        job_desc = response.xpath('//*[@id="main"]//div[@class="detail-content"]/div[1]/div[1]//text()').extract()
        job_desc = ''.join(job_desc)
        print(job_desc)
        pass

    def parse(self, response):
        print(response)
        li_list = response.xpath('//div[@id="header"]/div[1]/div[2]/ul/li/text()').extract()
        print(li_list)
        # print('li_list',li_list)
        # for li in li_list:
        #     job_name = li.xpath('.//span[@class="job-name"]/a/text()').extract_first()
        #     detail_url = li.xpath('.//span[@class="job-name"]/a/@href').extract_first()
        #     print(job_name)
        #     # 对详情页发请求
        #     yield scrapy.Request(detail_url,callback=self.parse_detail)
