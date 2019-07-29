# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/4/21 15:52
@description:
"""
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from apps.core import models as _db
from info.utils import pagenator_data

from . import tasks

from rest_framework import viewsets
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = _db.Artical.objects.all().order_by('-timestamp')
    serializer_class = ArticleSerializer
