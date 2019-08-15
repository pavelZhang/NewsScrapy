"""info URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from info import views

urlpatterns = [

    url(r'^version$', views.SystemView.as_view(func='version', method='get')),

    url(r'^user/login$', views.UserViewSet.as_view(func='login', method='post')),
    url(r'^user/logout$', views.UserViewSet.as_view(func='logout', method='post')),
    url(r'^user/logout$', views.UserViewSet.as_view(func='logout', method='post')),

    url(r'^user/list$', views.UserViewSet.as_view(func='user_list', method='get')),
    url(r'^user/(?P<pk>\d+)/detail$', views.UserViewSet.as_view(func='user_detail', method='get')),
    url(r'^user/(?P<pk>\d+)/add$', views.UserViewSet.as_view(func='user_add', method='post')),
    url(r'^user/(?P<pk>\d+)/update$', views.UserViewSet.as_view(func='user_update', method='post')),
    url(r'^user/(?P<pk>\d+)/delete$', views.UserViewSet.as_view(func='user_delete', method='post')),

    # 下载
    url(r'^common/template/download$',
        views.CommonView.as_view(func='template_download', method='get')),

    url(r'^scrapy/', include('news_spider.urls')),
]
