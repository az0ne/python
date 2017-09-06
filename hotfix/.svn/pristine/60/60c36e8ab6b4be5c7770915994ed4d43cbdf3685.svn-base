# -*- coding: utf8 -*-

from django.conf.urls import patterns, url
from mz_wiki import views

urlpatterns = patterns(
    '',
    # wiki首页
    url(r'^$', views.wiki_index, name="index"),
    # wiki分类详情页
    url(r'^(?P<short_name>\w+)/$', views.wiki_course_type, name="course_type"),
    # wiki知识点详情页
    url(r'^(?P<course_short_name>\w+|\w+[-_]\w+)/(?P<item_short_name>\w+|\w+[-_]\w+)/$', views.wiki_item_detail, name="item_detail"),
)
