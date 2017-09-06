#!/usr/bin/env python
# -*- coding: utf8 -*-

from functools import partial

import base_sys_api
from mz_platform.utils.decorator_tool import api_except_catcher


class CommonSysApi(base_sys_api.BaseSysApi):
    """
    @brief 公用系统API接口类

    公用系统包括 Ad，Tag, Discuss, Like, SEO
    公用系统的定义：主要系统公用的的实体系统。
    外部调用形式为 [act]_[主要系统]_[公用系统]([主要系统]_id, *args， **kwargs)
    调用实现定义在service_map中，
    以公用系统为key，包含多个主要系统的字典对象，
    主要系统的字典对象以act为key，act为value
    _[公用系统] : 处理公用系统中的普遍参数
    __impl : 处理具体的映射调用关系

    @todo 实现全部first参数，支持输出单一对象
    """
    service_map_impl = None

    @property
    def service_map(self):
        if CommonSysApi.service_map_impl is None:
            _map = dict(
                tag=dict(
                    article=dict(
                        get=partial(CommonSysApi.article_service.get_related_objects, obj_type='TAG')
                    ),
                    course=dict(
                        get=CommonSysApi.course_service.get_related_tags
                    )
                ),
                ad=dict(
                    # article=dict(
                        # get=partial(CommonSysApi.career_course_service.get_related_objects, obj_type='CAREERAD', ad_type='ARTICLE', is_activate=True, order_by='-id')),
                    career_course=dict(
                        get=CommonSysApi.career_course_service.get_related_objects, obj_type='CAREERAD', is_activate=True, order_by='-id'),
                ),
                discuss=dict(
                    article=dict(get=partial(CommonSysApi.article_service.get_related_objects, obj_type='DISCUSS', order_by='-id')),
                    lesson=dict(get=partial(self.lesson_service.get_related_discuss, order_by='-id'))
                ),
                like=dict(
                    article=dict(
                        get=CommonSysApi.article_service.get_praised_users,
                        set=CommonSysApi.article_service.new_user_praise,)
                    ),
                seo=dict(
                    teacher=dict(
                        get=CommonSysApi.user_service.get_teacher_seo,
                        ),
                    course=dict(
                        get=CommonSysApi.course_service.get_course_seo,
                        ),
                    )
            )
            CommonSysApi.service_map_impl = _map
        return CommonSysApi.service_map_impl

    _api = None

    @staticmethod
    def default_instance():
        """
        @brief 默认api对象
        """
        if not CommonSysApi._api:
            CommonSysApi._api = CommonSysApi()
        return CommonSysApi._api

    @api_except_catcher
    def get_career_course_ad(self, career_course_id,
                             refer_business, first=True, **kwargs):
        """
        @brief 获取职业课程广告对象

        @param career_course_id : 职业课程id
        @param refer_business : 广告相关的业务，可选为小课程:'COURSE', 文章'ARTICLE'
        @param first : 返回一个CareerAd对象，如果first=True，默认True
        @param kwargs : 查询Ad对象的条件，多个条件是and的关系
        @retval : 符合条件的Ad对象，如果没有符合条件的对象返回[], 如果first为真，返回Ad对象
        """

        assert kwargs.get('ad_type') is None
        r = self.career_course_service.get_related_objects(
            career_course_id, obj_type='CAREERAD', ad_type=refer_business)
        if not r:
            if first:
                return None
            return []

        if first:
            r = r[0]

        return self.n_obj("CareerAd", r)

    # #######################################################
    # tag refer
    # #######################################################
    @api_except_catcher
    def get_all_article_tags(self, is_hot=False, **kwargs):
        """
        @brief 获取所有对象类型为文章的标签对象

        @param kwargs : 查询tag对象的条件，多个条件是and的关系
        @retval : 符合条件的tag对象，如果没有符合条件的对象返回[]

        @note 特殊处理
        """
        kwargs.update(dict(is_hot_tag=is_hot))
        t = self.tag_service.get_tag(conditions=self.s_p(kwargs))
        if not t:
            return []
        return self.n_obj('Tag', t)

    @api_except_catcher
    def get_article_tags(self, article_id, **kwargs):
        """
        @brief 获取某篇文章对应标签对象

        @param kwargs : 查询tag对象的条件，多个条件是and的关系
        @retval : 符合条件的tag对象，如果没有符合条件的对象返回[]
        """
        r = self._tag(article_id, 'article', 'get', **kwargs)
        return self.n_obj('Tag', r)

    @api_except_catcher
    def get_course_tags(self, course_id):
        """
        @brief 获取所有与Course相关的Tag对象

        @param course_id : course id
        @retval : 符合条件的Tag对象，如果没有符合条件的对象返回[]
        """
        ts = self._tag(course_id, 'course', 'get')
        return self.n_obj('Tag', ts)

    @api_except_catcher
    def get_tag(self, tag_id):
        tag = self.tag_service.get_tag(conditions=self.s_p(dict(id=tag_id)))
        if not tag:
            return None
        return self.n_obj('Tag', tag[0])

    # #######################################################
    # like refer
    # #######################################################
    @api_except_catcher
    def get_article_users_like(self, article_id):
        """
        @brief 获取article_id赞的用户id列表

        @param article_id : 文章id
        @retval : 符合条件的赞的文章user_id列表，如果没有符合条件的对象返回[]
        """
        r = self._like(article_id, 'article', 'get', what=('user_id',))
        return [i['user_id'] for i in r]

    @api_except_catcher
    def set_user_article_like(self, user_id, article_id, **kwargs):
        """
        @brief 获取用户赞的相关内容

        @param user_id : 用户id
        @param article_id : 文章id
        @param kwargs : 查询赞的其他条件
        @retval : 失败返回0，否则返回插入的记录的id
        """
        r = self.article_service.new_user_praise(article_id, user_id)
        return r

    # #######################################################
    # discuss refer
    # #######################################################
    def add_discuss(self, obj):
        """
        @brief 添加评论

        @param obj : 需要插入的评论对象，一个字典
        @retval : 符合条件的tag对象，如果没有符合条件的对象返回[]
        """
        return self.discuss_service.new_discuss(**obj)

    @api_except_catcher
    def get_discuss_by_lesson(self, lesson_id):
        """
        @brief 获取章节下的所有评论

        @param lesson_id : 章节ID
        @retval : 符合条件的Discuss对象,如果没有符合条件的对象返回[]
        """
        d_list = self._discuss(lesson_id, 'lesson', 'get')
        d_list = self.n_obj('Discuss', d_list)
        # pdl = [d for d in d_list if d.parent_id == 0]
        # self._compound_discuss(pdl, d_list)
        return d_list

    @api_except_catcher
    def get_discuss_by_article(self, article_id):
        """
        @brief 获取文章下的所有评论

        @param article_id : 文章ID
        @retval : 符合条件的Discuss对象,如果没有符合条件的对象返回[]
        """
        d_list = self._discuss(article_id, 'article', 'get')
        d_list = self.n_obj('Discuss', d_list)
        # pdl = [d for d in d_list if d['parent_id'] == 0]
        # self._compound_discuss(pdl, d_list)
        return d_list

    # def _compound_discuss(self, pdl, d_list):
    #     for pd in pdl:
    #         cdl = [d for d in d_list if d['parent_id'] == pd['id']]
    #         if cdl:
    #             pd['child_list'] = cdl
    #             self._compound_discuss(cdl, d_list)

    # #######################################################
    # SEO refer
    # #######################################################
    @api_except_catcher
    def get_teacher_seo(self, teacher_id):
        """
        @brief 获取teacher_id下的Seo

        @param  teacher_id teacher id
        @return     Seo object if success otherwise None
        """
        r = self._seo(teacher_id, 'teacher', 'get')
        return r[0] if r else None

    @api_except_catcher
    def get_article_seo(self, article_id):
        raise NotImplementedError()

    @api_except_catcher
    def get_course_seo(self, course_id):
        seo = self._seo(course_id, 'course', 'get')
        return seo[0] if seo else None

    @api_except_catcher
    def get_lesson_seo(self, lesson_id):
        raise NotImplementedError()
    
    # #######################################################
    # Implementation Part
    # #######################################################
    def _tag(self, pk, service, act, **kwargs):
        """
        @brief 获取符合条件的所有标签对象

        @param pk : 查询tag对象的条件, must
        @param service : service category, 'article',''
        @param kwargs : 查询tag对象的条件，多个条件是and的关系
        @retval : 符合条件的tag对象，如果没有符合条件的对象返回[]
        """
        return self.__impl(act, service, 'tag', pk, **kwargs)

    def _ad(self, pk, service, act, **kwargs):
        """
        @brief 获取符合条件的所有标签对象

        @param pk : 查询Ad对象的条件, must
        @param service : service category, 'article',''
        @param kwargs : 查询tag对象的条件，多个条件是and的关系
        @retval : 符合条件的tag对象，如果没有符合条件的对象返回[]
        """
        

        return self.__impl(act, service, 'ad', pk, **kwargs)

    def _discuss(self, pk, service, act, **kwargs):
        """
        @brief 获取符合条件的所有标签对象

        @param pk : 查询tag对象的条件, must
        @param service : service category, 'article',''
        @param kwargs : 查询tag对象的条件，多个条件是and的关系
        @retval : 符合条件的tag对象，如果没有符合条件的对象返回[]
        """
        return self.__impl(act, service, 'discuss', pk, **kwargs)

    def _like(self, pk, service, act, **kwargs):
        if pk is None:
            return self.__impl(act, service, 'like', **kwargs)
        return self.__impl(act, service, 'like', pk, **kwargs)

    def _seo(self, pk, service, act, **kwargs):
        """
        @brief 获取符合条件的Seo对象

        @param pk : 查询Seo对象的条件, must
        @param service : service category, 'article','teacher'
        @param kwargs : 查询seo对象的条件，多个条件是and的关系
        @retval : 符合条件的seo对象，如果没有符合条件的对象返回None
        """
        r = self.__impl(act, service, 'seo', pk, **kwargs)
        if act == 'get':
            r = self.n_obj('Seo', r)
        return r

    def __impl(self, act, refer, target, *args, **kwargs):
        """
        @brief      实现common api调用
        
        @param      self    The object
        @param      act     动作参数
        @param      refer   动作的对象
        @param      target  公共对象
        @param      args    主要约束条件
        @param      kwargs  次要约束条件
        
        @return     { description_of_the_return_value }
        """
        act = self.service_map[target][refer][act]
        return act(*args, **kwargs)