# -*- coding: utf-8 -*-
"""
@version: 2016/5/23 0023
@author: lewis
@contact: lewis@maiziedu.com
@file: interface.py
@time: 2016/5/23 0023 10:31
@note:  ??
"""
from django.conf import settings

import db.api.common.new_discuss
import db.api.usercenter.message
import db.api.lps.student
import db.api.user.user
from utils.logger import logger as log
from django.core.urlresolvers import reverse
from mz_lps.models import ClassStudents, Class

def is_joinclass_valid(user_id, class_id):
    """
    验证是否加入指定班级
    :param user_id: 用户ID
    :param class_id: 班级ID
    :return bool
    """
    if ClassStudents.objects.filter(status=ClassStudents.STATUS_NORMAL, user_id=user_id,
                                    student_class__class_type=Class.CLASS_TYPE_NORMAL,
                                    student_class_id=class_id).exists():
        return True
    return False


def is_join_job_class_valid(user_id):
    """
    验证用户是否加入了4.0的就业班级
    :param user_id:
    :return:
    """
    flags = db.api.lps.student.is_join_lps4_job_class(user_id).result()
    if flags:
        return True
    else:
        return False


def get_discuss_count(user_id):
    """
    获取问答的未读数
    :param user_id:
    :return:
    """
    return db.api.common.new_discuss.get_user_status_count(user_id).result()


def gen_avatar_html(user_id):
    user = db.api.user.user.get_user_by_id(user_id).result()
    if user:
        avatar_html = '<img class="avatar" src="{}">'.format(
            settings.MEDIA_URL+user['avatar_small_thumbnall'])
    else:
        avatar_html = ''

    return avatar_html


def create_discuss_my_message(userB, userA_name, content, action_type, action_id, problem_id, user_id):
    """
    创建和讨论相关my_message
    :param userA_name: 发起user_name(str)
    :param userB: 目标user—ID (int)
    :param content: 内容(str)
    :param action_type: 类型(str)
    :param action_id: 相关ID(int)
    :param problem_id: 问题ID(int)
    :param user_id: 提问者的用户ID(int)
    :return:
    """
    kwargs = dict()
    kwargs['userA'] = 0
    kwargs['userB'] = int(userB)
    kwargs['action_id'] = int(action_id)
    kwargs['action_type'] = action_type
    try:
        # 问答：提问被回复
        if action_type == '21':
            url_str = reverse('home:student:my_discuss')+'?p_id=%s' % problem_id
            message_content = """‘%s‘回复了你在‘%s’下的提问，<a href="%s">赶快去看看吧！</a>""" % \
                              (userA_name, content, url_str)
        # 问答：回复被回复
        if action_type == '22':
            url_str = reverse('u:public_discuss', args=[user_id])+'?p_id=%s' % problem_id
            message_content = """你在‘%s’下参与的回答有了新的回复，<a href="%s">赶快去看看吧！</a>""" % \
                              (content, url_str)
        # 问答：有新的提问
        if action_type == '23':
            avatar_html = gen_avatar_html(user_id)

            url_str = reverse('home:teacher:student_discuss')+'?p_id=%s' % problem_id
            message_content = """‘%s‘在‘%s’下提出了新的疑问，非常需要您的专业解答<a href="%s">赶快去看看吧！</a>""" % \
                              (userA_name, content, url_str)

            message_content = avatar_html + '<p>{}</p>'.format(message_content)
    except Exception, e:
        log.warn(e)

    kwargs['action_content'] = message_content
    result = db.api.usercenter.message.create_my_message(**kwargs)
    if not result.result() == True:
        log.warn('create_discuss_my_message fail! content=%s; action_type=%s' % (content, action_type))
