# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/8/4 22:28
@description:
    测试CrawlSpider用法
"""

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MySpider(CrawlSpider):
    name = 'cnblog'
    allowed_domains = []
    start_urls = ['https://www.cnblogs.com']

    rules = (
        Rule(LinkExtractor(allow=('https://www.cnblogs.com/\w+/p/\d+.html',)), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
