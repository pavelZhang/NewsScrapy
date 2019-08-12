# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/8/10 22:26
@description:
    数据初始化
"""
from info import models as _db

from apps.news_spider import init_data


def create_user():
    """
    初始化用户
    :return:
    """
    _db.User.objects.create_user(username='admin', password='admin')


def main():
    create_user()
    init_data.main()


if __name__ == "__main__":
    main()
