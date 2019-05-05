# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/4/23 13:33
@description:
"""


def pagenator_data(model, request, *args, **kwargs):
    """
    统一数据分页 排序 函数
    :param model: Model
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    res = {
        'return': 'success',
        'data': {
            'all': 0,
            'page': 0,
            'detail': [],
        }
    }

    pagesize = int(request.GET.get('pagesize', 10))
    page = int(request.GET.get('page', 1))
    sortField = request.GET.get('sortField')
    sortOrder = request.GET.get('sortOrder')
    article_qs = model.objects.all()
    total = article_qs.count()
    if sortField and sortOrder:
        if sortOrder == 'ascend':
            article_qs = article_qs.order_by(sortField)
        else:
            article_qs = article_qs.order_by('-{}'.format(sortField))
    start_index = pagesize * (page - 1)
    end_index = pagesize * page - 1
    if start_index < total:
        article_qs = article_qs[start_index:end_index]
        data = list(article_qs.values())
    else:
        data = []
    res['data'] = {
        'all': total,
        'page': page,
        'detail': data,
    }
    return res
