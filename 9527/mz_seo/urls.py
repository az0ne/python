#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns("mz_seo",
                       url(r'^objSEO/list/$', "objSEO.obj_seo_list", name="obj_seo_list"),
                       url(r'^objSEO/edit/$', "objSEO.obj_seo_edit", name="obj_seo_edit"),
                       url(r'^objSEO/save/$', "objSEO.obj_seo_save", name="obj_seo_save"),
                       #
                       url(r'^tb_homepage_link/list/$', "homepagelink.homepage_link", name="homepagelink"),
                       url(r'^tb_homepage_link/edit/$', "homepagelink.homepage_link_edit", name="homepageedit"),
                       url(r'^tb_homepage_link/save/', "homepagelink.homepage_link_save", name="homepagesave"),
                       #
                       url(r'^mz_career_link/list/$', "careerlink.career_link", name="careerlink"),
                       url(r'^mz_career_link/edit/$', "careerlink.career_link_edit", name="careeredit"),
                       url(r'^mz_career_link/save/', "careerlink.career_link_save", name="careersave"),
                       #
                       url(r'^mz_wiki_link/list/$', "wikilink.wiki_link", name="wikilink"),
                       url(r'^mz_wiki_link/edit/$', "wikilink.wiki_link_edit", name="wikiedit"),
                       url(r'^mz_wiki_link/save/$', "wikilink.wiki_link_save", name="wikisave"),
                       #
                       url(r'^mz_career_linkthr/list/$', "careerlinkthr.career_link", name="careerlinkthr"),
                       url(r'^mz_career_linkthr/edit/$', "careerlinkthr.career_link_edit", name="careereditthr"),
                       url(r'^mz_career_linkthr/save/$', "careerlinkthr.career_link_save", name="careersavethr"),
                       )
