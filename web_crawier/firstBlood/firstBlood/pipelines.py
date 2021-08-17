# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class FirstbloodPipeline:
    fp = None
    # 重写父类方法 该方法只有在开始爬虫的时候调用一次
    def open_spider(self,spider):
        print('开始爬虫')
        self.fp = open('./first.txt','w',encoding='utf-8')

    # 该方法每接到一次item就会被调用一次
    def process_item(self, item, spider):
        author = item['author']
        content = item['content']
        self.fp.write(author+':'+content+'\n')
        return item  # 就会执行给下一个管道

    def close_spider(self,spider):
        print('结束爬虫')
        self.fp.close()

# 管道文件中一个管道类对应将一组数据存储到一个平台或载体中
class mysqlPipeLine:
    conn = None
    cursor = None
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='123456',db='scrapydb',charset='utf8')

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        try:
            sql = f'insert into qiubai (author,content) values("{item["author"]}","{item["content"]}")'
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item 

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()


