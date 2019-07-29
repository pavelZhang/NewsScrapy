"""
OS模版页面视图对应的url文件
"""

from django.conf.urls import url
from apps.core import views
from apps.core import models as _db
from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
