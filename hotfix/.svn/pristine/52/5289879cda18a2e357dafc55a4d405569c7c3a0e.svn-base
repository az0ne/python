#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.objects.sql_result_wrapper import SqlResultWrapper
from mz_platform.apis.article_sys_api import ArticleSysApi
from mz_platform.apis.common_sys_api import CommonSysApi


class Article(SqlResultWrapper):
    """
    @brief Article对象

    支持以下属性

    title = models.CharField(u'文章标题', max_length=200)
    content = models.TextField(u'内容')
    is_actived = models.BooleanField(u'是否生效', default=True)
    abstract = models.CharField(u'内容', max_length=200)
    title_image = models.CharField(u'文章配图', max_length=200)
    user_id = models.IntegerField(u'发表用户ID')
    nick_name = models.CharField(u'昵称', max_length=50)
    user_head = models.CharField(u'用户头像', max_length=200)
    replay_count = models.IntegerField(u'回复数量')
    praise_count = models.IntegerField(u'点赞数量')
    publish_date = models.DateTimeField(u'发布日期')
    article_type_id = models.IntegerField(u'类型', db_index=True)

    name -> 文章关联的职业课程的名字
    """

    @property
    def article_type(self):
        if self._article_type is None:
            api = ArticleSysApi.default_instance()
            r = api.get_first_article_type(id=self.article_type_id)
            if not r:
                return None
            self._article_type = r.obj
        return self._article_type

    @property
    def tags(self):
        if self._tags is None:
            api = CommonSysApi.default_instance()
            r = api.get_article_tags(self.id)
            if not r:
                return []
            self._tags = r.obj
        return self._tags

    @property
    def hot_tags(self):
        if self._hot_tags is None:
            result = [i for i in self.tags if i.is_hot_tag]
            if result:
                self._hot_tags = result
            else:
                return []
        return self._hot_tags

    @property
    def html_publish_date(self):
        return self._html_publish_date_impl(self.publish_date)

    @property
    def relate_career_name(self):
        return self.name
