from django.urls import path, re_path
from django.conf.urls import include, url
from django.views import static
from django.conf import settings
from django.views.generic.base import RedirectView
from Online import views

# /online/*
urlpatterns = [
    re_path(r'^$', views.index, name="index"),  # 主页
    re_path(r'^index$', views.index, name="index"),  # 主页
    re_path(r'^epq_test$', views.epq_test, name="epq_test"),  # 主页
]