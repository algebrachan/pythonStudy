# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SunproPipeline:
    fp = None
    # 重写父类方法 该方法只有在开始爬虫的时候调用一次
    def open_spider(self,spider):
        print('开始爬虫')
        self.fp = open('./sun.txt','w',encoding='utf-8')

    # 该方法每接到一次item就会被调用一次
    def process_item(self, item, spider):
        id = item['id']
        state = item['state']
        title = item['title']
        time1 = item['time1']
        time2 = item['time2']
        self.fp.write(id+','+state+','+title+','+time1+','+time2+'\n')
        return item  # 就会执行给下一个管道

    def close_spider(self,spider):
        print('结束爬虫')
        self.fp.close()
