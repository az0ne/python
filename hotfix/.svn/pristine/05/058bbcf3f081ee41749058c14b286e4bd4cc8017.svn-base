#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

if django.VERSION[1] > 5:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()

from utils.logger import logger as log
from tornado.options import options, define, parse_command_line

from utils.send_sms_and_message import SendSmsAndMessage
import tornado.ioloop
import tornado.web
import db.api.onevone.meeting
import datetime
from mz_lps4.interface_teacher_warning import update_teacher_backlog_is_done
import db.api.lps.teacher_warning

define('port_lps4', type=int, default=8037)


def periodic_task():
    result = db.api.onevone.meeting.get_not_ended_onevone_meeting()
    if result.is_error():
        log.warn('get_not_ended_onevone_meeting is error')

    now = datetime.datetime.now()
    for onevone_meeting in result.result():

        meeting_id = onevone_meeting.get('id', 0)
        start_time = onevone_meeting.get('start_time', now)
        end_time = onevone_meeting.get('end_time', now)
        delta_time = start_time-now

        # 更改状态为已开始
        if onevone_meeting['status'] in ['CREATE', 'DATED'] and delta_time <= datetime.timedelta(minutes=5):
            result = db.api.onevone.meeting.update_onevone_meeting(meeting_id, 'START')
            if result.is_error():
                log.warn('update_onevone_meeting is error; meeting_id:%s status:START' % meeting_id)
            # 给老师推送(app)5分钟
            try:
                _meeting5_teacher_sms_message(meeting_id, onevone_meeting['teacher_id'], start_time)
            except Exception, e:
                log.warn('_meeting5_teacher_sms_message is error; meeting_id:%s except:%s' % (meeting_id, str(e)))
            # 给学生推送(app)5分钟
            try:
                _meeting5_student_sms_message(meeting_id, onevone_meeting['user_id'], start_time)
            except Exception, e:
                log.warn('_meeting5_teacher_sms_message is error; meeting_id:%s except:%s' % (meeting_id, str(e)))

        # 更改状态为已结束
        if onevone_meeting['status'] == 'START' and now >= end_time:
            result = db.api.onevone.meeting.update_onevone_meeting(meeting_id, 'ENDED')
            if result.is_error():
                log.warn('update_onevone_meeting is error; meeting_id:%s status:ENDED' % meeting_id)
            # 约课结束时强制更新状态
            update_teacher_backlog_is_done(meeting_id, None, onevone_meeting['teacher_id'],
                                           onevone_meeting['user_id'], 5)
            continue

        # 开始前30分钟,发送短信
        if not onevone_meeting.get('is_sendsms_start30') and onevone_meeting['status'] in ['CREATE', 'DATED'] \
                and onevone_meeting.get('user_id') is not None and delta_time.total_seconds() > 0 \
                and delta_time <= datetime.timedelta(minutes=30):

            # 给老师推送(app)30分钟
            try:
                _meeting30_teacher_message(meeting_id, onevone_meeting['teacher_id'], start_time)
            except Exception, e:
                log.warn('_meeting30_teacher_message is error; meeting_id:%s except:%s' % (meeting_id, str(e)))
            # 给学生推送(app)30分钟
            try:
                _meeting30_student_message(meeting_id, onevone_meeting['user_id'], start_time)
            except Exception, e:
                log.warn('_meeting30_student_message is error; meeting_id:%s except:%s' % (meeting_id, str(e)))

            # 更新短信记录
            result = db.api.onevone.meeting.update_onevone_meeting_is_sendsms(meeting_id)
            if result.is_error():
                log.warn('update_onevone_meeting_is_sendsms is error; meeting_id:%s' % meeting_id)


def _meeting30_teacher_message(meeting_id, teacher_id, start_time):
    """
    开始前30分钟推送信息(老师)
    :param meeting_id:
    :param teacher_id:
    :param start_time:
    :return:
    """
    # 给老师推送(app)
    start_time_str = start_time.strftime('%H:%M')
    end_time = start_time+datetime.timedelta(minutes=30)
    date_str = start_time_str+'-'+end_time.strftime('%H:%M(%m/%d)')
    result = db.api.lps.teacher_warning.get_backlog_id_by_meeting_id(meeting_id)
    if result.is_error():
        log.warn('get_backlog_id_by_meeting_id is error; meeting_id:%s' % meeting_id)
    backlog_id = result.result().get('id')
    if backlog_id:
        custom = {
            "type": 5,
            "backlog_id": backlog_id
            }
        content_message = '【约课即将开始】您与学员的约课即将开始，请先阅读你需要解决的问题吧。' \
                          '直播前充分的准备能更好的解决学员的疑问，直播时间：%s。' % date_str
        try:
            SendSmsAndMessage(teacher_id, '', [], content_message, custom, SendSmsAndMessage.ONLY_MESSAGE).send()
        except Exception, e:
            log.warn('send_sms_and_message is error; except:%s' % str(e))


def _meeting30_student_message(meeting_id, user_id, start_time):
    """
    开始前30分钟推送信息(学生)
    :param meeting_id:
    :param user_id:
    :param start_time:
    :return:
    """
    # 给学生推送(app)
    start_time_str = start_time.strftime('%H:%M')
    end_time = start_time + datetime.timedelta(minutes=30)
    date_str = start_time_str + '-' + end_time.strftime('%H:%M')
    custom = {'meeting_id': meeting_id, 'type': 3}
    content_message = '【约课即将开始】你预约的直播课即将开始，请先阅读你需要解决的问题吧。' \
                      '充分的准备能更好的解决你的疑问。直播时间：%s！' % date_str
    try:
        SendSmsAndMessage(user_id=user_id, content_message=content_message, custom=custom,
                          send_type=SendSmsAndMessage.ONLY_MESSAGE).send()
    except Exception, e:
        log.warn('send_sms_and_message is error; except:%s' % str(e))


def _meeting5_teacher_sms_message(meeting_id, teacher_id, start_time):
    """
    开始前5分钟推送短信和信息(老师)
    :param meeting_id:
    :param teacher_id:
    :param start_time:
    :return:
    """
    # 给老师推送(app)
    start_time_str = start_time.strftime('%H:%M')
    end_time = start_time+datetime.timedelta(minutes=30)
    date_str = start_time_str+'-'+end_time.strftime('%H:%M(%m/%d)')
    result = db.api.lps.teacher_warning.get_backlog_id_by_meeting_id(meeting_id)
    if result.is_error():
        log.warn('get_backlog_id_by_meeting_id is error; meeting_id:%s' % meeting_id)
    backlog_id = result.result().get('id')
    if backlog_id:
        content_sms = [date_str]
        custom = {
            "type": 5,
            "backlog_id": backlog_id
            }
        content_message = '【请立刻进入您的约课】直播时间：%s，你与学员预约的直播课即将开始，立刻进入直播吧！' % date_str
        try:
            SendSmsAndMessage(teacher_id, 'teacher_meeting_open', content_sms, content_message, custom).send()
        except Exception, e:
            log.warn('send_sms_and_message is error; except:%s' % str(e))


def _meeting5_student_sms_message(meeting_id, user_id, start_time):
    """
    开始前5分钟推送短信和信息(学生)
    :param meeting_id:
    :param user_id:
    :param start_time:
    :return:
    """
    # 给学生推送(app)
    start_time_str = start_time.strftime('%H:%M')
    end_time = start_time + datetime.timedelta(minutes=30)
    date_str = start_time_str + '-' + end_time.strftime('%H:%M')
    content_sms = [date_str]
    custom = {'meeting_id': meeting_id, 'type': 3}
    content_message = '【请立刻进入你的约课】直播时间：%s！你预约的直播课即将开始，立刻进入直播吧。' % date_str
    try:
        SendSmsAndMessage(user_id=user_id, tmp_id='student_onevone_begin_in_5m', content_sms=content_sms,
                          content_message=content_message, custom=custom).send()

    except Exception, e:
        log.warn('send_sms_and_message is error; except:%s' % str(e))


def periodic_task_teacher_warning():
    # 查询所有已经超时并且未发短信的代办
    result = db.api.lps.teacher_warning.filter_warning_backlog()
    if result.is_error():
        log.warn('filter_warning_backlog is error')
    for warning_backlog in result.result():
        content_sms = []
        custom = {
            "type": warning_backlog['type'],
            "backlog_id": warning_backlog['id']
            }
        content_message = '【教学事故-待办任务】您已给学员带来不好的教学体验，请及时处理事故任务，以避免更恶劣的用户体验。'
        SendSmsAndMessage(warning_backlog['teacher_id'], 'app_teacher_waring', content_sms, content_message,
                          custom).send()
        result = db.api.lps.teacher_warning.update_teacher_warning_backlog_is_send_sms(warning_backlog['id'])
        if result.is_error():
            log.warn('update_teacher_warning_backlog_is_send_sms is error backlog_id:%s' % warning_backlog['id'])


def main():
    parse_command_line()
    tornado_app = tornado.web.Application()
    tornado_app.listen(options.port_lps4)

    tornado.ioloop.PeriodicCallback(periodic_task, 1 * 60 * 1000).start()
    tornado.ioloop.PeriodicCallback(periodic_task_teacher_warning, 1 * 60 * 1000).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
