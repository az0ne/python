# -*- coding: utf-8 -*-
import base64
import json
import urllib

import requests
from django.conf import settings

from utils.logger import logger as log
from utils.sms_manager import send_sms_new

import db.api.common.app
import db.api.lps.teacher_warning
import db.api.user.user
import db.api.common.new_discuss_post
from utils.tool import strip_tags


class UserObj(object):
    def __init__(self, user_id):
        self.user_id = user_id
        u = db.api.user.user.get_user_by_id(user_id)
        if u.is_error():
            log.warn("get_user_by_id failed. "
                     "user_id: {}".format(user_id))
            raise Exception("get user error.")
        self.user = u.result()

    def is_teacher(self):
        r = db.api.common.new_discuss_post.is_teacher(self.user_id)
        if r.is_error():
            log.warn("is_teacher failed. user_id: {}"
                     .format(self.user_id))
            return False
        return bool(r.result())

    def __getattr__(self, item):
        if item == "id":
            return self.user_id
        return self.user[item]


class SendSmsAndMessage(object):
    """
    有新的代办后发送APP 或短信
    :param user_id: 用户ID
    :param tmp_id: 短信模板
    :param content_sms: 短信参数
    :param content_message: 消息内容
    :param custom: 定在参数（在APP或短信中点击）
    :param send_type: 1:只发短信;2:只发推送;3:都发
    :return:
    """
    ONLY_SMS = 1
    ONLY_MESSAGE = 2
    BOTH_SMS_AND_MESSAGE = 3

    def __init__(self, user_id, tmp_id='', content_sms=None, content_message=None, custom=None,
                 send_type=BOTH_SMS_AND_MESSAGE):
        self.user_id = user_id
        self.tmp_id = tmp_id
        self.content_sms = content_sms
        self.content_message = content_message
        self.custom = custom
        self.send_type = send_type

    def send(self):
        try:
            user = UserObj(self.user_id)
        except Exception as e:
            log.warn('UserProfile user_id is not')
            raise Exception(str(e))

        # 判断是否是老师
        if user.is_teacher():
            xinge_type = 'xinge_tech'
            _url = 'maiziteacher://maiziedu.com/app?'
            result = db.api.common.app.app_get_user_token(self.user_id)
            if result.is_error():
                log.warn('app_get_user_token is error user_id:%s' % self.user_id)
            user_token = result.result()
        else:
            xinge_type = 'xinge_stu'
            _url = 'maizistudent://maiziedu.com/app?'
            if user.token:
                if len(user.token) == 64:  # ios
                    user_token = dict(token=user.token, type=2)
                else:
                    user_token = dict(token=user.token, type=1)
            else:
                user_token = None
        if self.send_type != self.ONLY_MESSAGE:
            # 链接参数编码
            if self.custom:
                self.content_sms.append(_url + base64.b32encode(urllib.urlencode(self.custom)))
            send_sms_new(user.mobile, self.tmp_id, self.content_sms)
            log.info('send  sms success mobile:%s tmp_id:%s' % (user.mobile, self.tmp_id))
            if self.send_type == self.ONLY_SMS:
                return True

        if not user_token:
            return True
        if hasattr(settings, 'IS_SEND_MESSAGE') and settings.IS_SEND_MESSAGE:
            result = db.api.lps.teacher_warning.get_new_backlog_count_by_teacher_id(self.user_id)
            if result.is_error():
                log.warn('get_new_backlog_count_by_user_id is error user_id:%s' % self.user_id)
                message_count = 1
            else:
                message_count = int(result.result()) if result.result() else 1
            try:
                content_message = strip_tags(self.content_message)
                token = user_token['token']
                if user_token['type'] == 2:
                    # ios通知
                    requests.post(settings.SEND_SMS_URL + "push/", data=json.dumps({
                        "sender": xinge_type,
                        "args": {
                            "msg": content_message,
                            "token": token,
                            "device_type": "ios",
                            "message_type": 1,
                            "expire": 3600,
                            "badge": message_count,
                            "send_type": 1,
                            "custom": self.custom,
                            "user_id": user.id,
                            "user_name": user.nick_name
                        }
                    }), timeout=2)
                    log.info('send msg ios success user_id:%s token:%s' % (user.id, token))

                if user_token['type'] == 1:
                    # android 通知
                    requests.post(settings.SEND_SMS_URL + "push/", data=json.dumps({
                        "sender": xinge_type,
                        "args": {
                            "title": "麦子学院",
                            "msg": content_message,
                            "token": token,
                            "device_type": "android",
                            "message_type": 1,
                            "expire": 3600,
                            "badge": message_count,
                            "send_type": 1,
                            "custom": self.custom,
                            "user_id": user.id,
                            "user_name": user.nick_name
                        }
                    }), timeout=2)
                    log.info('send msg android success user_id:%s token:%s' % (user.id, token))
            except Exception, e:
                log.warn("send_xinge failed. details: %s" % str(e))
                raise Exception(str(e))
        return True
    

