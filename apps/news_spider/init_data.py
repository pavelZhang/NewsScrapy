# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/8/10 22:30
@description:
"""
from apps.news_spider import models as _db


def create_site():
    """
    采集站点初始化
    :return:
    """
    sites = [
        {
            'name': '虎嗅',
            'code': 'huxiu',
            'home': 'https://www.huxiu.com/'
        },
        {
            'name': '观察者',
            'code': 'guancha',
            'home': 'https://www.guancha.cn/'
        },
        {
            'name': '澎湃',
            'code': 'thepaper',
            'home': 'https://www.thepaper.cn/'
        },
    ]
    for site in sites:
        _db.Site.objects.create(**site)


def main():
    create_site()
