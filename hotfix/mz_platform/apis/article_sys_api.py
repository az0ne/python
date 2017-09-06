# -*- coding: utf-8 -*-
import base_sys_api

from mz_platform.utils.decorator_tool import api_except_catcher


class ArticleSysApi(base_sys_api.BaseSysApi):
    """
    @brief 文章系统API接口类

    """

    _api = None

    @staticmethod
    def default_instance():
        """
        @brief 默认api对象
        """
        if not ArticleSysApi._api:
            ArticleSysApi._api = ArticleSysApi()
        return ArticleSysApi._api

    @api_except_catcher
    def get_one_article(self, **kwargs):
        """
        @brief 获取文章对象

        @param kwargs : 查询Article对象的条件，多个条件是and的关系
        @retval : 符合条件的Teacher对象，如果存在多个返回第一个，如果没有
        符合条件的对象，返回None
        """
        a = self.article_service.get_article(conditions=self.s_p(kwargs))
        if not a:
            return None
        return self.n_obj('Article', a[0])

    @api_except_catcher
    def get_all_article(self, **kwargs):
        """
        @brief 获取文章对象

        @param kwargs : 查询Article对象的条件，多个条件是and的关系
        @retval : 符合条件的Article对象，如果没有符合条件的对象返回[]
        """
        # if 'article_type_id' in kwargs \
        #         and not kwargs.get('article_type_id', None):
        #     at = self.get_first_article_type()
        #     if at:
        #         kwargs['article_type_id'] = at.id
        #     else:
        #         del kwargs['article_type_id']
        a = self.article_service.get_article(conditions=self.s_p(kwargs))
        if not a:
            return []
        return self.n_obj('Article', a)

    @api_except_catcher
    def get_first_article_type(self, **kwargs):
        """
        @brief 获取第一个文章分类对象

        @param kwargs : 查询ArticleType对象的条件，多个条件是and的关系
        @retval : 符合条件的ArticleType对象，如果没有符合条件的对象返回[]
        """
        at = self.article_type_service.get_article_type(conditions=self.s_p(kwargs))
        # at = self.article_service.get_article(conditions=self.s_p(kwargs))
        if not at:
            return None
        return self.n_obj('ArticleType', at[0])

    @api_except_catcher
    def get_all_article_type(self, is_homepage=None, **kwargs):
        """
        @brief 获取文章分类对象

        @param is_homepage : 是否显示在首页，none不区分， 0，选择非homepage的， 1选择homepage的
        @param kwargs : 查询ArticleType对象的条件，多个条件是and的关系
        @retval : 符合条件的ArticleType对象，如果没有符合条件的对象返回[]
        """
        if is_homepage is not None:
            is_homepage = 1 if is_homepage else 0
            kwargs.update(is_homepage=is_homepage)
        at = self.article_type_service.get_article_type(
            conditions=self.s_p(kwargs))
        if not at:
            return []
        return self.n_obj('ArticleType', at)

    @api_except_catcher
    def get_related_articles(self, career_id, **kwargs):
        """
        @brief      获取article_id相关的其他文章

        @param  career_id  职业课程id

        @return     返回[Article] 如果失败返回[]
        """
        # r = self.article_service.get_related_objects(
        #     article_id, obj_type='CAREER')
        # if r:
        #     r = r[0]
        # else:
        #     return []
        # self._deb_print(r=r)
        r = self.career_course_service.get_related_objects(
            career_id, obj_type='ARTICLE', limit='5')
        return self.n_obj('Article', r)

    @api_except_catcher
    def get_related_careercourse(self, article_id, first=True, **kwargs):
        """
        @brief      获取article_id相关的

        @param  article_id  相关文章依赖的文章id

        @return     返回[CareerCourse] 如果失败返回[],
                    如果first为True返回CareerCourse对象
                    如果失败返回None
        """
        r = self.article_service.get_related_objects(
            article_id, obj_type='CAREER', otr_type='ARTICLE', is_active=False)
        if first:
            if r:
                r = r[0]
            else:
                return None
        return self.n_obj('CareerCourse', r)
