# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/4/21 15:52
@description:
"""
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from info.views import BaseView
from apps.news_spider import models as _db
from info.utils import pagenator_data


class ScapyViewSet(BaseView):

    def article_list(self, request, *args, **kwargs):
        res = pagenator_data(_db.Artical, request, *args, **kwargs)
        return res

    def article_detail(self, request, *args, **kwargs):
        res = {
            'return': 'success',
            'data': {}
        }

        pk = kwargs.get('pk')
        article = _db.Artical.objects.get(id=pk)
        res['data'] = model_to_dict(article)
        return res
