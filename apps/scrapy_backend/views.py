# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/4/21 15:52
@description:
"""
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from NewsScrapy.views import BaseView
from apps.scrapy_backend import models as _db
from NewsScrapy.utils import pagenator_data


class ScapyViewSet(BaseView):

    def article_list(self, request, *args, **kwargs):

        res = {
            'return': 'success',
            'data': {
                'all': 0,
                'page': 0,
                'detail': [],
            }
        }

        pagesize = request.GET.get('pagesize', 10)
        page = request.GET.get('page', 1)
        sortField = request.GET.get('sortField')
        sortOrder = request.GET.get('sortOrder')
        if not (sortField and sortOrder):
            article_qs = _db.Artical.objects.all()
        else:
            if sortOrder == 'ascend':
                article_qs = _db.Artical.objects.all().order_by(sortField)
            else:
                article_qs = _db.Artical.objects.all().order_by('-{}'.format(sortField))
        data = list(article_qs.values())
        res['data'] = pagenator_data(data, page, pagesize)
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
