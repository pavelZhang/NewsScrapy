# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/8/4 22:28
@description:
    测试CrawlSpider用法,自动匹配url
"""
import redis
import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myScrapy.items import SiteUser, Article, Comment


class MySpider(CrawlSpider):
    name = 'huxiu_url'
    allowed_domains = []
    start_urls = ['https://www.huxiu.com/article']

    rules = (
        Rule(LinkExtractor(allow=('https://www.huxiu.com/article/\d+.html',)), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow=('https://www.huxiu.com/member/\d+.html',)), callback='parse_user', follow=True),
    )

    r = redis.Redis(host='10.45.10.201', port=6379)

    def _build_request(self, rule, link):
        """
        继承自 CrawlSpider，排除已抓取的url
        :param rule:
        :param link:
        :return:
        """
        if not self.r.sismember('urls', link.url):
            r = Request(url=link.url, callback=self._response_downloaded)
            r.meta.update(rule=rule, link_text=link.text)
            return r

    def parse_article(self, response):
        item = Article()
        item['url'] = response.url
        item['site'] = 'huxiu'

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
            'span[@class="article-share"]',
            'div[contains(@class, "mb24")]/i'
        ]
        comment_pattern = [
            'span[@class="article-pl pull-left"]',
            'span[@class="article-pl"]',
            'div[contains(@class, "comment")]/i'
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
                share_xpath = share_xpath.strip()
                if share_xpath.isdigit():
                    item['collect'] = share_xpath
                else:
                    item['collect'] = share_xpath[2:]
                break

        for pattern in comment_pattern:
            comment_xpath = response.xpath(
                f'//{pattern}/text()').extract_first()
            if comment_xpath:
                comment_xpath = comment_xpath.strip()
                if comment_xpath.isdigit():
                    item['comment'] = comment_xpath
                else:
                    item['comment'] = comment_xpath[2:]
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

    def parse_user(self, response):
        """
        解析用户信息

        user_info =
['\n                        ',
 '\n                        公司：广州有好戏网络科技有限公司                    ',
 '\n                        ',
 '\n                        邮箱：保密                    ',
 '\n                        ',
 '\n                        微博：',
 '                    ',
 '\n                        ',
 '\n                        微信：youhaoxifilm                    ',
 '\n                            ',
 '\n                            微信公众号：youhaoxifilm                        ']


        more_user_info =
['\n                            ',
 '\n                            真实姓名：毒眸                        ',
 '\n                            ',
 '\n                            手机：保密                        ',
 '\n                            ',
 '\n                            性别：保密                        ',
 '\n                            ',
 '\n                            所在地址：保密                        ',
 '\n                    ',
 '\n                    注册时间：2018-08-01                ']
        :param response:
        :return:
        """
        nickname = response.xpath('//div[@class="user-name"]/text()').extract_first().strip()
        item = SiteUser(site='huxiu', nickname=nickname, url=response.url)

        user_fields = {
            '公司': 'company',
            '邮箱': 'email',
            '微博': 'weibo',
            '微信': 'weichat',
            '真实姓名': 'username',
            '手机': 'telephone',
            '性别': 'gender',
            '所在地址': 'address',
            '注册时间': 'regtime',
        }

        user_info = response.xpath('//div[@class="user-info"]/text()').extract()
        more_user_info = response.xpath('//div[@class="more-user-info"]/text()').extract()
        user_info.extend(more_user_info)
        for line in user_info:
            if '：' not in line:
                continue

            key, value = line.strip().split('：', 1)
            if key in user_fields:
                item[user_fields[key]] = value

        yield item
