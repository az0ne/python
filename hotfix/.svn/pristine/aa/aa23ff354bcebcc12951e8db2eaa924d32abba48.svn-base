# -*- coding: utf-8 -*-
import re
import datetime
import time
import json
from hashlib import md5

from django.utils.html import strip_tags
import db.api.onevone.study_service
import db.api.onevone.meeting
import db.api.lps.teacher_warning
import db.api.lps.student
import db.api.coach.coach
import db.api.lps.lps_index
from core.common.http.response import success_json, failed_json
from mz_common.functions import paginater, safe_int
from mz_lps.models import Project, ProjectMaterial, ProjectImage, Class
from mz_lps3.models import UserTaskRecord, UserKnowledgeItemRecord, KnowledgeItem
from mz_lps3.views_student_project import create_or_find_dir
from mz_lps4.class_dict import week_day_dict, LPS4_DICT
from mz_lps4.interface import serialize_onevone_meeting_time_list, get_onevone_meeting
from mz_lps4.interface_coach import post_coach_comment, get_coach_last_comment
from mz_lps4.models import OnevoneMeeting
from mz_lps4.views import send_mobile_captcha_from_onevone_meeting
from mz_usercenter.teacher.interface import check_onevone_meeting
from utils.constants import CoachUserType, CoachCommentUserType
from utils.is_logined import student_in_career_required
from utils.message_queue import mq_service
from utils.send_sms_and_message import SendSmsAndMessage
from utils.sensitive_word import sensitive_word
from utils.tool import get_param_by_request
from website.api.user.decorators import app_user_required
from django.conf import settings
from utils.logger import logger as log
from mz_lps4.interface_teacher_warning import cancel_meeting_teacher_sms_message, add_meeting_teacher_backlog, \
    add_project_coach_teacher_backlog
from website.api.warning_teacher.interface import get_backlog_detail_by_id_interface
from mz_lps4.interface_coach import create_coach_info_student


# 学习建议列表
@app_user_required
def app_student_service_list(request):
    career_id = request.POST.get('ccourse_id')
    page = int(request.POST.get('page', 1))
    page_size = int(request.POST.get('pageSize', 15))
    student = request.user
    result = db.api.onevone.study_service.get_teacher_by_lps4(career_id=career_id, student_id=request.user.id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    if not result.result():
        return success_json({'status': 0, 'career_url': settings.SITE_URL + '/course/'})
    teacher_id = result.result()['teacher_id']
    # result = db.api.onevone.study_service.student_service_count(
    # career_id=career_id, student_id=student.id, teacher_id=teacher_id)
    # if result.is_error():
    #     return failed_json(u'服务器开小差了,稍后再试吧')
    # if not result.result():
    #     total_count = 0
    # else:
    #     total_count = result.result()['total_count']
    # page_count_list, page_index, start_index, end_index = paginater(page, page_size, total_count, 2)
    if page < 1:
        page = 1
    result = db.api.onevone.study_service.service_list(career_id=int(career_id), student_id=int(student.id),
                                                       teacher_id=0, start_index=(page-1)*page_size,
                                                       end_index=page_size)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    data_list = result.result()
    # 清除学生未读服务数
    result = db.api.onevone.study_service.clean_new_service_count(career_id=career_id, teacher_id=teacher_id,
                                                                  user_id=request.user.id, user=request.user)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    data = [dict(
            service_id=service['id'],
            name=service['nick_name'],
            avatar=settings.SITE_URL + settings.MEDIA_URL + service['head'],
            user_type=1 if student.id == service['user_id'] else 2,  # 直通班学员：1，老师：2
            time=service['create_date'].strftime('%Y/%m/%d %H:%M:%S'),
            content=strip_tags(service['content']),
            source=service['source'],
            student_unread=service['student_unread']
            ) for service in data_list]
    return success_json({'list': data, 'status': 1})


# 学习建议详情
@app_user_required
def app_student_service_detail(request):
    service_id = request.POST.get('service_id')
    page = int(request.POST.get('page', 1))
    page_size = int(request.POST.get('pageSize', 15))
    type_student, type_teacher = 1, 2

    user = request.user
    is_student = user.is_student()
    result = db.api.onevone.study_service.get_service_detail_and_count(service_id=service_id)

    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    service = result.result()['service']
    if not service:
        return failed_json(u'学习建议详情为空')
    if is_student:
        type_self, type_other = type_student, type_teacher
        if user.id != service['user_id']:
            return failed_json(u'权限不符合')
    else:
        type_self, type_other = type_teacher, type_student
        if user.id != service['teacher_id']:
            return failed_json(u'权限不符合')
    if page < 1:
        page = 1
    result = db.api.onevone.study_service.one_to_one_service_detail(service_id=service_id,
                                                                    start_index=(page-1)*page_size,
                                                                    end_index=page_size)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    comments = result.result()
    # 清除相应未读数目
    result = db.api.onevone.study_service.clean_service_message_count(service=service, user=request.user)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    p = re.compile(r'src="/')
    pic_url = 'src="%s/' % settings.SITE_URL
    data = [dict(
            service_id=comment['service_id'],
            name=comment['nick_name'],
            avatar=settings.SITE_URL + settings.MEDIA_URL + comment['head'],
            user_type=type_self if user.id == comment['user_id'] else type_other,
            time=comment['create_date'].strftime('%Y/%m/%d %H:%M:%S'),
            content=p.sub(pic_url, comment['comment']) if comment['comment'].startswith('<p') else
            p.sub(pic_url, '<p>%s</p>' % comment['comment']),
            ) for comment in comments]
    final_data = {'list': data}
    if page == 1:
        final_data['list'][0].update({'source': service['source']})
        if not is_student:  # is_teacher
            # update priority and deadline in data
            backlog_id = request.POST.get('backlog_id')
            result = get_backlog_detail_by_id_interface(backlog_id)
            if not result.get('success', False):
                log.warn('get_backlog_detail_by_id_interface error, backlog_id %s' % backlog_id)
                return failed_json(u'服务器开小差了,稍后再试吧')
            final_data.update(result.get('data', {}))
            # update is_new in backlog
            result = db.api.lps.teacher_warning.update_backlog_status_by_obj_id('is_new', service_id, 1, 2)
            # 1, 2 is service
            if result.is_error():
                log.warn('db update_backlog_status_by_obj_id error, backlog_id %s' % backlog_id)
    return success_json(final_data)


# 学习建议回复提交
@app_user_required
def app_student_submit_service_comment(request):
    service_id = request.POST.get('service_id')
    content = request.POST.get('comment')
    user = request.user
    is_student = user.is_student()
    result = db.api.onevone.study_service.get_service_detail_and_count(service_id=service_id)

    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    service = result.result()['service']
    if not service:
        return failed_json(u'请先报名')
    if is_student:
        if user.id != service['user_id']:
            return failed_json(u'权限不符合')
    else:
        if user.id != service['teacher_id']:
            return failed_json(u'权限不符合')

    result = db.api.onevone.study_service.add_service_reply(service=service, user=user, content=content)
    if result.is_error():
        return failed_json(u'服务器错误, 请稍后再试')

    # 老师回复 需要结束待办(学生发起的问题)
    if user.is_teacher() and service['source_type'] == 0:
        if service['source']:
            pass
        else:
            # 加入消息队列
            result = db.api.onevone.study_service.get_onevone_service_comment(service_id, service['teacher_id'])
            if not result.is_error() and result.result():
                mq_data = mq_service.publish({
                    "event": "new_student_communicate_finish",
                    "data": {
                        "user_id": str(service['user_id']),
                        "teacher_id": str(service['teacher_id'])
                    }
                })
                log.info('mq_new_student_communicate_finish: %s' % str(mq_data))

    return success_json()


# 学习建议回复提交 上传图片
@app_user_required
def app_student_service_upload(request):
    # 判断图片格式,大小
    data = {}
    for f in request.FILES.values():
        if "*.jpg; *.jpeg; *.png;".find(f.name.split(".")[-1]) == -1:
            return failed_json(u"头像必须为JPG/PNG/JPEG格式")
        if f.size / 1024 > 5000:
            return failed_json(u"图片大小超过5MB限制")
        ext = f.name.split('.')[-1]
        image_md5 = md5()
        image_md5.update(str(f) + str(time.time()))
        file_relative_path = '/'.join((create_or_find_dir(), image_md5.hexdigest()))
        file_path = '/'.join((settings.MEDIA_ROOT, file_relative_path))
        image_file = open(file_path + '.' + ext, 'wb')
        image = f.read()
        image_file.write(image)
        image_file.close()
        img_url = file_relative_path + '.' + ext
        data.update({f.name.split(".")[0]: '/uploads/' + img_url})
    return success_json({'images': data})


# 预约发送短信
@app_user_required
def app_student_meeting_send_sms(request):
    return send_mobile_captcha_from_onevone_meeting(request)


# 是否被直播已被预约
@app_user_required
def is_meeting_ordered(request):
    meeting_id = get_param_by_request(request.POST, "meeting_id", 0, int)
    result = db.api.onevone.meeting.is_ordered_onevone_meeting(meeting_id)
    if result.is_error():
        return failed_json(u'直播课已经被预约')
    if result.result():
        return failed_json(u'直播课已经被预约')
    return success_json()


# 可预约直播
@app_user_required
def app_student_meeting_unordered(request):
    key = request.POST.get('type')
    career_id = request.POST.get('ccourse_id')
    page = int(request.POST.get('page', 1))
    page_size = int(request.POST.get('pageSize', 15))
    user_id = request.user.id
    # 获取老师ID
    result = db.api.onevone.study_service.get_teacher_by_lps4(career_id=career_id, student_id=user_id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    if not result.result():
        return failed_json(u'请先报名')
    teacher_id = result.result()['teacher_id']
    # 获取老师信息
    result = db.api.onevone.study_service.get_user_name(user_id=teacher_id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    teacher_name = result.result()['real_name'] or result.result()['nick_name']
    teacher_avatar = settings.SITE_URL + settings.MEDIA_URL + result.result()['avatar_url']
    # 剩余预约次数
    result = db.api.onevone.meeting.get_onevone_meeting_user_count(user_id, career_id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    residue_count = result.result()

    data = []
    if key == '1':
        # 未预约
        result = db.api.onevone.meeting.get_recent_onevone_meeting(teacher_id, False, datetime.datetime.now(), 0, 0)
        if result.is_error():
            return failed_json(u'服务器开小差了,稍后再试吧')
        for meeting in result.result():
            data.append({
                "meeting_id": meeting['id'],
                "max_num": residue_count,
                "start_time": meeting['start_time'].strftime('%H:%M'),
                "end_time": meeting['end_time'].strftime('%H:%M'),
                "datetime": meeting['end_time'].strftime('%Y/%m/%d'),
                "week_time": week_day_dict[meeting['start_time'].weekday()],
                "status": 0 if meeting['status'] == 'DATED' else 1
            })
    elif key == '2':
        # 未预约和已被他人预约
        if page < 1:
            page = 1
        result = db.api.onevone.meeting.get_recent_onevone_meeting(teacher_id, True, datetime.datetime.now(),
                                                                   (page-1)*page_size, page_size)
        if result.is_error():
            return failed_json(u'服务器开小差了,稍后再试吧')
        for meeting in result.result():
            data.append({
                "meeting_id": meeting['id'],
                "max_num": residue_count,
                "start_time": meeting['start_time'].strftime('%H:%M'),
                "end_time": meeting['end_time'].strftime('%H:%M'),
                "datetime": meeting['end_time'].strftime('%Y/%m/%d'),
                "week_time": week_day_dict[meeting['start_time'].weekday()],
                "status": 0 if meeting['status'] == 'DATED' else 1
            })
    else:
        return failed_json(u'类型错误')
    return success_json({'list': data, 'avatar': teacher_avatar, 'teacher_name': teacher_name})


@app_user_required
def app_student_meeting_submit(request):
    """
    学生创建直播
    :param request:
    :return:
    """
    user_id = request.user.id
    career_id = get_param_by_request(request.POST, "ccourse_id", 0, int)
    question = get_param_by_request(request.POST, "question", "", str)
    start_time = get_param_by_request(request.POST, "start_time", "", str)
    if not career_id or not question or not start_time:
        return failed_json(u'参数不全')

    try:
        student_in_career_required(request)
    except Exception as e:
        log.warn('student_in_career_required error.career_id: %s.%s.' % (career_id, str(e)))
        return failed_json(unicode(e))

    # 去标签
    _question = strip_tags(question)

    # 检查字数
    if len(_question.encode('gbk')) > 1000:
        return failed_json(u'输入超过1000字，请重新输入')
    if len(_question.encode('gbk')) < 15:
        return failed_json(u'输入少于15字，请重新输入')

    # 检查敏感词
    result = sensitive_word.filter(_question)
    if result == sensitive_word.SERVER_ERROR:
        return failed_json(u'服务器错误')
    if result == sensitive_word.FAIL:
        return failed_json(u'含有不正当词汇')

    # 查询老师
    result = db.api.lps.student.get_lps4_teacher_by_career_student_id(career_id, user_id)
    if result.is_error():
        log.warn('get_lps4_teacher_by_career_student_id is error career_id:%s user_id:%s' % (career_id, user_id))
        return failed_json(u'服务器错误')
    teacher = result.result()
    if not teacher:
        return failed_json(u'获取所预约老师失败，请联系老师')

    # 查询时间是否合法
    teacher_id = teacher.get('id', 0)
    try:
        start_time, end_time = check_onevone_meeting(start_time, teacher_id)
    except Exception as e:
        return failed_json(unicode(e))

    teacher_name = teacher.get('real_name', teacher.get('nick_name', ''))
    # 插入班会
    result = db.api.onevone.meeting. \
        create_onevone_meeting(career_id, user_id, teacher_id, teacher_name, start_time, end_time, question)
    if result.is_error():
        if result.result():
            return failed_json(result.result())
        log.warn('create_onevone_meeting is error teacher_id:%s teacher_name:%s' % (teacher_id, teacher_name))
        return failed_json(u'预约失败，请重新提提交')
    meeting_id_dict = result.result()
    if not isinstance(meeting_id_dict, dict):
        return failed_json(u'获取预约返回信息失败')
    meeting_id = meeting_id_dict.get('LAST_INSERT_ID()', 0)

    try:
        # 预约1v1成功后，添加老师预约待办(确保加入)
        add_meeting_teacher_backlog(request.user, teacher_id, career_id, question, meeting_id)
    except Exception as e:
        log.warn(str(e))
        return failed_json(unicode(e))

    try:
        # 预约成功短信
        _start_time = start_time.strftime('%m月%d日%R') + '-' + end_time.strftime('%R')
        SendSmsAndMessage(user_id=user_id, tmp_id='student_order_onevone', content_sms=[_start_time],
                          custom={'meeting_id': meeting_id, 'type': 3}, send_type=SendSmsAndMessage.ONLY_SMS).send()
    except Exception as e:
        log.warn(str(e))

    return success_json(dict(
        date='%s %s' % (start_time.strftime('%Y/%m/%d'), week_day_dict[start_time.weekday()]),
        start_time=start_time.strftime('%R'),
        end_time=end_time.strftime('%R')
    ))


@app_user_required
def get_available_date_list(request):
    """
    获取可预约时间列表
    :param request:
    :return:
    """
    try:
        user_id = request.user.id
        career_id = int(request.POST.get('ccourse_id'))
    except Exception as e:
        log.warn('para error %s' % str(e))
        return failed_json(u'参数错误')

    try:
        student_in_career_required(request)
    except Exception as e:
        log.warn('student_in_career_required error.career_id: %s.%s.' % (career_id, str(e)))
        return failed_json(unicode(e))

    data = serialize_onevone_meeting_time_list(career_id, user_id)
    if not data:
        return failed_json(u'参数错误')
    return success_json(data)


@app_user_required
def cancel_meeting(request):
    """
    删除班会
    :param request:
    :return:
    """
    try:
        user_id = request.user.id
        meeting_id = int(request.POST.get('meeting_id'))
        reason = int(request.POST.get('reason'))
    except Exception as e:
        log.warn('para error %s' % str(e))
        return failed_json(u'参数错误')

    try:
        student_in_career_required(request)
    except Exception as e:
        log.warn('student_in_career_required error.meeting_id: %s.%s.' % (meeting_id, str(e)))
        return failed_json(unicode(e))

    result = db.api.onevone.meeting.cancel_meeting_by_meeting_id(meeting_id, reason, request.user.id)
    if result.is_error():
        if result.result():
            return failed_json(result.result())
        log.warn('cancel_meeting_by_meeting_id error, meeting_id %s' % meeting_id)
        return failed_json(u'取消班会错误')
    start_time = result.result().get('start_time')

    # 给老师发取消短信
    try:
        result = cancel_meeting_teacher_sms_message(meeting_id, reason)
        if not result:
            log.warn('cancel_meeting_teacher_sms_message is False')
    except Exception as e:
        log.warn(str(e))

    # 给学生发取消班会短信
    try:
        _start_time = start_time.strftime('%m月%d日%R')
        SendSmsAndMessage(user_id=user_id, tmp_id='student_cancel_onevone', content_sms=[_start_time],
                          custom={'meeting_id': meeting_id, 'type': 3}, send_type=SendSmsAndMessage.ONLY_SMS).send()
    except Exception as e:
        log.warn(str(e))

    return success_json()


@app_user_required
def student_onevone_meeting_detail(request):
    """
    学生1v1直播详情
    :param request:
    :return:
    """
    try:
        meeting_id = int(request.POST.get('meeting_id'))
    except Exception as e:
        log.warn('para error %s' % str(e))
        return failed_json(u'参数错误')

    try:
        student_in_career_required(request)
    except Exception as e:
        log.warn('student_in_career_required error.meeting_id: %s.%s.' % (meeting_id, str(e)))
        return failed_json(unicode(e))

    try:
        m = get_onevone_meeting(meeting_id)
        start_time = m['start_time']
        status_dict = OnevoneMeeting.STATUS_DICT
        _question = re.sub(r'src="/', 'src="%s/' % settings.SITE_URL, m['question']) if m['question'] else ''
        question = _question if _question.startswith('<p>') else '<p>%s</p>' % _question
        data = {
            "teacher_avatar": settings.SITE_URL + settings.MEDIA_URL + m['teacher_head'],
            "teacher_name": m['teacher_real_name'] or m['teacher_nick_name'],
            "start_time": start_time.strftime('%R'),
            "end_time": m['end_time'].strftime('%R'),
            "datetime": start_time.strftime('%Y/%m/%d'),
            "week_time": week_day_dict[start_time.weekday()],
            "token": m['student_client_token'],
            "join_url": m['student_url'],
            "room_number": m['live_code'],
            "student_name": m['user_real_name'] or m['user_nick_nam'],
            "student_avatar": settings.SITE_URL + settings.MEDIA_URL + m['user_head'],
            "create_time": m['create_date_time'].strftime('%F %R'),
            "question": question,
            "status": 4 if m['star'] else status_dict[m['status']],
            "evaluate": {
                "score": str(m['star']) if m['star'] else None,
                "comment": m['suggest']
            }
        }
    except Exception as e:
        log.warn(str(e))
        return failed_json(u'服务器开小差了,稍后再试吧')
    return success_json(data)


@app_user_required
def app_get_coach_list(request):
    """
    辅导列表
    :param request:
    :return:
    """
    user = request.user
    career_id = request.POST.get('career_id')
    if not career_id:
        return failed_json(u'career_id不能为空。', code=400)
    result = db.api.onevone.study_service.get_teacher_by_lps4(career_id=career_id, student_id=user.id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    if not result.result():
        return success_json({'status': 0, 'career_url': settings.SITE_URL + '/course/'})
    mapper = {
        'id': 'service_id', 'nick_name': 'name', 'head': 'avatar',
        'create_date': 'create_time', 'abstract': 'content',
        'source': 'source', 'source_type': 'service_type'
    }

    page = safe_int(request.POST.get('page', 1), 1)
    page_size = safe_int(request.POST.get('page_size', 20), 20)

    data = db.api.coach.coach.student_coach_list(
        career_id=int(career_id), student_id=int(user.id),
        start_index=(page-1)*page_size, end_index=page_size)
    if data.is_error():
        return failed_json()
    data = data.result()

    # 清除学生未读服务数
    result = db.api.coach.coach.clean_new_coach_count(
        career_id=career_id, user_id=request.user.id, teacher_id=None)
    if result.is_error():
        return failed_json()

    data_list = []
    for d in data:
        vd = dict()
        for k, v in mapper.items():
            if k == 'create_date':
                vd[v] = d[k].strftime('%Y/%m/%d %T')
            elif k == 'source_type':
                vd[v] = 2 if d[k] == CoachUserType.PROJECT else 1
            elif k == 'head':
                vd[v] = settings.SITE_URL + settings.MEDIA_URL + d[k]
            else:
                vd[v] = d[k]
        vd['is_new'] = 1 if d['student_replay_count'] != 0 else 0
        if vd['service_type'] == 1:
            vd['reply_item'] = get_coach_last_comment(d['id'], is_api=True)
            vd['reply_item'] = vd['reply_item'] if vd['reply_item'] else None
        else:
            source_location = json.loads(d['source_location'])
            source_location = source_location['project']
            try:
                user_task_record = UserTaskRecord.objects.get(class_id=source_location['class_id'],
                                                              student_id=user.id,
                                                              stage_task_id=source_location['stage_task_id'])
            except UserTaskRecord.DoesNotExist:
                return failed_json(u'数据错误')
            if source_location['item_id']:
                is_task = False
                try:
                    item_record = UserKnowledgeItemRecord.objects.get(student_id=user.id,
                                                                      class_id=source_location['class_id'],
                                                                      knowledge_item_id=source_location['item_id'],
                                                                      user_task_record=user_task_record)
                except UserKnowledgeItemRecord.DoesNotExist:
                    return failed_json(u'数据错误')
                project_id = item_record.knowledge_item.obj_id
                project = Project.objects.get(id=project_id)
                project_status = None
                score = None
            else:
                is_task = True
                project_id = user_task_record.stage_task.task.project_id
                project = Project.objects.get(id=project_id)
                if user_task_record.status == 'DONE':
                    project_status = 1
                elif user_task_record.status == 'DOING':
                    project_status = 0
                else:
                    project_status = 2
                score = user_task_record.score
            vd['project_item'] = dict(
                    project_name=project.title,
                    score=score,
                    project_status=project_status,
                    is_task=is_task
            )
        data_list.append(vd)

    data = {
        'list': data_list,
        'status': 1
    }
    return success_json(data)


@app_user_required
def app_create_coach_info(request):
    """
    创建辅导详情
    :param request:
    :return:
    """
    user = request.user
    career_id = request.POST.get('career_id')
    source = request.POST.get('source')
    source_location = request.POST.get('source_location')
    comment = request.POST.get('question')
    source_type = request.POST.get('source_type', CoachUserType.STUDENT)
    try:
        return create_coach_info_student(user, career_id, source, source_location, comment, source_type)
    except Exception, e:
        log.warn('create_coach_info_student is except:%s' % str(e))
        return failed_json(u'服务器错误')


@app_user_required
def coach_detail(request):
    """
    辅导详情
    :param request:
    :return:
    """
    coach_id = request.POST.get('coach_id')
    page = safe_int(request.POST.get('page', 1), 1)
    page_size = safe_int(request.POST.get('page_size', 15), 15)

    user = request.user

    coach_result = db.api.coach.coach.get_coach(
        coach_id, user.id, user.is_student())

    if coach_result.is_error():
        log.warn('get_coach failed. coach_id: {0}, '
                 'user_id: {1}.'.format(coach_id, user.id))
    coach = coach_result.result()
    if not coach:
        return failed_json(u'服务器开小差了,稍后再试吧')

    comments_result = db.api.coach.coach.get_coach_comments(
        coach_id, start_index=(page - 1) * page_size, end_index=page_size)
    if comments_result.is_error():
        log.warn('get_coach_comments failed. '
                 'coach_id: {}'.format(coach_id))
        comments = []
    else:
        comments = comments_result.result()

    p = re.compile(r'src="/')
    pic_url = 'src="%s/' % settings.SITE_URL
    data = [dict(
        comment_id=comment['id'],
        name=comment['nick_name'],
        avatar=settings.SITE_URL + settings.MEDIA_URL + comment['head'],
        user_type=1 if comment['user_type'] == CoachCommentUserType.STUDENT else 2,
        create_time=comment['create_date'].strftime('%Y/%m/%d %T'),
        content=p.sub(pic_url, comment['comment']) if comment['comment'].startswith('<p') else
        p.sub(pic_url, '<p>%s</p>' % comment['comment']),
        source=''
    ) for comment in comments]
    if len(data) > 0:
        data[0]['source'] = coach['source']

    final_data = {'list': data}

    return success_json(final_data)


@app_user_required
def app_reply_coach_info(request):
    """
    学生回复辅导
    :param request:
    :return:
    """
    user = request.user
    coach_id = request.POST.get('coach_id')
    comment = request.POST.get('comment')

    if not coach_id:
        return failed_json(u"coach_id不能为空", code=400)
    if not comment:
        return failed_json(u"comment不能为空", code=400)
    try:
        result = post_coach_comment(coach_id, user, comment)
    except Exception, e:
        log.warn('post_coach_comment is except:%s coach_id:%s' % (str(e), coach_id))
        result = failed_json(u'服务器开小差了，请稍后再试。')

    return result


@app_user_required
def app_student_project_coach(request):
    # 项目辅导详情
    from_type = safe_int(request.POST.get('type'), None)
    class_id = safe_int(request.POST.get('class_id'), 0)
    stage_task_id = safe_int(request.POST.get('stagetask_id'), 0)
    item_id = safe_int(request.POST.get('item_id'), 0)
    coach_id = safe_int(request.POST.get('coach_id'), 0)
    user = request.user
    is_lps3 = False
    show_score = False
    is_free = True
    if from_type == 1:
        career_id = LPS4_DICT.get(class_id, 0)
        if not career_id:
            try:
                klass = Class.objects.xall().get(id=class_id)
                if klass.class_type == Class.CLASS_TYPE_NORMAL:
                    is_lps3 = True
            except Class.DoesNotExist:
                return failed_json(u'找不到相关数据')

        coach = None
        source_location = json.dumps(dict(
            project=dict(
                class_id=int(class_id),
                stage_task_id=int(stage_task_id),
                item_id=int(item_id),
                student_id=int(user.id)
            )
        ))
    elif from_type == 2:
        result = db.api.coach.coach.get_coach(coach_id, user.id, True)
        if result.is_error():
            return failed_json(u'服务器开小差了，请稍后再试。')
        if not result.result():
            return failed_json(u'没有相关数据')
        coach = result.result()
        if coach['student_id'] != user.id:
            return failed_json(u'权限不符')
        career_id = coach['career_id']
        source_location = json.loads(coach['source_location'])
        source_location = source_location['project']
        class_id = source_location['class_id']
        stage_task_id = source_location['stage_task_id']
        item_id = source_location['item_id']
    else:
        return failed_json(u'type error')
    try:
        user_task_record = UserTaskRecord.objects.get(class_id=class_id, student_id=user.id,
                                                      stage_task_id=stage_task_id)
    except UserTaskRecord.DoesNotExist:
        return failed_json(u'找不到相关数据')

    result = db.api.onevone.study_service.get_teacher_info_by_lps4(int(career_id), int(user.id))
    if result.is_error():
        return failed_json(u'服务器开小差了，请稍后再试。')
    teacher = result.result()

    comment_list = []
    if teacher:
        is_free = False
        if from_type == 1:
            result = db.api.coach.coach.get_project_coach(career_id, user.id, teacher['id'], source_location, True)
            if result.is_error():
                return failed_json(u'服务器开小差了，请稍后再试。')
            if result.result():
                coach = result.result()
                result = db.api.coach.coach.get_project_coach_comment(coach['id'])
                if result.is_error():
                    return failed_json(u'服务器开小差了，请稍后再试。')
                comment_list = result.result()
        else:
            result = db.api.coach.coach.get_project_coach_comment(coach['id'])
            if result.is_error():
                return failed_json(u'服务器开小差了，请稍后再试。')
            comment_list = result.result()
    if item_id:
        try:
            KnowledgeItem.objects.get(id=item_id)
        except KnowledgeItem.DoesNotExist:
            return failed_json(u'找不到相关数据')
        try:
            item_record = UserKnowledgeItemRecord.objects.get(student_id=user.id, class_id=class_id,
                                                              knowledge_item_id=item_id,
                                                              user_task_record=user_task_record)
        except UserKnowledgeItemRecord.DoesNotExist:
            item_record = UserKnowledgeItemRecord(status="DOING", knowledge_item_id=item_id, student_id=user.id,
                                                  class_id=class_id, user_task_record=user_task_record)
            item_record.save()
        project_id = item_record.knowledge_item.obj_id
        project = Project.objects.get(id=project_id)
    else:
        project_id = user_task_record.stage_task.task.project_id
        project = Project.objects.get(id=project_id)
    project_material = ProjectMaterial.objects.filter(project=project)
    project_image = ProjectImage.objects.filter(project=project)
    p = re.compile(r'src="/')
    pic_url = 'src="%s/' % settings.SITE_URL
    tmp = {}
    comments = []
    for comment in comment_list:
        if tmp.get('comment_id') == comment['id']:
            tmp['sub_material'].append(comment['file_name'])
        else:
            if tmp:
                comments.append(tmp)
            tmp = dict(
                comment_id=comment['id'],
                content=p.sub(pic_url, comment['comment']) if comment['comment'].startswith('<p') else
                p.sub(pic_url, '<p>%s</p>' % comment['comment']),
                user_type=1 if comment['user_type'] == 10 else 2,
                user_id=comment['user_id'],
                name=comment['nick_name'],
                avatar=settings.SITE_URL + settings.MEDIA_URL + comment['head'],
                create_time=comment['create_date'].strftime("%Y/%m/%d %H:%M:%S"),
                sub_material=[]
            )
            if comment['mz_coach_project.id']:
                tmp['sub_material'].append(comment['file_name'])
    if tmp:
        comments.append(tmp)
    teacher_name = '小麦'
    teacher_header = settings.SITE_URL + '/static/images/wapwike/weixin_share_logo.jpg'
    if teacher:
        teacher_name = teacher['real_name'] or teacher['nick_name']
        teacher_header = settings.MEDIA_URL + teacher['avatar_url']
    if user_task_record.status == 'DONE':
        project_status = 1
    elif user_task_record.status == 'DOING':
        project_status = 0
    else:
        project_status = 2
    if teacher and not item_id:
        show_score = True
    if is_lps3 and not item_id:
        show_score = True
    data = dict(
        project_info=dict(
            is_free=is_free,
            show_score=show_score,
            class_id=class_id,
            stage_task_id=stage_task_id,
            item_id=item_id,
            teacher_name=teacher_name,
            teacher_header=teacher_header,
            project_id=project.id,
            project_name=project.title,
            project_desc=project.description,
            project_score=user_task_record.score,
            project_status=project_status,
            project_material=[material.name for material in project_material],
            img_list=[settings.SITE_URL+settings.MEDIA_URL+str(img.image) for img in project_image]
        ),
        reply_list=comments if comments else None,
    )
    return success_json(data)


@app_user_required
def app_reply_student_project_coach(request):
    # 回复项目辅导
    from_type = safe_int(request.POST.get('type'), None)
    class_id = safe_int(request.POST.get('class_id'), 0)
    stage_task_id = safe_int(request.POST.get('stagetask_id'), 0)
    item_id = safe_int(request.POST.get('item_id'), 0)
    coach_id = safe_int(request.POST.get('coach_id'), 0)
    comment = request.POST.get('comment')

    user = request.user
    if not comment:
        return failed_json(u'内容不能为空')
    abstract = strip_tags(comment)
    abstract = abstract.replace('&nbsp;', '')
    if abstract:
        # 敏感词判断
        result = sensitive_word.filter(abstract)
        if result == sensitive_word.SERVER_ERROR:
            return failed_json(u'服务器开小差了，请稍后再试。')
        if result == sensitive_word.FAIL:
            return failed_json(u'含有不正当词汇')

    if from_type == 1:
        career_id = LPS4_DICT.get(class_id)
        source_location = json.dumps(dict(
            project=dict(
                class_id=int(class_id),
                stage_task_id=int(stage_task_id),
                item_id=int(item_id),
                student_id=int(user.id)
            )
        ))
    elif from_type == 2:
        result = db.api.coach.coach.get_coach_data(coach_id)
        if result.is_error():
            return failed_json(u'服务器开小差了，请稍后再试。')
        if not result.result():
            return failed_json(u'没有相关数据')
        coach = result.result()
        if coach['student_id'] != user.id:
            return failed_json(u'权限不符')
        career_id = coach['career_id']
        source_location = json.loads(coach['source_location'])
        source_location = source_location['project']
        class_id = source_location['class_id']
        stage_task_id = source_location['stage_task_id']
        item_id = source_location['item_id']
        coach_id = coach['id']
    else:
        return failed_json(u'type error')

    try:
        user_task_record = UserTaskRecord.objects.get(class_id=class_id, student_id=user.id,
                                                      stage_task_id=stage_task_id)
    except UserTaskRecord.DoesNotExist:
        return failed_json(u'找不到相关数据')

    if item_id:
        try:
            item_record = UserKnowledgeItemRecord.objects.get(student_id=user.id, class_id=class_id,
                                                              knowledge_item_id=item_id,
                                                              user_task_record=user_task_record)
        except UserKnowledgeItemRecord.DoesNotExist:
            return failed_json(u'找不到相关数据')
        project_id = item_record.knowledge_item.obj_id
        project = Project.objects.get(id=project_id)
    else:
        project_id = user_task_record.stage_task.task.project_id
        project = Project.objects.get(id=project_id)

    result = db.api.onevone.study_service.get_teacher_info_by_lps4(int(career_id), int(user.id))
    if result.is_error():
        return failed_json(u'服务器开小差了，请稍后再试。')
    teacher = result.result()
    if not result.result():
        return failed_json(u'权限不符')
    now = datetime.datetime.now()
    username = user.real_name or user.nick_name
    if from_type == 1:
        result = db.api.coach.coach.get_project_coach(career_id, user.id, teacher['id'], source_location, True, False)
        if result.is_error():
            return failed_json(u'服务器开小差了，请稍后再试。')
        if result.result():
            coach_id = result.result()['id']
        else:
            # 新建
            source = '【项目制作】 %s %s' % (user_task_record.stage_task.task.name, project.title)
            data = {'career_id': career_id, 'student_id': user.id, 'teacher_id': teacher['id'], 'nick_name': username,
                    'head': str(user.avatar_url), 'source_type': 30, 'abstract': abstract, 'source': source, 'now': now,
                    'source_location': source_location, 'comment': comment, 'user_id': user.id,
                    'is_student': True, 'files_list': None}
            result = db.api.coach.coach.create_new_coach(**data)
            if result.is_error():
                return failed_json(u'服务器错误')
            if int(item_id) == 0:
                user_task_record.status = 'DONE'
                user_task_record.done_time = datetime.datetime.now()
                user_task_record.save()
                if teacher:
                    coach_id = result.result()
                    add_project_coach_teacher_backlog(user, teacher['id'], career_id, abstract, coach_id, None,
                                                      send_type=SendSmsAndMessage.BOTH_SMS_AND_MESSAGE)
            else:
                item_record = UserKnowledgeItemRecord.objects.get(
                        class_id=class_id, student_id=request.user.id,
                        knowledge_item_id=item_id, user_task_record=user_task_record)
                if user_task_record.status == 'DOING':
                    item_record.status = 'DONE'
                    item_record.done_time = datetime.datetime.now()
                    item_record.save()
            return success_json()
    result = db.api.coach.coach.add_coach_comment(
            coach_id, comment, 10, user.id, username,
            str(user.avatar_url), career_id, None)
    if result.is_error():
        return failed_json(u'服务器开小差了，请稍后再试', code=500)
    comment_id = result.result()
    add_project_coach_teacher_backlog(user, teacher['id'], career_id, abstract, coach_id, comment_id,
                                      send_type=SendSmsAndMessage.BOTH_SMS_AND_MESSAGE)

    if user_task_record.status == 'FAIL':
        user_task_record.status = 'REDOING'
        user_task_record.save()
    return success_json()
