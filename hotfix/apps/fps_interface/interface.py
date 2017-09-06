# -*- coding: utf-8 -*-
__author__ = 'bobby'

import urllib,urllib2
import json
from django.conf import settings

class BaseTest():
    @classmethod
    def get(self,url):

        req = urllib2.Request(url)

        response = urllib2.urlopen(req)
        res = json.loads(response.read())
        return res

    @classmethod
    def post_json(self,url,data):
        try:
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(data))
            result = json.loads(response.read())
            return result
        except Exception,e:
            return str(e)

    @classmethod
    def post_data(self,url,data):
        params = urllib.urlencode(data)
        ret = urllib.urlopen(url, params)
        code = ret.getcode()
        ret_data = ret.read()
        return ret_data

class FpsInterface(object):
    server_host = settings.FPS_API
    @classmethod
    def new_class(self,data):
        """
        新建班级通知
        :param class_id:
        :return:
        """
        url = self.server_host + "savechatgroup/"
        if settings.FPS_SWITCH:
            return BaseTest.post_json(url,data)
        else:
            return ''

    @classmethod
    def new_discuss(self,data):
        """
        新增评论通知
        :param discuess_id:
        :return:
        """
        url = self.server_host + "savediscuss/"
        if settings.FPS_SWITCH:
            return BaseTest.post_json(url,data)
        else:
            return ''

    @classmethod
    def student_join(self,data):
        """
        学生加入班级通知
        :param user_id:
        :param class_id:
        :return:
        """
        url = self.server_host + "saveclassmate/"
        if settings.FPS_SWITCH:
            return BaseTest.post_json(url,data)
        else:
            return ''

    @classmethod
    def new_user(self,data):
        """
        新用户注册
        :param user_id:
        :param class_id:
        :return:
        """
        url = self.server_host + "adduser/"
        if settings.FPS_SWITCH:
            return BaseTest.post_json(url,data)
        else:
            return ''

def pay_attention_to_classmates(class_id, student_id):
    FpsInterface.student_join({"class_id": class_id, "user_id": student_id})