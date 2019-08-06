# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/8/4 22:28
@description:
    爬去虎嗅文章
"""
import redis
import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import HtmlResponse, Request

from myScrapy.items import huxiuItem

INDEX_NAME = 'web'
DOC_NAME = 'huxiu'

import requests


def get_urls():
    res = requests.get('https://www-api.huxiu.com/v1/article/list?page=1&pagesize=21')

    if res.status_code == 200:
        ret = res.json()
        dataList = ret['data']['dataList']
        urls = (f"https://www.huxiu.com/article/{item['aid']}.html" for item in dataList)
        return urls


class HuxiuSpdier(scrapy.spiders.Spider):
    name = "huxiu2"
    allowed_domains = ["huxiu.com"]
    start_urls = get_urls()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Cookie': ''
    }

    r = redis.Redis(host='10.45.10.201', port=6379)

    def start_requests(self):
        for url in self.start_urls:
            if not self.r.sismember('urls', url):
                yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
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

        keywords_xpath = [
            '//meta[@name="keywords"]/@content',
            '//meta[@name="keyWords"]/@content',
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

        for xpath in keywords_xpath:
            keywords = response.xpath(xpath).extract_first()
            if keywords:
                item['keywords'] = keywords.strip()
                break

        for pattern in content_pattern:
            paragraphs = response.xpath(
                f'//{pattern}').xpath('p/text()').extract()
            if paragraphs:
                item['content'] = '\r\n'.join(paragraphs)
                break

        yield item
