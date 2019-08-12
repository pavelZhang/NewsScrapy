# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SiteUser(scrapy.Item):
    """
    站点用户
    """
    site = scrapy.Field()  # 站点
    username = scrapy.Field()  # 真实姓名
    nickname = scrapy.Field()  # 昵称
    url = scrapy.Field()  # url
    gender = scrapy.Field()  # 性别
    birthday = scrapy.Field()  # 生日
    occupation = scrapy.Field()  # 职业
    edubg = scrapy.Field()  # 教育背景
    telephone = scrapy.Field()  # 手机
    address = scrapy.Field()  # 地址
    regtime = scrapy.Field()  # 注册时间
    company = scrapy.Field()  # 公司
    email = scrapy.Field()  # 邮箱
    weibo = scrapy.Field()  # 微博
    weichat = scrapy.Field()  # 微信
    level = scrapy.Field()  # 用户等级
    points = scrapy.Field()  # 积分
    last_login = scrapy.Field()  # 最后登录时间


class Article(scrapy.Item):
    """
    咨询文章
    """
    site = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    keywords = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    description = scrapy.Field()
    share = scrapy.Field()  # 分享/转发
    comment = scrapy.Field()  # 评论数
    like = scrapy.Field()  # 点赞数
    dislike = scrapy.Field()  # 反对数
    collect = scrapy.Field()  # 收藏数


class Comment(scrapy.Item):
    """
    评论
    """
    author = scrapy.Field()  # 发言用户
    content = scrapy.Field()  # 内容
    timestamp = scrapy.Field()  # 发言时间
    like = scrapy.Field()  # 点赞数
    dislike = scrapy.Field()  # 反对数

    # 评论对象
    fid = scrapy.Field()  # id
    content_type = scrapy.Field()  # 类型 comment/article
