# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/4/23 13:33
@description:
"""
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def pagenator_data(data, page, pagesize):
    ret = {}
    paginator = Paginator(data, pagesize)
    ret['all'] = paginator.count
    ret['page'] = int(page)
    try:
        ret['detail'] = paginator.page(page).object_list
    except PageNotAnInteger:
        ret['detail'] = paginator.page(1).object_list
        ret['page'] = 1
    except EmptyPage:
        ret['detail'] = []
    return ret
