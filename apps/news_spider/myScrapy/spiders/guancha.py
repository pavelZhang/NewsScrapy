# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/8/4 22:28
@description:
    观察者网内容爬取
"""
import redis
import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myScrapy.items import SiteUser, Article, Comment


class GuanChaSpider(CrawlSpider):
    name = 'guancha'
    allowed_domains = []
    start_urls = ['https://www.guancha.cn/']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Cookie': ''
    }

    rules = (
        Rule(LinkExtractor(allow=(r'https://www.guancha.cn/\w+/[\d_]+.shtml',)), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow=('https://user.guancha.cn/user/personal-homepage?uid=\d+',)), callback='parse_user', follow=True),
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

    def _article_title(self, response, item):
        """
        解析文章标题
        :param response:
        :param item:
        :return:
        """
        title_pattern = [
            'h3',
        ]
        for pattern in title_pattern:
            title = response.xpath(f'//{pattern}/text()').extract_first()
            if title:
                title = title.strip()
                item['title'] = title
                break

    def _article_author(self, response, item):
        """
        解析文章作者
        :param response:
        :param item:
        :return:
        """
        author_pattern = [
            '//div[@class="author-intro fix"]/p/a/text()',
        ]
        for pattern in author_pattern:
            author_name = response.xpath(f'{pattern}').extract_first()
            if author_name:
                item['author'] = author_name.strip()
                break

    def _article_keyword(self, response, item):
        """
        解析文章关键词
        :param response:
        :param item:
        :return:
        """
        author_pattern = [
            '//div[@class="key-word"]/span/text()',
        ]
        for pattern in author_pattern:
            xpath = response.xpath(
                f'{pattern}').extract()
            if xpath:
                item['keywords'] = ','.join(xpath[1:])
                break

    def _article_timestamp(self, response, item):
        """
        解析文章发布时间
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            '//div[@class="time fix"]/span/text()',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                item['timestamp'] = xpath
                break

    def _article_description(self, response, item):
        """
        解析文章描述信息
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            '//meta[@name="Description"]/@content',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                item['description'] = xpath
                break

    def _article_collect(self, response, item):
        """
        解析文章收藏数
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            '//a[@title="收藏本文"]/span/text()',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                item['collect'] = xpath
                break

    def _article_comment(self, response, item):
        """
        解析文章评论数
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            '//a[@title="查看评论"]/span/text()',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                item['comment'] = xpath
                break

    def _article_content(self, response, item):
        """
        解析文章内容
        :param response:
        :param item:
        :return:
        """
        content_pattern = [
            'div[@class="content all-txt"]',
        ]

        for pattern in content_pattern:
            paragraphs = response.xpath(f'//{pattern}').xpath('p/text()').extract()
            if paragraphs:
                item['content'] = '\r\n'.join(paragraphs)
                break

    def parse_article(self, response):
        item = Article()
        item['url'] = response.url
        item['site'] = self.name

        for func in (
                self._article_title,
                self._article_author,
                self._article_keyword,
                self._article_timestamp,
                self._article_description,
                self._article_collect,
                self._article_comment,
                self._article_content,
        ):
            func(response, item)

        print('comment-list', response.xpath('//div[@class="comment-list"]'))
        yield item

    def parse_user(self, response):
        """
        解析用户信息
        :param response:
        :return:
        """
        nickname = response.xpath('//div[@class="user-nick"]/text()').extract_first().strip()
        item = SiteUser(site=self.name, nickname=nickname, url=response.url)

        user_fields = {
            '公司': 'company',
            '邮箱': 'email',
            '微博': 'weibo',
            '微信': 'weichat',
            '真实姓名': 'username',
            '手机': 'telephone',
            '性别': 'gender',
            '所在地址': 'address',
            '所在城市': 'address',
            '注册时间': 'regtime',
            '生日': 'birthday',
            '职业': 'occupation',
            '教育背景': 'edubg',

        }

        match = response.xpath('//ul[@class="main_info"]/li')
        for each in match:
            key = each.xpath('text()').extract_first()
            value = each.xpath('span/text()').extract_first()
            if not key:
                continue
            if '：' in key:
                key.replace('：', '')
            key = key.strip()
            if key in user_fields:
                item[user_fields[key]] = value

        yield item
