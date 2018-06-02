# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class huxiuItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    share = scrapy.Field()
    comment = scrapy.Field()
    keywords = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    description = scrapy.Field()
