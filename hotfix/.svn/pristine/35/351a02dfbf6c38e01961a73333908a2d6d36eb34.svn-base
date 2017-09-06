# -*- coding: utf-8 -*
import datetime
import db.api.common.app
from utils.logger import logger as log
import db.api.lps.teacher_warning
import db.api.onevone.study_service
import db.api.onevone.meeting
from utils.send_sms_and_message import SendSmsAndMessage


def add_join_learning_teacher_backlog(user, teacher_id, career_id, content, coach_id, coach_comment_id,
                                      send_type=SendSmsAndMessage.ONLY_MESSAGE):
    """
    入学沟通提醒
    :param user:
    :param teacher_id:
    :param career_id:
    :param content:
    :param coach_id:
    :param coach_comment_id:
    :param send_type:
    :return:
    """
    tmp_id = 'app_join_class_service'
    if send_type == SendSmsAndMessage.BOTH_SMS_AND_MESSAGE:
        content_message = '【入学沟通-待办任务】您有一名新的学员成功入学,请在%s之前向学员发出入学建议'
    else:
        content_message = '【入学沟通-待办任务】有学员在入学时遇到了问题,请在%s之前向学员发出入学建议'
    backlog_type = 11
    obj_id = coach_id
    obj_child_id = coach_comment_id
    try:
        _create_backlog(user, teacher_id, career_id, content, tmp_id, content_message, backlog_type,
                        obj_id, obj_child_id=obj_child_id, send_type=send_type)
    except Exception, e:
        log.warn('add_teacher_backlog user_id:%s teacher_id:%s career_id:%s obj_id:%s msg:%s' %
                 (user.id, teacher_id, career_id, obj_id, str(e)))


def add_student_q_a_teacher_backlog(user, teacher_id, career_id, content, coach_id, coach_comment_id):
    """
    学员问答提醒
    :param user:
    :param teacher_id:
    :param career_id:
    :param content:
    :param coach_id:
    :param coach_comment_id:
    :return:
    """
    tmp_id = ''
    content_message = '【学员提问-待办任务】有学员在学习时遇到了问题，请在%s前帮助学生解决问题'
    backlog_type = 12
    obj_id = coach_id
    obj_child_id = coach_comment_id
    try:
        _create_backlog(user, teacher_id, career_id, content, tmp_id, content_message, backlog_type,
                        obj_id, obj_child_id=obj_child_id, send_type=SendSmsAndMessage.ONLY_MESSAGE)
    except Exception, e:
        log.warn('add_teacher_backlog user_id:%s teacher_id:%s career_id:%s obj_id:%s msg:%s' %
                 (user.id, teacher_id, career_id, obj_id, str(e)))


def add_coach_info_teacher_backlog(user, teacher_id, career_id, content, coach_id, coach_comment_id):
    """
    辅导信息提醒
    :param user:
    :param teacher_id:
    :param career_id:
    :param content:
    :param coach_id:
    :param coach_comment_id:
    :return:
    """
    tmp_id = ''
    content_message = '【辅导信息-待办任务】有学员在学习时遇到了问题，请在%s前帮助学生解决问题'
    backlog_type = 13
    obj_id = coach_id
    obj_child_id = coach_comment_id
    try:
        _create_backlog(user, teacher_id, career_id, content, tmp_id, content_message, backlog_type,
                        obj_id, obj_child_id=obj_child_id, send_type=SendSmsAndMessage.ONLY_MESSAGE)
    except Exception, e:
        log.warn('add_teacher_backlog user_id:%s teacher_id:%s career_id:%s obj_id:%s msg:%s' %
                 (user.id, teacher_id, career_id, obj_id, str(e)))


def add_project_coach_teacher_backlog(user, teacher_id, career_id, content, coach_id, coach_comment_id,
                                      send_type=SendSmsAndMessage.ONLY_MESSAGE):
    """
    项目辅导提醒
    :param user:
    :param teacher_id:
    :param career_id:
    :param content:
    :param coach_id:
    :param coach_comment_id:
    :param send_type:
    :return:
    """
    tmp_id = 'app_teacher_project'
    content_message = '【项目辅导-待办任务】您有一条来自学员项目制作的信息，请在%s前处理'
    backlog_type = 14
    obj_id = coach_id
    obj_child_id = coach_comment_id
    try:
        _create_backlog(user, teacher_id, career_id, content, tmp_id, content_message, backlog_type,
                        obj_id, obj_child_id=obj_child_id, send_type=send_type)
    except Exception, e:
        log.warn('add_teacher_backlog user_id:%s teacher_id:%s career_id:%s obj_id:%s msg:%s' %
                 (user.id, teacher_id, career_id, obj_id, str(e)))


def add_meeting_teacher_backlog(user, teacher_id, career_id, content, coach_id):
    """
    加入待办
    :param user:
    :param teacher_id:
    :param career_id:
    :param content:
    :param coach_id:
    :return:
    """
    tmp_id = 'teacher_meeting'
    content_message = '【新的约课-待办任务】您的新的约课，直播时间：%s，请做好直播准备并准时参加。' \
                      '如需调整请及时与学员沟通取消以避免教学事故。'
    backlog_type = 5
    obj_id = coach_id
    try:
        _create_backlog(user, teacher_id, career_id, content, tmp_id, content_message, backlog_type,
                        obj_id, send_type=SendSmsAndMessage.BOTH_SMS_AND_MESSAGE)
    except Exception, e:
        log.warn('add_teacher_backlog user_id:%s teacher_id:%s career_id:%s obj_id:%s msg:%s' %
                 (user.id, teacher_id, career_id, obj_id, str(e)))
        raise Exception(u'加入待办出错')


def _create_backlog(user, teacher_id, career_id, content, tmp_id, content_message, backlog_type,
                    obj_id, obj_child_id=None, send_type=SendSmsAndMessage.ONLY_MESSAGE):
    """
    创建告警代办的子函数
    :param user:
    :param teacher_id:
    :param career_id:
    :param content:
    :param tmp_id:
    :param content_message:
    :param backlog_type:
    :param obj_id:
    :param obj_child_id:
    :param send_type:
    :return:
    """
    if backlog_type == 5:  # 约课
        # 获取1v1输入对象
        result = db.api.onevone.meeting.get_onevone_meeting_by_id(obj_id)
        if result.is_error():
            log.warn('get_onevone_meeting_by_id is error ovo_meeting_id:%s' % obj_id)
        ovo_meeting = result.result()
        if not ovo_meeting:
            return False
        start_time = ovo_meeting['start_time']
        warn_one_date, warn_two_date = start_time - datetime.timedelta(minutes=5), start_time + datetime.timedelta(
            minutes=5)
        warn_three_date = None
    else:
        warn_one_date, warn_two_date, warn_three_date = get_warn_times(backlog_type)
    kwargs = dict(
        user_id=user.id,
        user_name=user.real_name or user.nick_name,
        user_head=user.avatar_small_thumbnall,
        teacher_id=teacher_id,
        content=content,
        type=backlog_type,
        obj_id=obj_id,
        obj_child_id=obj_child_id,
        warn_one_date=warn_one_date,
        warn_two_date=warn_two_date,
        warn_three_date=warn_three_date,
        career_id=career_id
    )
    result = db.api.lps.teacher_warning.create_teacher_warning_backlog(**kwargs)
    if result.is_error():
        log.warn('create_teacher_warning_backlog is error type:%s obj_id:%s' % (backlog_type, obj_id))
        return False
    # 发信息
    if result.result():
        try:
            if backlog_type == 5:  # 约课
                start_time_str = start_time.strftime('%H:%M')
                end_time = start_time+datetime.timedelta(minutes=30)
                date_str = start_time_str+'——'+end_time.strftime('%H:%M(%m-%d)')
            else:
                date_str = warn_three_date.strftime('%H:%M(%m-%d)')
            backlog_id = result.result()

            if backlog_type == 11:
                content_sms = [user.real_name or user.nick_name, date_str, user.mobile, user.qq, user.wechat]
            else:
                content_sms = [date_str]
            custom = {
                "type": backlog_type,
                "backlog_id": int(backlog_id),
                "coach_id": obj_id
                }
            content_message = content_message % date_str
            SendSmsAndMessage(teacher_id, tmp_id, content_sms, content_message, custom, send_type).send()
        except Exception as e:
            log.warn('send sms or message error: %s' % str(e))
    return result.result()


def update_teacher_backlog_is_done(obj_id, teacher_child_id, teacher_id, user_id, type):
    """
    更新老师告警待办项为已经完成
    :param obj_id:
    :param teacher_child_id:
    :param teacher_id:
    :param user_id:
    :param type:
    :return:
    """

    result = db.api.lps.teacher_warning.update_teacher_warning_backlog_is_done(obj_id, teacher_child_id,
                                                                           teacher_id, user_id, type)
    if result.is_error():
        log.warn('update_teacher_warning_backlog_is_done is error type:%s obj_id:%s teacher_id:%s user_id:%s'%
                 (type, obj_id, teacher_id, user_id))
        return False

    # 老师回复后需要给学生推送;1：辅导2:项目3:约课
    if type in [11, 12, 13]:
        custom = {'coach_id': obj_id, 'type': 1}
    elif type == 14:
        custom = {'coach_id': obj_id, 'type': 2}
    else:
        return result.result()
    content_message = '快去看看吧，您的老师给你发送了新的辅导信息'
    try:
        SendSmsAndMessage(user_id=user_id, content_message=content_message, custom=custom,
                          send_type=SendSmsAndMessage.ONLY_MESSAGE).send()
    except Exception, e:
        log.warn('send_sms_and_message is error; student_id:%s except:%s' % (user_id, str(e)))
    return result.result()


def cancel_meeting_teacher_sms_message(meeting_id, cancel_type):
    """
    取消班会推送信息
    :param meeting_id:
    :param cancel_type: 1:学生 2：老师
    :return:
    """
    result = db.api.lps.teacher_warning.get_backlog_id_by_meeting_id(meeting_id)
    if result.is_error():
        log.warn('get_backlog_id_by_meeting_id is error; meeting_id:%s' % meeting_id)
    meeting_info = result.result()
    if meeting_info:
        backlog_id = meeting_info.get('id')
        date_str = meeting_info['warn_two_date'].strftime('%m月%d日%H:%M')
        teacher_id = meeting_info.get('teacher_id')
        # 添加取消
        result = db.api.lps.teacher_warning.update_backlog_cancel_is_done_by_id(backlog_id)
        if result.is_error():
            log.warn('update_backlog_cancel_is_done_by_id is error; backlog_id:%s' % backlog_id)
            return False
        # 信息推送
        content_sms = [date_str]
        custom = {
            "type": 5,
            "backlog_id": backlog_id
            }
        if cancel_type == 2:
            content_message = '【取消约课】学员已取消%s开始的直播。您将不需要参加本次约课！' % date_str
            try:
                SendSmsAndMessage(teacher_id, 'teacher_meeting_cancel_student', content_sms, content_message,
                                  custom).send()
            except Exception, e:
                log.warn('send_sms_and_message is error; except:%s' % str(e))
        if cancel_type == 1:
            content_message = '【取消约课】学员已同意取消%s开始的直播。您将不需要参加本次约课！' % date_str
            try:
                SendSmsAndMessage(teacher_id, 'teacher_meeting_cancel_teacher', content_sms, content_message,
                                  custom).send()
            except Exception, e:
                log.warn('send_sms_and_message is error; except:%s' % str(e))
        return True
    return False

def get_warn_times(type):
    """
    获取以计算告警时间（工作时间为早上9点到晚上9点）
    :param type:
    :return:
    """
    warn_one_date, warn_two_date, warn_three_date = None, None, None

    def calc_warn_time(now_datetime, warn_hour):
        """
        :param now_datetime:
        :param warn_hour:
        计算告警时间（工作时间为早上9点到晚上9点）
        """
        # 加上休息时间
        new_warn_hour = (int(warn_hour)/12)*12+warn_hour
        # 当前时间在9点到21点范围(工作时间)
        if datetime.time(9) <= now_datetime.time() <= datetime.time(21):
            # 识别剩余时间是否需要添加跨度的时间
            warn_date = now_datetime+datetime.timedelta(hours=warn_hour % 12)
            if datetime.time(9) <= warn_date.time() < datetime.time(21):
                return now_datetime+datetime.timedelta(hours=new_warn_hour)
            else:
                return now_datetime+datetime.timedelta(hours=new_warn_hour+12)
        else:  # 休息时间
            # 如果在21点以后 则加1天
            if now_datetime.time() > datetime.time(21):
                now_datetime += datetime.timedelta(days=1)
            # 将time 重置为当天9点
            now_datetime = now_datetime.replace(hour=9, minute=0, second=0, microsecond=0)
            return now_datetime+datetime.timedelta(hours=new_warn_hour)

    result = db.api.lps.teacher_warning.get_teacher_warning_by_type(type)
    if result.is_error():
        log.warn('get_teacher_warning_by_type is error type:%s' % type)
    teacher_warning = result.result()
    if teacher_warning:
        now_datetime = datetime.datetime.now()
        try:
            warn_one_date = calc_warn_time(now_datetime, teacher_warning['warn_one_hour'])
        except Exception, e:
            log.warn('calc_warn_time except:%s warn_hour:%s' % (e, teacher_warning['warn_one_hour']))
        try:
            warn_two_date = calc_warn_time(now_datetime, teacher_warning['warn_two_hour'])
        except Exception, e:
            log.warn('calc_warn_time except:%s warn_hour:%s' % (e, teacher_warning['warn_two_hour']))
        try:
            warn_three_date = calc_warn_time(now_datetime, teacher_warning['warn_three_hour'])
        except Exception, e:
            log.warn('calc_warn_time except:%s warn_hour:%s' % (e, teacher_warning['warn_three_hour']))

    return warn_one_date, warn_two_date, warn_three_date


