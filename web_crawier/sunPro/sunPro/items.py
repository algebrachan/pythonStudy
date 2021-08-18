# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SunproItem(scrapy.Item):
    id = scrapy.Field()
    state = scrapy.Field()
    title = scrapy.Field()
    time1 = scrapy.Field()
    time2 = scrapy.Field()
