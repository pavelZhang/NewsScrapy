# coding=utf-8
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/2/26 20:47
@description:
    2. 屏蔽异常报错修正
"""

import re
import logging
import traceback

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from NewsScrapy.settings import EXCLUDE_URL

logger = logging.getLogger('django.middleware')

exclued_path = [re.compile(item) for item in EXCLUDE_URL]


class CommonMiddle(MiddlewareMixin):
    """
    1. 登录验证
    2. 返回 json 格式数据
    """

    def process_request(self, request):
        """
        登录验证
        1. 过滤掉不需要验证的 url
        2. 判断用户是否登录，未登录返回
        """
        ret = {'message': 'please login', 'return': 'error'}
        url_path = request.path
        exclued = False
        for each in exclued_path:
            if re.search(each, url_path):
                exclued = True

        if not exclued:
            if not request.user.is_authenticated:
                # pass
                return ret

    def process_response(self, request, response):
        """
        1. 统一的国际化转换
        2. 返回 json 格式数据
        """
        if isinstance(response, dict):
            if not response.get('status_code'):  # 处理异常的返回
                ret = {
                    'status_code': 200,
                    'response': response
                }
            else:
                ret = response
        else:
            return response
            ret = {
                'status_code': response.status_code,
                'response': {
                    'return': 'success' if response.status_code == 200 else 'error',
                }
            }

        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = 'http://localhost:8000'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] = 'Content-Type,XFILENAME,XFILECATEGORY,XFILESIZE,Access-Control-Allow-Origin,Origin'
        response['Access-Control-Allow-Methods'] = '*'
        return response

    '''
    def process_view(self, request, callback, *args, **kwargs):
        """
        返回数据封装
        """
        data = callback(request, *args, **kwargs)
        return data
    '''


class ExceptionHandleMiddle(MiddlewareMixin):
    """
    1. 异常处理
    """

    def process_exception(self, request, exception):
        """
        异常处理
        """

        logger.error(traceback.format_exc())
        ret = {
            'status_code': 500,
            'response': {
                'return': 'error',
                'message': traceback.format_exc()
            }
        }
        return ret
