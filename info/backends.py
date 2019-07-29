# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/5/5 16:53
@description:
"""
import json
from django.core.cache import cache
from info.models import User
from django.contrib.auth.backends import ModelBackend

from info.utils.cache_utils import SystemCache


class ModelBackend(ModelBackend):
    """
    一个特殊的业务场景，需要使用数据库作为缓存，导致django在用户鉴权时频繁查询数据库，
    用户访问每个需要权限的页面都会查询一次。为了减少数据库开销，把用户数据缓存，
    需要重载AUTHENTICATION_BACKENDS配置。
    """

    def get_user(self, user_id):
        user = SystemCache.get_user_by_id(user_id)
        return user if user and self.user_can_authenticate(user) else None
