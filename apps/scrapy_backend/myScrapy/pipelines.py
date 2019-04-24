# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import django

from myScrapy.elasticsearch_utils import ESUtils
from myScrapy.spiders.huxiu import INDEX_NAME, DOC_NAME

os.environ['DJANGO_SETTINGS_MODULE'] = 'NewsScrapy.settings'
django.setup()
from apps.scrapy_backend import models as _db


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
        _db.Artical.objects.create(**dict(item))
        return item
