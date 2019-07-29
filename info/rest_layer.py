# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/7/29 18:09
@description:
    定义一些 rest-framework 分层组件
"""

from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    增加分页参数 pagesize
    """
    page_size = 10
    page_size_query_param = 'pagesize'
    max_page_size = 1000