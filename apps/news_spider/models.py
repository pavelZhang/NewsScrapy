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


class Site(AbstractModel):
    """
    站点表
    """
    name = models.CharField(max_length=128, verbose_name='站点名')
    code = models.CharField(max_length=128, verbose_name='编码')
    home = models.CharField(max_length=128, null=True, blank=True, verbose_name='主页')
    desc = models.CharField(max_length=128, null=True, blank=True, verbose_name='简介')


class SiteUser(AbstractModel):
    """
    站点用户
    """
    site = models.ForeignKey(Site, verbose_name='站点', on_delete=models.CASCADE)
    username = models.CharField(max_length=128, null=True, blank=True, verbose_name='姓名')
    nickname = models.CharField(max_length=128, unique=True, verbose_name='昵称')
    url = models.CharField(max_length=128, null=True, blank=True, verbose_name='url')
    gender = models.CharField(max_length=64, null=True, blank=True, verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    occupation = models.CharField(max_length=128, null=True, blank=True, verbose_name='职业')
    edubg = models.CharField(max_length=128, null=True, blank=True, verbose_name='教育背景')
    telephone = models.CharField(max_length=128, null=True, blank=True, verbose_name='手机')
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name='地址')
    regtime = models.DateTimeField(null=True, blank=True, verbose_name='注册时间')
    company = models.CharField(max_length=256, null=True, blank=True, verbose_name='公司')
    email = models.CharField(max_length=256, null=True, blank=True, verbose_name='邮箱')
    weibo = models.CharField(max_length=128, null=True, blank=True, verbose_name='微博')
    weichat = models.CharField(max_length=128, null=True, blank=True, verbose_name='微信')
    level = models.CharField(max_length=128, null=True, blank=True, verbose_name='用户等级')
    points = models.IntegerField(null=True, blank=True, verbose_name='积分')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')


class Artical(AbstractModel):
    """
    文章表
    """
    title = models.CharField(max_length=256, null=True, blank=True, verbose_name='标题')
    author = models.ForeignKey(SiteUser, null=True, blank=True, verbose_name='站点用户', on_delete=models.CASCADE)
    keywords = models.CharField(max_length=256, null=True, blank=True, verbose_name='所属站点')
    content = models.TextField(verbose_name='内容')
    url = models.CharField(max_length=128, verbose_name='url')
    timestamp = models.DateTimeField(verbose_name='发表时间')
    description = models.TextField(null=True, blank=True, verbose_name='介绍')
    share = models.IntegerField(null=True, blank=True, verbose_name='分享')
    comment = models.IntegerField(null=True, blank=True, verbose_name='评论数')
    like = models.IntegerField(null=True, blank=True, verbose_name='点赞数')
    dislike = models.IntegerField(null=True, blank=True, verbose_name='反对数')
    collect = models.IntegerField(null=True, blank=True, verbose_name='收藏数')
    read = models.IntegerField(null=True, blank=True, verbose_name='阅读数')

    class Meta:
        ordering = ['-timestamp']
        permissions = (
            ('read_article', 'read article'),
        )


class Comment(AbstractModel):
    """
    评论
    """
    author = models.ForeignKey(SiteUser, verbose_name='发言用户', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容')
    timestamp = models.DateTimeField(verbose_name='发表时间')
    like = models.IntegerField(null=True, blank=True, verbose_name='点赞数')
    dislike = models.IntegerField(null=True, blank=True, verbose_name='反对数')

    # 评论对象
    fid = models.IntegerField(null=True, blank=True, )  # id
    content_type = models.CharField(null=True, blank=True, max_length=128)  # 类型 comment/article
