#!/usr/bin/env python
# -*- coding: utf8 -*-
from django import forms

from mz_platform.apis.article_sys_api import ArticleSysApi
from mz_platform.apis.common_sys_api import CommonSysApi
from mz_platform.utils.view_shortcuts import opt_apiresult_obj


class BaseDiscussForm(forms.Form):
    ARTICLE = 'ARTICLE'
    LESSON = 'LESSON'
    TYPE_CHOICES = {ARTICLE: u'文章', LESSON: u'视频'}
    common_api = CommonSysApi.default_instance()


class DiscussForm(BaseDiscussForm):
    """评论form"""
    object_id = forms.IntegerField()
    object_type = forms.ChoiceField(
        choices=BaseDiscussForm.TYPE_CHOICES.items())
    comment = forms.CharField()
    user_id = forms.IntegerField()
    nick_name = forms.CharField()
    head = forms.CharField()
    create_date = forms.DateTimeField()
    parent_id = forms.IntegerField()

    def save(self, is_commit=True):
        if is_commit:
            return dict(id=self.common_api.add_discuss(self.cleaned_data),
                        parent_id=self.cleaned_data.get('parent_id'))
        return self.cleaned_data


class GetDiscussForm(BaseDiscussForm):
    """获取评论form"""
    object_id = forms.IntegerField()
    object_type = forms.ChoiceField(
        choices=BaseDiscussForm.TYPE_CHOICES.items())

    def get_discuss(self):
        object_id = self.cleaned_data.get('object_id')
        object_type = self.cleaned_data.get('object_type')
        if object_type == DiscussForm.ARTICLE:
            discuss = opt_apiresult_obj(
                [], self.common_api.get_discuss_by_article, object_id)
        else:
            discuss = opt_apiresult_obj(
                [], self.common_api.get_discuss_by_lesson, object_id)
        return discuss


class LikeArticleForm(forms.Form):
    """给文章点赞form"""
    error_messages = {'repeatedly': u'重复点赞'}

    article_id = forms.IntegerField()
    user_id = forms.IntegerField()

    common_api = CommonSysApi.default_instance()
    article_api = ArticleSysApi.default_instance()

    def clean(self):
        if self.check_repeat_like():
            raise forms.ValidationError(
                self.error_messages['repeatedly'],
                code='repeatedly'
            )

    def do_like(self):
        article_id = self.cleaned_data.get('article_id')
        user_id = self.cleaned_data.get('user_id')
        return self.common_api.set_user_article_like(user_id, article_id).obj

    def get_like_num(self):
        article_id = self.cleaned_data.get('article_id')
        article = self.article_api.get_one_article(pk=article_id).obj
        return article.praise_count

    # 检查重复点赞
    def check_repeat_like(self):
        article_id = self.cleaned_data.get('article_id')
        user_id = self.cleaned_data.get('user_id')
        like_list = self.common_api.get_article_users_like(article_id).obj
        return user_id in like_list if like_list else False
