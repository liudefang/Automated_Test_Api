"""api_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path

from ApiTest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^index/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^home/$', views.home),

    # 项目
    url(r'^project/$', views.project),
    url(r'^add_project/$', views.add_project),
    re_path(r'project/(\d+)/(edit|delete)', views.edit_project),
    # url(r'^del_project/$', views.del_project),

    # 模块
    url(r'^module/$', views.module),
    url(r'^add_module/$', views.add_module),
    re_path(r'^module/(\d+)/(edit|delete)', views.edit_module),

    # 用例
    url(r'^api_case/$', views.api_case),
    url(r'^add_case/$', views.add_case),
    re_path(r'^api_case/(\d+)/(edit|delete)', views.edit_case),

    # 用例步骤
    url(r'^api_step/$', views.api_step),
    url(r'^add_step/$', views.add_step),
    url(r'^edit_step/$', views.edit_step),
    re_path(r'^api_step/(\d+)/delete', views.del_step),

    # 环境
    url(r'^env/$', views.environment),
    url(r'^add_env/$', views.add_env),
    url(r'^edit_env/$', views.edit_env),
    re_path(r'env/(\d+)/delete', views.del_env),


    # 邮箱
    url(r'^email/$', views.email),
    url(r'^add_email/$', views.add_email),
    # url(r'^edit_email/$', views.edit_email),
    re_path(r'email/(\d+)/delete', views.del_email),
]
