# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/8/4 22:28
@description:
    cnbeta 文章爬取
"""
import re
import datetime
import redis
import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myScrapy.items import SiteUser, Article, Comment


class CnBetaSpider(CrawlSpider):
    name = 'cnbeta'
    allowed_domains = []
    start_urls = ['https://www.cnbeta.com/']

    rules = (
        Rule(LinkExtractor(allow=(
            'http://www.cnbeta.com/articles/\w+/\d+.htm',
            'https://hot.cnbeta.com/articles/\w+/\d+.htm'
        )), callback='parse_article', follow=True),
        # Rule(LinkExtractor(allow=('https://cnbeta.com/comment/\w+/\d+.htm',)), callback='parse_comment', follow=True),
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
            '//header[@class="title"]/h1/text()',
        ]
        for pattern in title_pattern:
            title = response.xpath(pattern).extract_first()
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
            # '//div[@class="news_about"]/p/text()',
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
            '//meta[@name="keywords"]/@content',
        ]
        for pattern in author_pattern:
            xpath = response.xpath(
                f'{pattern}').extract_first()
            if xpath:
                item['keywords'] = xpath
                break

    def _article_timestamp(self, response, item):
        """
        解析文章发布时间
        :param response:
        :param item:
        :return:
        """
        intab = "年月"
        outtab = "--"
        trantab = str.maketrans(intab, outtab)

        xpath_pattern = [
            '//div[@class="meta"]/span/text()',
            '//div[@class="video_info_left"]/span/text()',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract()
            if xpath:
                for each in xpath:
                    if re.search(r'\d+[:-]\d+', each):
                        item['timestamp'] = each.strip().translate(trantab).replace('日', '')
                        break

    def _article_description(self, response, item):
        """
        解析文章描述信息
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            '//meta[@name="description"]/@content',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                item['description'] = xpath
                break

    def _article_read(self, response, item):
        """
        解析文章阅读数
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            '//span[@title="人气"]/span/text()',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                item['read'] = xpath
                break

    def _article_collect(self, response, item):
        """
        解析文章收藏数
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            # '//a[@title="收藏本文"]/span/text()',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                item['collect'] = xpath
                break

    def _article_like(self, response, item):
        """
        解析文章点赞数
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            '//div[@class="like"]/text()',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                item['like'] = xpath.strip().split()[0]
                break

    def _article_dislike(self, response, item):
        """
        解析文章反对数
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            '//div[@class="dislike"]/text()',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                item['dislike'] = xpath.strip().split()[0]
                break

    def _article_comment(self, response, item):
        """
        解析文章评论数
        :param response:
        :param item:
        :return:
        """
        xpath_pattern = [
            '//a[@class="comment-num"]/span/text()',
        ]
        for pattern in xpath_pattern:
            xpath = response.xpath(f'{pattern}').extract_first()
            if xpath:
                xpath = xpath.strip().replace('（', '').replace('）', '')
                if 'k' in xpath:
                    xpath = xpath.replace('k', '')
                    xpath = float(xpath) * 1000
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
            '//div[@class="article-content"]/p/text()',
        ]

        for pattern in content_pattern:
            xpath = response.xpath(pattern).extract()
            if xpath:
                item['content'] = '\r\n'.join(xpath)
                break

    def parse_article(self, response):
        """
        评论获取 https://www.thepaper.cn/newDetail_commt.jsp?contid=4143977
        :param response:
        :return:
        """

        item = Article()
        item['url'] = response.url
        item['site'] = self.name

        for func in (
                self._article_title,
                self._article_author,
                self._article_keyword,
                self._article_timestamp,
                self._article_description,
                self._article_read,
                self._article_collect,
                self._article_like,
                self._article_dislike,
                self._article_comment,
                self._article_content,
        ):
            func(response, item)

        yield item

    def parse_comment(self, response):
        """
        解析评论
        :param response:
        :return:
        """
        comment_que = response.xpath('//ul[@class="J_commt_list"]')
        for xpath in comment_que:
            item = Comment(
                site=self.name,
                url=response.url.replace('comment', 'articles'),
                content_type='Artical'
            )
            username = xpath.xpath('div/div[@class="aqwright"]/h3/a/text()').extract_first()
            if username:
                item['author'] = username
            timestamp = xpath.xpath('div/div[@class="aqwright"]/h3/span/text()').extract_first()
            if timestamp:
                desc = {
                    '分钟前': 1,
                    '小时前': 60,
                    '天前': 60 * 24,
                    '月前': 60 * 24 * 30,
                    '年前': 60 * 24 * 365
                }
                for key, value in desc.items():
                    if key in timestamp:
                        timestamp = timestamp.replace(key, '')
                        if timestamp.isdigit():
                            item['timestamp'] = datetime.datetime.now() - datetime.timedelta(minutes=int(timestamp) * value)
                        else:
                            item['timestamp'] = timestamp
                        break

            content = xpath.xpath('div/div[@class="aqwright"]/div[@class="ansright_cont"]/a/text()').extract_first()
            if content:
                item['content'] = content
            like = xpath.xpath('div/div[@class="aqwright"]/div[@class="ansright_time"]/a/text()').extract_first()
            if like:
                if 'k' in like:
                    like = like.replace('k', '')
                    like = float(like) * 1000
                item['like'] = like

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
                key = key.replace('：', '')
            key = key.strip()
            if key in user_fields:
                item[user_fields[key]] = value

        yield item
