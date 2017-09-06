# -*- coding: utf-8 -*-

#　转介绍功能模块

__author__ = 'changfu'

import os
import datetime

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    import django
    django.setup()

from mz_user.models import UserProfile, InvitationRecord
from mz_common.views import sys_send_message

def add_invitation_record(userA_id, userB_id):
    """
    add new invitation record, this function should be called when a new user who is invited registering
    增加邀请记录，当被邀请的用户注册时，需要调用该函数
    :param userA_id: user id who send out the invitation
    :param userB_id: user id who is invited
    :return: True will return if success
    """
    assert isinstance(userA_id, long)
    assert isinstance(userB_id, long)
    if InvitationRecord.objects.filter(userB=userB_id).exists():
        return True
    record = InvitationRecord(userA=userA_id, userB=userB_id)
    record.save()
    return True

def if_user_is_invited(user_id):
    """
    用户是否被邀请加入
    :param user_id:
    :return:
    """
    assert isinstance(user_id, long)
    if InvitationRecord.objects.filter(userB=user_id).exists():
        return True
    return False

def if_first_register_course(user_id):
    """
    用户是否是第一次受邀报名职业班级
    :param user_id:
    :return:
    """
    assert isinstance(user_id, long)
    if not InvitationRecord.objects.values_list('if_attend_course', flat=True).get(userB=user_id):
        return True
    return False

def update_invitation_course_info(userb, career_course_id):
    """
    update the career course info, this function should be called when an invited user buy career course
    更新邀请记录的用户报班信息，当受邀用户报班时，需要调用该函数
    :param userB:
    :param career_course_id:
    :return:
    """
    assert isinstance(userb, long)
    assert isinstance(career_course_id, long)
    InvitationRecord.objects.filter(userB=userb).update(if_attend_course=True,
                                                        attend_course_id=career_course_id,
                                                        first_attend_time=datetime.datetime.now())
    return True

def send_message(user_id, course_name):
    """
    为邀请人记录被邀请人报名成功系统消息。
    当有被邀请人报名时，应该调用此函数
    :param user_id: 被邀请人ID
    :param course_name: 报名课程
    :return:
    """
    assert isinstance(user_id, long)
    nick_name = UserProfile.objects.values_list('nick_name', flat=True).get(id=user_id)
    user_a = UserProfile.objects.values_list('id', flat=True).get(
        id=InvitationRecord.objects.values_list('userA', flat=True).get(userB=user_id))
    msg = '恭喜您！学员%s通过您的邀请链接成功报名%s课程，享受了立减200学费的优惠！同时您将获得麦子学院的200元现金红包奖励。' \
          '稍后客服将和您取得联系，请确认您的账号绑定了手机号。您也可以主动联系客服400-8628862' % (nick_name, course_name)
    sys_send_message(0, user_a, '20', msg, action_id=user_id)

if __name__ == '__main__':
    user_id = 5
    # print set_invitation_code(user_id)
    # print get_invitation_code(user_id)
    # add_invitation_record(long(5), long(2221))
    # print if_user_is_invited(long(2221))
    # print if_first_register_course(long(2218))
    # print update_invitation_course_info(long(2218), long(107))
    # send_message(long(2219), 'python web')
    # print generate_qrcode_file('DYO8ACQB')
    # print get_qrcode_file_path('DYO8ACQB')

