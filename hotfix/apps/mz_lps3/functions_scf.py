# -*- coding: utf-8 -*-

"""
this file contains functions that writes global msg / task project score msg into mymessage
"""

__author__ = 'changfu'

import logging
import time
import json
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from mz_common.views import sys_send_message
from core.common.cache.util import CachedFixedQueue
logger = logging.getLogger('mz_lps3.functions_scf')

class CustomJsonEncode(json.JSONEncoder):
    """
    自定义序列化 ImageFiled 字段的类
    """
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            try:
                return str(obj)
            except ValueError, e:
                return ''
        return json.JSONEncoder.default(self, obj)

class ClassDyMsgQueue(object):
    """
    """
    max_length = 30
    key_prex = 'Class:DyMsg'

    @classmethod
    def get(cls, class_id):
        queue = CachedFixedQueue(key='%s:%s' % (cls.key_prex, class_id), max_len=cls.max_length)
        ret = queue.get()
        return list(json.loads(x) for x in ret)[::-1]

    @classmethod
    def push(cls, class_id, item):
        item = json.dumps(item, cls=CustomJsonEncode)
        queue = CachedFixedQueue(key='%s:%s' % (cls.key_prex, class_id), max_len=cls.max_length)
        queue.push(item)

    @classmethod
    def format_message(cls, message):
        """
        格式化班级消息,主要工作是:
        1.  为消息增加时戳
        2.  处理头像的链接
        3.  格式化时间显示
        :param message: 一挑班级动态格式为:
                        {
                            'user_id': user_id,
                            'nick_name': nick_name,
                            'avatar_url': avatar_url,
                            'message':  message,
                            'time': datatime instance
                        }
        :return:
        """
        assert isinstance(message, dict)
        timestampe = ('timestampe', time.mktime(message['time'].timetuple()))   # 由消息产生的时间生成时戳
        message['url'] = '%s%s' % (settings.FPS_CENTER, message['user_id'])    # 生成头像链接
        message['time'] = message['time'].strftime('%H:%M')    # 调整时间的显示格式
        return dict([timestampe, ] + message.items())

def write_class_rank_change_message(user_id, class_id, rank_change):
    """
    write class rank change to my message
    :param user_id:
    :param class_id:
    :param rank_change: should be an int number, for example, -3 means rank down 3
    :return:
    """
    try:
        if rank_change > 0:
            msg = '恭喜你！你的班级排名上升%s名！真厉害，继续加油吧！' % str(rank_change)
        elif rank_change < 0:
            msg = '哎呀，你的排名已经被同班%s名同学超过啦。别灰心！赶紧加油学习赶上吧！' % str(-rank_change)
        else:  # if rank_change equal 0, will not record message.
            return True
        return sys_send_message(A_id=0, B_id=user_id, action_type=10, content=msg, action_id=class_id)
    except Exception as msg:
        logger.error(msg)

def write_task_project_score_message(user_id, user_task_record_id):
    """
    write task project score into mymessage
    :param user_id:
    :param user_task_record_id: id of user task record id.
    :return:
    TODO: Construct the content by QinXuan.
    """
    try:
        content = ''  # construct content here
        return sys_send_message(A_id=0, B_id=user_id, action_type=11, content=content, action_id=user_task_record_id)
    except Exception as msg:
        logger.error(msg)

def write_class_meeting_open_message(user_id, class_meeting_id):
    """
    将班会开始的信息写入Mymessage
    :param user_id:
    :param class_meeting_id: 班会ID.
    :return:
    TODO: Construct the content by Guotao.
    """
    try:
        content = ''  # construct content here
        return sys_send_message(A_id=0, B_id=user_id, action_type=12, content=content, action_id=class_meeting_id)
    except Exception as msg:
        logger.error(msg)

def write_absent_user_message(user_id, class_meeting_id):
    """
    将班会缺勤的信息写入Mymessage
    :param user_id:
    :param class_meeting_id: 班会ID.
    :return:
    TODO: Construct the content by Guotao.
    """
    try:
        content = ''  # construct content here
        return sys_send_message(A_id=0, B_id=user_id, action_type=13, content=content, action_id=class_meeting_id)
    except Exception as msg:
        logger.error(msg)





