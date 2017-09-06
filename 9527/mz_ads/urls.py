#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns("mz_ads",
                       # 首页标题
                       url(r'^bannermng/list/$', "banner.banner_list", name="banner_list"),
                       url(r'^bannermng/edit/$', "banner.banner_edit", name="banner_edit"),
                       url(r'^bannermng/save/$', "banner.banner_save", name="banner_save"),

                       # 广告
                       url(r'^careernewAd/list/$', "careernewAd.career_new_ad_list", name="career_newAd_list"),
                       url(r'^careernewAd/edit/$', "careernewAd.update_career_new_ad", name="update_career_new_ad"),
                       url(r'^careernewAd/save/$', "careernewAd.save_career_new_ad", name="save_career_new_ad"),

                       # 职业广告
                       url(r'^careerAd/list/$', "careerAd.career_ad_list", name="careerAd_list"),
                       url(r'^careerAd/edit/$', "careerAd.career_ad_edit", name="careerAd_edit"),
                       url(r'^careerAd/save/$', "careerAd.career_ad_save", name="careerAd_save"),

                       # wiki广告
                       url(r'^wiki_ad/list/$', "wiki_ad.wiki_ad_list", name="wiki_ad_list"),
                       url(r'^wiki_ad/edit/$', "wiki_ad.wiki_ad_edit", name="wiki_ad_edit"),

                       # 小课程广告
                       url(r'^course_ad/list/$', "course_ad.course_ad_list", name="course_ad_list"),
                       url(r'^course_ad/edit/$', "course_ad.course_ad_edit", name="course_ad_edit"),
                       url(r'^course_ad/update_status/$', "course_ad.ajax_update_course_ad_status",
                           name="update_course_ad_status"),
                       # app广告
                       url(r'^app_ad/list/$', "app_career_ad.app_career_ad_list", name="app_ad_list"),
                       url(r'^app_ad/edit/$', "app_career_ad.app_career_ad_edit", name="app_ad_edit"),
                       url(r'^app_ad/save/$', "app_career_ad.app_career_ad_save", name="app_ad_save"),
                       url(r'^app_ad/delete/$', "app_career_ad.delete_app_ad_by_career_id", name="app_ad_delete"),
                       url(r'^app_ad/check_career/$', "app_career_ad.check_is_have_the_career",
                           name="app_ad_check_career"),
                       )
