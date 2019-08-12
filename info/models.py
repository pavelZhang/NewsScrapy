# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/4/1 21:29
@description:
"""
import json
import logging
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, URLValidator, validate_ipv4_address

from django.contrib.auth.models import Group

logger = logging.getLogger('django.view')


class BaseManager(models.Manager):
    """
    定义新的查询方法，只获取 row_status='normal' 的数据
    """

    def get_queryset(self):
        return super().get_queryset().filter(row_status='normal')


class AbstractModel(models.Model):
    """
    1. 定义新属性 objects_nl, 使用方式等同于 objects 属性
    2. 重写 delete 方法，修改 row_status='delete'
    """
    # objects = models.Manager()
    # objects = BaseManager.from_queryset(BaseQuerySet)()
    # row_status = models.CharField(max_length=64, default='normal')
    # objects = BaseManager()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def delete(self):
        self.row_status = 'delete'
        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def fields_check(self):
        """
        1. 数据更新前，判断是否为更新操作，字段是否允许更新
        2. 是否匹配正则数据校验
        return 校验失败的字段
        """
        ret = []
        for field in self._meta.get_fields():
            pre_value = field.value_from_object(self)
            # logger.info('pre_value: ' + pre_value)
        return ret

    def json(self):
        data = {}
        for field in self._meta.fields:
            value = field.value_from_object(self)
            if type(value) is datetime.date or type(value) is datetime.datetime:
                value = datetime.datetime.strftime(value, '%Y-%m-%d %H:%M:%S')

            data[field.name] = value
        return data

    def json_str(self):
        return json.dumps(self.json())

    class Meta:
        abstract = True


class User(AbstractUser, AbstractModel):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
