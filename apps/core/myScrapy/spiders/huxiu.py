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
        """
        1. 解析首页内容，获取文章url
        2. 判断 url 是否为合法的文章链接
        3. 判断 url 是否已处理
        :param response:
        :return:
        """
        all_urls = response.xpath(
            '//a[contains(@href, "article")]/@href').extract()
        for url in all_urls:
            url = "https://www.huxiu.com" + url
            self.logger.info('url: %s', url)
            if re.search(r'https://www.huxiu.com/article/.+\.html', url):
                if not self.r.sismember('urls', url):
                    # if not self.es.exists(INDEX_NAME, DOC_NAME, url):
                    self.r.sadd('urls', url)
                    yield Request(url, callback=self.parse_article, headers=self.headers, )

    def parse_article(self, response):
        item = huxiuItem()  # 实例item（具体定义的item类）,将要保存的值放到事先声明的item属性中

        item['url'] = response.url

        title_pattern = [
            'title',
            'h1[@class="t-h1"]'
        ]
        author_pattern = [
            'span[@class="author-name"]/a',
            'span[@class="author-info__username"]'
        ]

        share_pattern = [
            'span[@class="article-share pull-left"]',
            'span[@class="article-share"]'
        ]
        comment_pattern = [
            'span[@class="article-pl pull-left"]',
            'span[@class="article-pl"]'
        ]

        content_pattern = [
            'div[@class="article-content-wrap"]',
            'div[@class="article-content"]',
            'div[@class="article__content"]',
        ]

        timestamp_pattern = [
            'span[@class="article-time pull-left"]',
            'span[@class="article-time"]',
            'span[@class="article__time"]',
        ]

        for pattern in title_pattern:
            title = response.xpath(
                f'//{pattern}/text()').extract_first()
            if title:
                title = title.strip()
                if title.endswith('-虎嗅网'):
                    title = title[:-4].strip()
                item['title'] = title
                break

        for pattern in author_pattern:
            author_name = response.xpath(
                f'//{pattern}/text()').extract_first()
            if author_name:
                item['author'] = author_name.strip()
                break

        for pattern in share_pattern:
            share_xpath = response.xpath(
                f'//{pattern}/text()').extract_first()
            if share_xpath:
                item['share'] = share_xpath.strip()[2:]
                break

        for pattern in comment_pattern:
            comment_xpath = response.xpath(
                f'//{pattern}/text()').extract_first()
            if comment_xpath:
                item['comment'] = comment_xpath.strip()[2:]
                break

        for pattern in timestamp_pattern:
            timestamp_xpath = response.xpath(
                f'//{pattern}/text()').extract_first()
            if timestamp_xpath:
                item['timestamp'] = timestamp_xpath.strip()
                break

        item['description'] = response.xpath(
            '//meta[@name="description"]/@content').extract_first()

        item['keywords'] = response.xpath(
            '//meta[@name="keywords"]/@content').extract_first()


        for pattern in content_pattern:
            paragraphs = response.xpath(
                f'//{pattern}').xpath('p/text()').extract()
            if paragraphs:
                item['content'] = '\r\n'.join(paragraphs)
                break

        yield item  # 返回item,这时会自定解析item

        # urllib.urlretrieve(realUrl, path)  # 接收文件路径和需要保存的路径，会自动去文件路径下载并保存到我们指定的本地路径
