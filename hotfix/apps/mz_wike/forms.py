# -*- coding: utf-8 -*-

from django import forms

import db.api

class WikeAskForm(forms.Form):
    """
    微课问答form
    """
    error_messages = {'openid_length_error': u'用户ID错误'}

    openid = forms.CharField()

    def clean_openid(self):
        """
        @brief 验证openid是否严格等于微信用户的openid的长度
        :return:
        @note 错误信息不明确,故意为之
        """
        openid = self.cleaned_data.get('openid')
        if not len(openid) == 28:
            raise forms.ValidationError(self.error_messages['openid_length_error'], code='openid_length_error')
        return openid

class LikeWikeAskForm(WikeAskForm):
    """微课问答点赞form
    注意: 此处并未做重复点赞的验证. 之所以如此,是出于以下考虑:
          1. 对于每次点赞,可以节省一次数据访问;
          2. 正常情况下,前端可以保证,点赞之后,无法再次点赞;
          3. 异常情况下,比如用户用脚本点赞, 则只返回粗略的错误信息,该信息同时带有误导性质, 误导对手脚本;
    """
    wike_ask_id = forms.IntegerField()

    def do_like(self):
        wike_ask_id = self.cleaned_data.get('wike_ask_id')
        openid = self.cleaned_data.get('openid')
        result = db.api.wike.wike.add_wike_ask_like(openid, wike_ask_id)
        return result

    def get_like_num(self):
        wike_ask_id = self.cleaned_data.get('wike_ask_id')
        result = db.api.wike.wike.get_wike_ask_like_count(wike_ask_id)
        return result

class MicroCourseAskForm(WikeAskForm):
    """
    微课问答的Form
    """
    micro_course_id = forms.IntegerField()
    nick_name = forms.CharField(required=False)
    head_image = forms.URLField(required=False)
    content = forms.CharField()
    ask_time = forms.DateTimeField()

    def save(self, is_commit=True):
        if is_commit:
            result = db.api.wike.wike.add_wike_ask(self.cleaned_data.get('micro_course_id'),
                                                   self.cleaned_data.get('openid'),
                                                   self.cleaned_data.get('nick_name'),
                                                   self.cleaned_data.get('head_image'),
                                                   self.cleaned_data.get('content'),
                                                   self.cleaned_data.get('ask_time'))
            return result
        return self.cleaned_data
