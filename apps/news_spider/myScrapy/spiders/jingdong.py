# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/8/5 22:15
@description:
"""

from scrapy import Spider, Request
from selenium import webdriver


class JingdongSpider(Spider):
    name = 'jingdong'

    def __init__(self):
        SERVICE_ARGS = ['--load-images=false', '--disk-cache=true', '--ignore-ssl-errors=true']
        self.browser = webdriver.PhantomJS(
            executable_path=r'C:\Users\23995\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe',
            service_args=SERVICE_ARGS
        )
        self.browser.set_page_load_timeout(30)

    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        start_urls = ['https://search.jd.com/Search?keyword=%E6%96%87%E8%83%B8&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&page={}&s=1&click=0'.format(str(i)) for i in
                      range(1, 10, 2)]
        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        print(len(selector))
        print('---------------------------------------------------')
