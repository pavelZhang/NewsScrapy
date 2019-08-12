# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
import traceback
import configparser

parser = configparser.ConfigParser()
CONF = r'D:\WorkSpace\my-github\info\newsinfo.conf'
parser.read(CONF)
HOME = parser.get('newsinfo', 'home')
sys.path.append(HOME)
import django

from myScrapy.elasticsearch_utils import ESUtils
from myScrapy.spiders.huxiu import INDEX_NAME, DOC_NAME
from myScrapy.items import SiteUser, Article, Comment

os.environ['DJANGO_SETTINGS_MODULE'] = 'info.settings'
django.setup()
from apps.news_spider import models as _db


class MyscrapyPipeline(object):

    def __init__(self):
        self.esutils = ESUtils()
        self.es = self.esutils.connect()

    def process_item(self, item, spider):
        self.es.index(INDEX_NAME, DOC_NAME, dict(item), id=item['url'])
        return item


class PGPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        item2func = {
            SiteUser: self.create_user,
            Article: self.create_article,
            Comment: '',
        }
        try:
            item2func[type(item)](item)
            spider.r.sadd('urls', item['url'])
        except Exception as e:
            spider.r.srem('urls', item['url'])
            print(traceback.format_exc())
        return item

    def create_user(self, item):
        """
        1. 查询是否存在 siteuser, 不存在则新建，否则更新
        :param item:
        :return:
        """
        site = item.pop('site')
        siteuser = _db.SiteUser.objects.filter(nickname=item['nickname']).first()
        if not siteuser:
            site = _db.Site.objects.filter(code=site).first()
            _db.SiteUser.objects.create(site=site, **dict(item))
        else:
            siteuser.update(**dict(item))

    def create_article(self, item):
        """
        1. 查询是否存在 siteuser， 不存在则新建
        :param item:
        :return:
        """
        author = item.pop('author')
        site = item.pop('site')
        siteuser = _db.SiteUser.objects.filter(nickname=author).first()
        if not siteuser:
            site = _db.Site.objects.filter(code=site).first()
            siteuser = _db.SiteUser.objects.create(
                nickname=author,
                site=site
            )
        _db.Artical.objects.create(author=siteuser, **dict(item))
