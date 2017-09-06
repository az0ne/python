# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^course/(?P<keyword>.*)-(?P<page_index>\d+)/$', 'mz_homepage.search.get_search_course',
        name='search_course'),
    url(r'^article/(?P<keyword>.*)-(?P<page_index>\d+)/$', 'mz_homepage.search.get_search_article',
        name='search_article'),
    url(r'^wiki/(?P<keyword>.*)-(?P<page_index>\d+)/$', 'mz_homepage.search.get_search_wiki',
        name='search_wiki'),
)
