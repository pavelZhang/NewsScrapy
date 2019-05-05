# coding=utf-8
import redis
import scrapy
import re
import os
import urllib
import sys
from scrapy.selector import Selector
from scrapy.http import HtmlResponse, Request

from myScrapy.elasticsearch_utils import ESUtils
from myScrapy.items import huxiuItem

INDEX_NAME = 'web'
DOC_NAME = 'huxiu'


class HuxiuSpdier(scrapy.spiders.Spider):
    name = "huxiu"  # 定义爬虫名，要和settings中的BOT_NAME属性对应的值一致
    allowed_domains = ["huxiu.com"]  # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    start_urls = ["https://www.huxiu.com/"]  # 开始爬取的地址
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Cookie': ''
    }

    esutils = ESUtils()
    es = esutils.connect()
    r = redis.Redis(host='10.45.10.201', port=6379)

    def start_requests(self):
        yield Request(url=self.start_urls[0], headers=self.headers, callback=self.parse)

    # 该函数名不能改变，因为Scrapy源码中默认callback函数的函数名就是parse
    def parse(self, response):
        all_urls = response.xpath(
            '//a[contains(@href, "article")]/@href').extract()
        for url in all_urls:
            url = "https://www.huxiu.com" + url
            self.logger.info('url: %s', url)
            if not self.r.sismember('urls', url):
            # if not self.es.exists(INDEX_NAME, DOC_NAME, url):
                self.r.sadd('urls', url)
                yield Request(url, callback=self.parse_article, headers=self.headers, )

    def parse_article(self, response):
        item = huxiuItem()  # 实例item（具体定义的item类）,将要保存的值放到事先声明的item属性中
        title = response.xpath(
            '//title/text()').extract_first()
        if not title:
            title = response.xpath(
                '//h1[@class="t-h1"]/text()').extract_first().strip()
        if title:
            if title.endswith('-虎嗅网'):
                title = title[:-4].strip()
            item['title'] = title
        item['author'] = response.xpath(
            '//span[@class="author-name"]/a/text()').extract_first().strip()

        share_xpath = response.xpath(
            '//span[@class="article-share pull-left"]/text()').extract_first()
        if not share_xpath:
            share_xpath = response.xpath(
                '//span[@class="article-share"]/text()').extract_first()
        item['share'] = share_xpath.strip()[2:]

        comment_xpath = response.xpath(
            '//span[@class="article-pl pull-left"]/text()').extract_first()
        if not comment_xpath:
            comment_xpath = response.xpath(
                '//span[@class="article-pl"]/text()').extract_first()
        item['comment'] = comment_xpath.strip()[2:]

        item['url'] = response.url
        timestamp_xpath = response.xpath(
            '//span[@class="article-time pull-left"]/text()').extract_first()
        if not timestamp_xpath:
            timestamp_xpath = response.xpath(
                '//span[@class="article-time"]/text()').extract_first()
        item['timestamp'] = timestamp_xpath.strip()
        item['description'] = response.xpath(
            '//meta[@name="description"]/@content').extract_first()
        item['keywords'] = response.xpath(
            '//meta[@name="keywords"]/@content').extract_first()

        paragraphs = response.xpath(
            '//div[@class="article-content-wrap"]').xpath('p/text()').extract()
        if paragraphs:
            item['content'] = '\r\n'.join(paragraphs)
        yield item  # 返回item,这时会自定解析item

        # urllib.urlretrieve(realUrl, path)  # 接收文件路径和需要保存的路径，会自动去文件路径下载并保存到我们指定的本地路径
