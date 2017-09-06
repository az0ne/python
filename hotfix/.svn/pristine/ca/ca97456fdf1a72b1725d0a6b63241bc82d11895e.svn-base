#!/usr/bin/env python
# -*- coding: utf8 -*-
from mz_platform.apis.course_sys_api import CourseSysApi
from mz_platform.apis.user_sys_api import UserSysApi
from mz_platform.objects.sql_result_wrapper import SqlResultWrapper


class Discuss(SqlResultWrapper):
    """
    @brief Discuss对象

    支持以下属性

    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('LESSON', '视频'),
    )
    object_id = models.IntegerField(u'对象ID', default=0, db_index=True)
    object_type = models.CharField(u'对象类型', choices=TYPE_CHOICES, default='ARTICLE', max_length=20)
    comment = models.TextField(u'评论', blank=True, null=True)
    user_id = models.IntegerField(u'用户ID', db_index=True)
    nick_name = models.CharField(u'昵称', max_length=50, blank=True, null=True)
    head = models.CharField(u'头像', max_length=200, blank=True, null=True)
    create_date = models.DateTimeField(u'创建时间', auto_now_add=True)
    parent_id = models.IntegerField(u'父级评论_id', default=0, db_index=True)
    """
    ARTICLE = 'ARTICLE'
    LESSON = 'LESSON'

    @property
    def user(self):
        if not self._user:
            api = UserSysApi.default_instance()
            r = api.get_one_user(pk=self['user_id'])
            if not r:
                return None
            self._user = r.obj
        return self._user

    # @property
    # def obj(self):
    #     if not self._obj:
    #         if self['object_type'] == 'LESSON':
    #             api = CourseSysApi.default_instance()
    #             r = api.get_one_lesson(pk=self['object_id'])
    #             if not r:
    #                 return None
    #             self._obj = r.obj
    #     return self._obj
