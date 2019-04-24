"""
OS模版页面视图对应的url文件
"""

from django.conf.urls import url
from apps.scrapy_backend import views
from apps.scrapy_backend import models as _db

urlpatterns = [
    url(r'^article/list$', views.ScapyViewSet.as_view(
        method='get',
        func='article_list',
        permissions=['scrapy_backend.view_artical'],
    )),

    url(r'^article/(?P<pk>\d+)/detail$', views.ScapyViewSet.as_view(
        method='get',
        func='article_detail',
        permissions=['scrapy_backend.view_artical'],
        permission_model=_db.Artical
    )),

]
