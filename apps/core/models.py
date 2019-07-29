# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/4/1 21:29
@description:
"""
import logging
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User as Auth_User

logger = logging.getLogger('django.view')

from info.models import AbstractModel


class Artical(AbstractModel):
    """
    文章表
    """
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    keywords = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    content = models.TextField()
    url = models.CharField(max_length=64)
    share = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)
    timestamp = models.CharField(max_length=64)

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('read_article', 'read article'),
        )

class Scrapy(AbstractModel):
    """
    爬虫
    """
    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, verbose_name='程序标识')


