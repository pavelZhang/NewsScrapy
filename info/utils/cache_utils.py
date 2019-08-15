# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/5/5 16:26
@description:
"""
import json

from info.models import User
from django.core.cache import cache
from django_redis import get_redis_connection

from info import settings


class SystemCache(object):
    conn = get_redis_connection("default")

    @classmethod
    def update_user(cls, user):
        """
        用户信息缓存
        :param user:
        :return:
        """

        cache_key = 'user:%s' % user.id
        cls.conn.set(cache_key, user.json_str(), settings.SESSION_COOKIE_AGE)

    @classmethod
    def get_user_by_id(cls, id):
        cache_key = 'user:%s' % id
        user = cls.conn.get(cache_key)
        if user:
            user = json.loads(user)
            user = User(**user)
        else:
            try:
                user = User.objects.get(pk=id)
                cls.update_user(user)
            except User.DoesNotExist:
                return None
        return user
