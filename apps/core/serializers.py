# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/7/25 18:21
@description:
"""
from apps.core import models as _db
from rest_framework import serializers


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = _db.Artical
        fields = [
            "title",
            "author",
            "keywords",
            "description",
            "content",
            "url",
            "share",
            "comment",
            "timestamp",
        ]
