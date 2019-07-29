# -*- coding:utf-8 -*-
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/5/6 15:03
@description:
"""

from celery import shared_task
from celery.utils.log import get_task_logger
from info.celery import app

logger = get_task_logger(__name__)

@shared_task
def add(x, y):
    logger.info('in task add')
    return x + y