"""
OS模版页面视图对应的url文件
"""

from django.conf.urls import url
from apps.news_spider import views
from apps.news_spider import models as _db

urlpatterns = [
    url(r'^article/list$', views.ScapyViewSet.as_view(
        method='get',
        func='article_list',
        permissions=['news_spider.view_artical'],
    )),

    url(r'^article/(?P<pk>\d+)/detail$', views.ScapyViewSet.as_view(
        method='get',
        func='article_detail',
        permissions=['news_spider.view_artical'],
        permission_model=_db.Artical
    )),

]
