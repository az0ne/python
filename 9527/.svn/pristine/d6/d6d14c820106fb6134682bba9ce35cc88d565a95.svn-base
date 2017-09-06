#!/usr/bin/python
# -*- coding:utf-8 -*-


from django.conf.urls import patterns, url

urlpatterns = patterns('mz_homepage',
                       # 首页文章管理
                       url(r'^homepageArticle/list/$', 'homepage_article.homepage_article_list',
                           name='homepageArticle_list'),
                       url(r'^homepageArticle/edit/$', 'homepage_article.homepage_article_edit',
                           name='homepageArticle_edit'),
                       url(r'^homepageArticle/save/$', 'homepage_article.homepage_article_save',
                           name='homepageArticle_save'),
                       # 首页wiki管理
                       url(r'^homepageWiki/list/$', 'homepage_wiki.homepage_wiki_list',
                           name='homepageWiki_list'),
                       url(r'^homepageWiki/edit/$', 'homepage_wiki.homepage_wiki_edit',
                           name='homepageWiki_edit'),
                       url(r'^homepageWiki/save/$', 'homepage_wiki.homepage_wiki_save',
                           name='homepageWiki_save'),

                       )
