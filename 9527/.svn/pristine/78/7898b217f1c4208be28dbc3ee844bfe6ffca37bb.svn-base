#!/usr/bin/python
# -*- coding:utf-8 -*-


from django.conf.urls import patterns, url

urlpatterns = patterns("mz_article.views",

                       # 文章详情
                       url(r'^article/save/$', 'article_save', name='article_save'),
                       url(r'^article/edit/$', 'article_edit', name='article_edit'),
                       url(r'^article/list/$', 'article_list', name='article_list'),
                       url(r'^article/addpic/$', 'article_adpic', name='article_addpic'),
                       url(r'^articletitle/save/$', 'articletitle_save', name='article_articletitlesave'),
                       url(r'^article/chaginfo/$', 'article_infochag', name='article_chaginfo'),
                       url(r'^article/confchg/$', 'article_confchg', name='article_confchag'),
                       )

urlpatterns += patterns("mz_article.articleType",
                        # 文章类型
                        url(r'^articleType/save/$', 'articleType_save', name='articleType_save'),
                        url(r'^articleType/edit/$', 'articleType_edit', name='articleType_edit'),
                        url(r'^articleType/list/$', 'articleType_list', name='articleType_list'),

                        # 更新文章类型的isVisible
                        url(r'^articleType/update/isHomepage/ajax/$', 'articleType_isHomepage_save',
                            name='articleType_update_isHomepage'),
                        # 更新文章类型的isVisible
                        url(r'^articleType/update/isVisible/ajax/$', 'articleType_isVisible_save',
                            name='articleType_update_isVisible'),
                        # 更新文章类型的isCareer
                        url(r'^articleType/update/isCareer/ajax/$', 'articleType_isCareer_save',
                            name='articleType_update_isCareer'),
                        )
