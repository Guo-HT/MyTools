from django.urls import path, re_path
from django.conf.urls import include, url
from django.views import static
from django.conf import settings
from django.views.generic.base import RedirectView
from Resume import views

# /resume/*
urlpatterns = [
    re_path(r'^$', views.index, name="index"),  # 主页
    re_path(r'^index$', views.index, name="index"),  # 主页
    re_path(r'^upload$', views.upload, name="upload"),  # 上传页
    re_path(r'^upload_file$', views.upload_file, name="upload_file"),  # 上传
    re_path(r'^have_resume$', views.have_resume, name="have_resume"),  # 判断是否已存简历
    re_path(r'^show/', views.show, name="show"),  # 展示简历
    re_path(r'^show2/', views.show2, name="show2"),  # 展示简历
    re_path(r'^index_get_resumes', views.index_get_resumes, name="index_get_resumes"),  # 主页简历列表
    re_path(r'^watch_num', views.watch_num, name="watch_num"),  # 浏览量统计
]