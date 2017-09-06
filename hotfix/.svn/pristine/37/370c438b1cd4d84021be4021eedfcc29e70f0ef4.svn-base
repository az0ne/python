# -*- coding: utf-8 -*-
from django.conf import settings
import datetime
import db.api.coach.coach
import db.api.onevone.study_service
from django.utils.html import strip_tags
from django.http.response import Http404
from core.common.http.response import failed_json, success_json
from utils.sensitive_word import sensitive_word

from utils.constants import CoachUserType, CoachCommentUserType
from utils.logger import logger as log
from mz_lps4.interface_teacher_warning import add_join_learning_teacher_backlog,add_student_q_a_teacher_backlog,\
         add_coach_info_teacher_backlog, update_teacher_backlog_is_done
from mz_lps4.class_dict import week_day_dict, NORMAL_CLASS_DICT
from mz_lps3 import functions
from mz_usercenter.student.interface_study import get_study_base
from utils.message_queue import mq_service
from utils.send_sms_and_message import SendSmsAndMessage


def get_coach_detail(coach_id, user):
    """
    获取辅导详情
    :param coach_id:
    :param user:
    :return:
    """
    coach = db.api.coach.coach.get_coach(
        coach_id, user.id, user.is_student())

    if coach.is_error():
        log.warn('get_coach failed. coach_id: {0}, '
                 'user_id: {1}.'.format(coach_id, user.id))
        raise Http404
    coach = coach.result()

    if not coach:
        raise Http404
    if coach['source_type'] == CoachUserType.STUDENT_VIDEO:
        # 获取视频提问时间
        source = coach.get('source')
        try:
            coach['t'] = source.split(' ')[-1]
        except:
            coach['t'] = '00:00'

    comment_list = db.api.coach.coach.get_coach_comments(coach_id)
    if comment_list.is_error():
        log.warn('get_coach_comments failed. '
                 'coach_id: {}'.format(coach_id))
        comment_list = []
    else:
        comment_list = comment_list.result()

    return dict(
        coach=coach, comment_list=comment_list,
        CoachUserType=CoachUserType,
        CoachCommentUserType=CoachCommentUserType
    )


def post_coach_comment(coach_id, user, content):
    """
    提交回复
    :param coach_id:
    :param user:
    :param content:
    :return:
    """
    is_student = user.is_student()
    coach = db.api.coach.coach.get_coach(coach_id, user.id, is_student)
    if coach.is_error():
        log.warn('get_coach failed. coach_id: {0}, user_id: {1}, '
                 'is_student: {2}'.format(coach_id, user.id, is_student))
        return failed_json()
    coach = coach.result()

    result = sensitive_word.filter(content)
    if result == sensitive_word.FAIL:
        return failed_json(
            u'内容中包含有敏感词汇。', code=400)
    if result == sensitive_word.SERVER_ERROR:
        return failed_json(
            u'服务器开小差了，请稍后再试。', code=500)

    if not content:
        return failed_json(u'content字段不能为空。', code=400)

    user_type = (CoachCommentUserType.STUDENT if user.is_student()
                 else CoachCommentUserType.TEACHER)
    username = user.real_name or user.nick_name
    result = db.api.coach.coach.add_coach_comment(
        coach_id, content, user_type, user.id, username,
        user.avatar_url, coach['career_id']
    )
    if result.is_error():
        return failed_json(u'服务器开小差了，请稍后再试', code=500)
    comment_id = result.result()
    if not comment_id:
        return failed_json(u'服务器开小差了，请稍后再试', code=500)

    if is_student:
        # 学生回复 需要添加待办(学生发起的问题)
        if coach['source_type'] == CoachUserType.NW_COMMUNICATE:
            add_join_learning_teacher_backlog(
                    user, coach['teacher_id'], coach['career_id'], content, coach_id, comment_id)
        if coach['source_type'] in CoachUserType.students:
            add_student_q_a_teacher_backlog(
                     user, coach['teacher_id'], coach['career_id'], content, coach_id, comment_id)
        if coach['source_type'] in CoachUserType.teachers:
            add_coach_info_teacher_backlog(
                     user, coach['teacher_id'], coach['career_id'], content, coach_id, comment_id)
    else:
        # 老师回复 需要结束待办(学生发起的问题)
        if coach['source_type'] == CoachUserType.NW_COMMUNICATE:
            backlog_type = 11
        if coach['source_type'] in CoachUserType.students:
            backlog_type = 12
        if coach['source_type'] in CoachUserType.teachers:
            backlog_type = 13
        if coach['source_type'] == CoachUserType.PROJECT:
            backlog_type = 14
        update_teacher_backlog_is_done(coach_id, comment_id, coach['teacher_id'], coach['student_id'], backlog_type)
    return success_json()


def get_coach_last_comment(coach_id, is_api=False):
    mapper = {'nick_name': 'name', 'head': 'avatar', 'create_date': 'time'}

    item = db.api.coach.coach.get_last_coach_comment(coach_id)
    if item.is_error():
        log.warn('get_last_coach_comment failed. '
                 'coach_id: {}'.format(coach_id))
        item = {}
    else:
        item = item.result()

    if item and is_api:
        result = dict()
        for k, v in mapper.items():
            result[v] = item[k]
        result['time'] = result['time'].strftime('%Y/%m/%d %T')
        result['avatar'] = settings.SITE_URL + settings.MEDIA_URL + result['avatar']
        return result

    return item


def create_coach_info_student(user, career_id, source, source_location, comment, source_type):
    """
    学生创建辅导信息(10:学生主动发起; 11：学生视频问答;)
    :param user:
    :param career_id:
    :param source:
    :param source_location:
    :param comment:
    :param source_type:
    :return:
    """
    teacher = db.api.onevone.study_service.get_teacher_by_lps4(
        career_id=career_id, student_id=user.id)
    if teacher.is_error() or not teacher.result():
        return failed_json(u'服务器错误')

    if not comment:
        return failed_json(u'内容不能为空')
    abstract = strip_tags(comment)
    abstract = abstract.replace('&nbsp;', '')
    if abstract:
        # 敏感词判断
        result = sensitive_word.filter(abstract)
        if result == sensitive_word.SERVER_ERROR:
            return failed_json(u'服务器错误')
        if result == sensitive_word.FAIL:
            return failed_json(u'含有不正当词汇')
    username = user.real_name or user.nick_name
    # get current Task name
    if not source:
        try:
            class_id = NORMAL_CLASS_DICT.get(int(career_id))
            st_interface = functions.StageTaskInterface(class_id)
            st_interface.load_student_data(user.id)
            current_task = st_interface.get_student_latest_task(user.id)
            userstage = st_interface.get_student_stage_by_stagetask(user.id, current_task.stage_task_id)
            source = '%s %s' % (userstage.name, current_task.task_name)
        except Exception as e:
            log.warn('create new coach error when get current Task name: %s' % str(e))
            source = None
    now = datetime.datetime.now()
    teacher_id = teacher.result()['teacher_id']
    data = {'career_id': career_id, 'student_id': user.id, 'teacher_id': teacher_id, 'nick_name': username,
            'head': user.avatar_url, 'source_type': source_type, 'abstract': abstract, 'source': source, 'now': now,
            'source_location': source_location, 'comment': comment, 'user_id': user.id, 'is_student': True,
            'files_list': None}
    result = db.api.coach.coach.create_new_coach(**data)
    if result.is_error():
        return failed_json(u'服务器错误')
    coach_id = result.result()
    add_student_q_a_teacher_backlog(user, teacher_id, career_id, abstract, coach_id, None)
    return success_json({'content': abstract, 'name': username, 'head': settings.MEDIA_URL + str(user.avatar_url),
                         'source': source, 'create_date': now.strftime('%Y年%m月%d日 %H:%M')})


def create_coach_info_teacher(teacher, career_id, student_id, source, source_location, comment, source_type):
    """
    老师创建辅导信息(20：老师主动发起)
    :param teacher:
    :param career_id:
    :param student_id:
    :param source:
    :param source_location:
    :param comment:
    :param source_type:
    :return:
    """
    if not comment:
        return failed_json(u'内容不能为空')
    abstract = strip_tags(comment)
    abstract = abstract.replace('&nbsp;', '')
    if abstract:
        # 敏感词判断
        result = sensitive_word.filter(abstract)
        if result == sensitive_word.SERVER_ERROR:
            return failed_json(u'服务器错误')
        if result == sensitive_word.FAIL:
            return failed_json(u'含有不正当词汇')
    username = teacher.real_name or teacher.nick_name
    now = datetime.datetime.now()
    data = {'career_id': career_id, 'student_id': student_id, 'teacher_id': teacher.id, 'nick_name': username,
            'head': teacher.avatar_url, 'source_type': source_type, 'abstract': abstract, 'source': source, 'now': now,
            'source_location': source_location, 'comment': comment, 'user_id': teacher.id, 'is_student': False,
            'files_list': None}
    result = db.api.coach.coach.create_new_coach(**data)
    if result.is_error():
        return failed_json(u'服务器错误')
    return success_json()


def create_coach_info_unlock_task(user, source, career_id, task_id):
    """
    创建解锁任务球的辅导
    :param user:
    :param source:
    :param career_id:
    :param task_id:
    :return:
    """

    result = db.api.onevone.study_service.get_teacher_by_lps4(
        career_id=career_id, student_id=user.id)
    if result.is_error() or not result.result():
        return False
    teacher_id = result.result()['teacher_id']
    result = db.api.onevone.study_service.get_user_name(user_id=teacher_id)
    if result.is_error():
        return False
    teacher = result.result()
    result = db.api.coach.coach.get_coach_task_lib_info(career_id, task_id)
    if result.is_error() or not result.result():
        return False
    comment = result.result()['content']
    if not comment:
        return False
    abstract = strip_tags(comment)
    abstract = abstract.replace('&nbsp;', '')
    username = teacher['real_name'] or teacher['nick_name']
    now = datetime.datetime.now()
    data = {'career_id': career_id, 'student_id': user.id, 'teacher_id': teacher_id, 'nick_name': username,
            'head': teacher['avatar_url'], 'source_type': CoachUserType.UNLOCK, 'abstract': abstract,
            'source': source, 'now': now, 'source_location': None, 'comment': comment, 'user_id': user.id,
            'is_student': False, 'files_list': None}
    result = db.api.coach.coach.create_new_coach(**data)
    if result.is_error():
        return False
    return True


def create_coach_info_student_join_class(user, career_id, career_name):
    """
    创建新学员入班的辅导
    :param user:
    :param career_id:
    :param career_name:
    :return:
    """

    result = db.api.onevone.study_service.get_teacher_by_lps4(career_id=career_id, student_id=user.id)
    if result.is_error():
        return False
    teacher_id = result.result()['teacher_id']

    # 加入消息队列
    result = db.api.course.career_course.get_institute_by_career_id(career_id)
    institute = {}
    if not result.is_error():
        institute = result.result()
    mq_data = mq_service.publish({
        "event": "user_study_info_perfect_sync",
        "data": {
            "user_id": str(user.id),
            "domain": institute.get('name')
        }
    })
    log.info('mq_data_user_study_info_perfect_sync: %s' % str(mq_data))
    mq_data = mq_service.publish({
        "event": "notify_teacher_time_sync",
        "data": {
            "user_id": str(user.id),
            "career_id": career_id,
            "notify_teacher_time": datetime.datetime.now().strftime("%F %T")
        }
    })
    log.info('mq_data_notify_teacher_time_sync: %s' % str(mq_data))

    # 学习目标
    study_goal_str = '其他'
    result = db.api.lps.student.student_study_goal(user_id=int(user.id), career_id=int(career_id))
    if result.is_error():
        log.warn('db.api.lps.student.student_study_goal failed : user_id=%s, career_id=%s' % (user.id, career_id))
    else:
        if result.result():
            study_goal_str = result.result()['name']

    # 学习基础
    study_base_str = ""
    result = db.api.lps.student.get_lps_3_institute_name_by_career_id(career_id)
    if result.is_error():
        log.warn('')
    if result.result():
        institute_name = result.result()['name']
        study_base_list = get_study_base(user.id, institute_name)
        if study_base_list:
            study_base_str_begin = '<p>&nbsp;&nbsp;&nbsp;&nbsp;我的学习基础情况：</p>' \
                                   '<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            study_base_str_middle = '</p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'.join(
                                [study_base['name']+'，'+study_base['level']+';' for study_base in study_base_list])
            study_base_str_end = '</p>'
            study_base_str = study_base_str_begin+study_base_str_middle+study_base_str_end
        else:
            study_base_str = ''

    str_mobile = '我的电话是：%s，' % user.mobile if user.mobile else ''
    str_email = '我的邮箱是：%s，' % user.email if user.email else ''
    str_qq = '我的QQ号是：%s。' % user.qq if user.qq else ''
    str_wechat = '我的微信号是：%s。' % user.wechat if user.wechat else ''
    content = '<p>老师您好：</p>' \
              '<p>&nbsp;&nbsp;&nbsp;&nbsp;我刚加入您的%s课程进行1V1学习。%s%s%s%s</p>' \
              '<p>&nbsp;&nbsp;&nbsp;&nbsp;我的学习目标：%s</p>%s' \
              '<p>麻烦老师帮我制定下符合我个人情况的学习建议吧！</p>' % (
                  career_name, str_mobile, str_email, str_qq, str_wechat,
                  study_goal_str, study_base_str)
    abstract = strip_tags(content)
    abstract = abstract.replace('&nbsp;', '')
    username = user.real_name or user.nick_name
    now = datetime.datetime.now()
    data = {'career_id': career_id, 'student_id': user.id, 'teacher_id': teacher_id, 'nick_name': username,
            'head': user.avatar_url, 'source_type': CoachUserType.NW_COMMUNICATE, 'abstract': abstract,
            'source': None, 'now': now, 'source_location': None, 'comment': content, 'user_id': user.id,
            'is_student': True, 'files_list': None}
    result = db.api.coach.coach.create_new_coach(**data)
    if result.is_error():
        return False
    coach_id = result.result()
    add_join_learning_teacher_backlog(user, teacher_id, career_id, abstract, coach_id, None,
                                      send_type=SendSmsAndMessage.BOTH_SMS_AND_MESSAGE)
    return True
