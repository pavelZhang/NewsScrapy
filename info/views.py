# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/4/1 21:18
@description:
"""

import os
import traceback
import logging

from django.views.generic import View
from django.http import FileResponse
from django.utils.http import urlquote
from django.forms.models import model_to_dict
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout

from info import models as _db
from django.core.exceptions import ValidationError
from info.utils import pagenator_data

# from ire_web.settings import DIMENSION_DOCUMENTS_HOME

DIMENSION_DOCUMENTS_HOME = "/"

logger = logging.getLogger('django.view')


class BaseView(View):
    """
    1. method  指定 request 方法，判断 请求方法 是否正确
    2. 通过 func 属性，调用View的func方法，如果找不到该方法，调用默认实现
    3. 权限验证
    """
    func = ''
    method = 'get'
    permissions = []  # url 请求需要的权限
    permission_model = None  # 权限操作对象
    logger = logger

    def dispatch(self, request, *args, **kwargs):
        check, permission = self.permission_check(request, *args, **kwargs)
        if not check:
            ret = {
                'status_code': 403,
                'response': {
                    'return': 'error',
                    'message': '{} is forbidden'.format(permission)
                }
            }
            return ret

        handler = None
        request_method = request.method.lower()
        if request_method in ('get', 'post', 'put', 'delete'):
            if self.method.lower() != request_method:
                ret = {
                    'status_code': 405,
                    'response': {
                        'return': 'error',
                        'message': 'Method not allowed'
                    }
                }
                return ret
        if self.func and hasattr(self, self.func):
            handler = getattr(self, self.func)
        if not handler:
            return super(BaseView, self).dispatch(request, *args, **kwargs)
        return handler(request, *args, **kwargs)

    def permission_check(self, request, *args, **kwargs):
        """
        1. 超级用户不验证权限
        2. 分别验证 global permission 和 object permission
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        obj = None
        pk = kwargs.get('pk')
        if not request.user.is_superuser:
            if self.permissions:
                if pk and self.permission_model:
                    obj = self.permission_model.objects.get(id=pk)
                for permission in self.permissions:
                    if obj:
                        check = request.user.has_perm(permission, obj)
                    else:
                        check = request.user.has_perm(permission)
                    if not check:
                        logger.info('permission {} on {} forbidden, '.format(permission, obj.id))
                        return False, permission
        return True, None


class UserViewSet(BaseView):
    """
    用户处理View
    """

    def login(self, request, *args, **kwargs):
        """
        用户登录接口
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.info('username: {}'.format(username))
        logger.info('password: {}'.format(password))
        user = authenticate(username=username, password=password)
        logger.info("user: {}".format(user))

        if user is not None:
            login(request, user)
            ret = {
                'code': '',
                'return': 'success',
                'currentAuthority': 'admin',
                'type': 'admin' if user.is_superuser else 'user',
                'message': '',
            }
        else:
            ret = {
                'code': '',
                'return': 'failed',
                'currentAuthority': '',
                'type': '',
                'message': 'authenticate error',
            }

        return ret

    def logout(self, request, *args, **kwargs):
        """
        用户登出接口
        """
        logout(request)
        return {'code': '', 'return': 'success', 'message': ''}

    def user_list(self, request, *args, **kwargs):
        """
        用户列表
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
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        users = _db.User.objects.all().values()
        data = pagenator_data(users, page, pagesize)
        res['data'] = data
        return res

    def user_detail(self, request, *args, **kwargs):
        """
        查询单个用户详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = {
            'return': 'success',
            'data': {}
        }
        pk = kwargs.get('pk')
        user = _db.User.objects.filter(id=pk).first()
        if not user:
            res['return'] = 'error'
            res['msg'] = 'invalid pk'
            return res

        res['data'] = model_to_dict(user)
        return res

    def user_add(self, request, *args, **kwargs):
        """
        新建用户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = {
            'return': 'success',
            'data': '',
        }
        param = request.POST.dict()
        try:
            user = _db.User.objects.create_user(**param)
            res['data'] = user.id
        except Exception as e:
            res['msg'] = "用户创建失败"
        return res

    def user_update(self, request, *args, **kwargs):
        """
        更新用户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = {
            'return': 'success',
            'msg': '用户创建成功',
        }

        pk = kwargs.get('pk')
        param = request.POST.dict()
        try:
            user = _db.User.objects.get(id=pk)
            user.update(**param)
        except Exception as e:
            res['msg'] = "用户创建失败"
        return res

    def user_delete(self, request, *args, **kwargs):
        """
        删除用户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = {
            'return': 'success',
            'msg': _('用户删除成功'),
        }

        pk = kwargs.get('pk')
        try:
            user = _db.User.objects.get(id=pk)
            user.delete()
        except Exception as e:
            res['msg'] = _("用户删除失败")
        return res


class GroupViewSet(BaseView):
    """
    用户组
    """

    def group_list(self, request, *args, **kwargs):
        """
        用户列表
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
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        groups = _db.Group.objects.all().values()
        data = pagenator_data(groups, page, pagesize)
        res['data'] = data
        return res

    def group_detail(self, request, *args, **kwargs):
        """
        查询单个用户详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = {
            'return': 'success',
            'data': {}
        }
        pk = kwargs.get('pk')
        group = _db.Group.objects.filter(id=pk).first()
        if not group:
            res['return'] = 'error'
            res['msg'] = 'invalid pk'
            return res

        res['data'] = model_to_dict(group)
        return res

    def group_add(self, request, *args, **kwargs):
        """
        新建用户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = {
            'return': 'success',
            'data': '',
        }
        param = request.POST.dict()
        try:
            group = _db.Group.objects.create_user(**param)
            res['data'] = group.id
        except Exception as e:
            res['msg'] = "用户创建失败"
        return res

    def group_update(self, request, *args, **kwargs):
        """
        更新用户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = {
            'return': 'success',
            'msg': '用户创建成功',
        }

        pk = kwargs.get('pk')
        param = request.POST.dict()
        try:
            group = _db.Group.objects.get(id=pk)
            group.update(**param)
        except Exception as e:
            res['msg'] = "用户创建失败"
        return res

    def group_delete(self, request, *args, **kwargs):
        """
        删除用户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = {
            'return': 'success',
            'msg': _('用户删除成功'),
        }

        pk = kwargs.get('pk')
        try:
            group = _db.Group.objects.get(id=pk)
            group.delete()
        except Exception as e:
            res['msg'] = _("用户删除失败")
        return res


class CommonView(BaseView):
    """
    通用视图处理
    """

    def template_download(self, request, *args, **kwargs):
        """
        规划文件模板下载
        """
        res = {
            'return': 'success',
            'message': '模板下载成功'
        }
        template_name = request.GET.get('template_name')
        assert template_name
        try:
            path = os.path.join(DIMENSION_DOCUMENTS_HOME, template_name).encode('utf8')
            res = FileResponse(open(path, 'rb'))
            res['Content-Type'] = 'application/octet-stream'
            attachment = 'attachment;filename="{name}"'.format(name=urlquote(template_name))
            res['Content-Disposition'] = attachment
        except Exception as e:
            self.logger.error(traceback.format_exc())
            res['return'] = 'error'
            res['message'] = '模板下载失败'
        return res


class SystemView(BaseView):
    """
    系统级接口
    """

    def version(self, request, *args, **kwargs):
        """
        版本说明, 校验接口
        """
        res = dict(
            name='Template',
            version='v1.0',
            copyright='***',
            developer='***',
            publish_date='2019-04-01',
            desc='',
            link='',
        )
        return res
