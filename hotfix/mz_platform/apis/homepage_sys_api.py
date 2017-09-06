#!/usr/bin/env python
# -*- coding: utf8 -*-
import base_sys_api
from mz_platform.utils.decorator_tool import api_except_catcher
from mz_platform.services.functions.home_page_service import HomePageService

"""
HomepageSysApi Api Collection


"""


class HomepageSysApi(base_sys_api.BaseSysApi):

    _api = None
    _home_page_service = HomePageService()

    @staticmethod
    def default_instance():
        """
        @brief 默认api对象
        """
        if not HomepageSysApi._api:
            HomepageSysApi._api = HomepageSysApi()
        return HomepageSysApi._api

    @api_except_catcher
    def get_homepage_all_hot_course(self):
        """
        @brief      主页推荐热门课程

        @return     [(CareerCategory， [Course])].
        """
        r = self.career_category_service.get_all_career_category()
        if len(r) > 4:
            r = r[:4]
        r = self.n_obj('CareerCategory', r)

        def _worker(cc):
            cs = self.career_category_service\
                .get_distinct_related_course(cc.id, limit=8)
            cs = self.n_obj('Course', cs)
            return cc, cs
        return [_worker(i) for i in r]

    @api_except_catcher
    def get_home_page_article(self):
        """
        @brief      主页推荐热门文章

        @return     [(ArticleType， [Article])].
        """

        at = self.article_type_service.get_article_type(
            conditions=self.s_p(dict(is_homepage=1)))
        at = self.n_obj('ArticleType', at)

        def _worker(atobj):
            r = HomepageSysApi._home_page_service.get_home_page_article(atobj.id)
            r = self.n_obj('Article', r)
            return (atobj, r)
        return [_worker(i) for i in at]
