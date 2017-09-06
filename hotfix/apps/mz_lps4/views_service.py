# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings

import db.api.lps.lps_index
import db.api.onevone.meeting
from mz_common.functions import paginater
from django.http.response import Http404

from mz_lps4.context import get_lps4_context
from mz_lps4.interface import get_onevone_meeting, get_onevone_meeting_range_by_user_id_interface
from utils.logger import logger
from django.shortcuts import render
from mz_common.decorators import teacher_required, student_required
import db.api.onevone.study_service
from core.common.http.response import success_json, failed_json
from db.cores.cache import cache
from utils.message_queue import mq_service
from utils.sms_manager import send_sms, get_templates_id
from utils.tool import strip_tags


@teacher_required
def teacher_service_list(request, career_id, student_id):
    """
    老师端 学生学习建议列表
    :param request:
    :param career_id: 职业课程id
    :param student_id: 学生id
    :return:
    """
    page = request.GET.get('page', 1)
    page_size = 6
    page_aroud = 2
    try:
        page = int(page)
    except ValueError:
        page = 1
    teacher_id = request.user.id
    result = db.api.onevone.study_service.check_into_service(career_id=career_id, teacher_id=teacher_id,
                                                             student_id=student_id)
    if result.is_error():
        raise Http404
    if not result.result():
        raise Http404
    result = db.api.onevone.study_service.get_user_name(user_id=student_id)
    if result.is_error():
        raise Http404
    user_name = result.result()['real_name'] or result.result()['nick_name']
    result = db.api.onevone.study_service.student_service_count(career_id=int(career_id), student_id=int(student_id),
                                                                teacher_id=int(teacher_id))
    if result.is_error():
        raise Http404
    if not result.result():
        total_count = 0
    else:
        total_count = result.result()['total_count']
    page_count_list, page_index, start_index, end_index = paginater(page, page_size, total_count,
                                                                    page_aroud)
    service_result = db.api.onevone.study_service.service_list(career_id=int(career_id),
                                                               student_id=int(student_id),
                                                               teacher_id=int(teacher_id),
                                                               start_index=start_index, end_index=end_index)
    if service_result.is_error():
        raise Http404
    data = service_result.result()
    for service in data:
        tmp = strip_tags(service['content'])
        service['content'] = '<p>%s</p>' % tmp
    # 清除新服务数目
    result = db.api.onevone.study_service.clean_new_service_count(
            career_id=career_id, user_id=student_id, teacher_id=teacher_id, user=request.user)
    if result.is_error():
        raise Http404
    return render(request, 'mz_usercenter/teacher/oneVone_service_list.html', {'user_name': user_name,
                                                                               'career_id': career_id,
                                                                               'teacher_id': teacher_id,
                                                                               'student_id': student_id,
                                                                               'page_count_list': page_count_list,
                                                                               'page_index': page_index,
                                                                               'data': data})


@teacher_required
def teacher_create_new_service(request, career_id, student_id):
    """
    老师新建学习建议
    :param request:
    :param career_id:
    :param student_id:
    :return:
    """
    teacher = request.user
    result = db.api.onevone.study_service.check_into_service(
            career_id=career_id, teacher_id=teacher.id, student_id=student_id)
    if result.is_error():
        raise Http404
    if not result.result():
        raise Http404

    if request.method == 'GET':
        result = db.api.onevone.study_service.get_user_name(
                user_id=student_id)
        if result.is_error():
            raise Http404
        teacher_id = teacher.id
        student_name = result.result()['real_name'] or result.result()['nick_name']
        return render(request, 'mz_usercenter/teacher/oneVone_service_create.html', locals())
    if request.method == 'POST':
        # 保存学习建议
        content = request.POST.get('content')
        if not content:
            return failed_json(u'内容不能为空')
        teacher_name = teacher.real_name or teacher.nick_name
        data = {'career_id': career_id, 'student_id': student_id, 'teacher_id': teacher.id,
                'teacher_nick_name': teacher_name,
                'teacher_avatar_url': str(teacher.avatar_url),
                'now': datetime.datetime.now(), 'source_type': 1, 'source': None,
                'content': content, 'user_id': teacher.id, 'user_nick_name': teacher_name,
                'user_avatar_url': str(teacher.avatar_url), 'teacher_unread': 0,
                'student_unread': 1, 'is_student': False}
        result = db.api.onevone.study_service.create_new_service(**data)
        if result.is_error():
            return failed_json(u'服务器错误, 请稍后再试')
        return success_json()


@login_required
def onevone_service_detail(request, service_id):
    """
    老师学生学习建议详情
    :param request:
    :param service_id:
    :return:
    """
    is_mq = False

    user = request.user
    is_student = user.is_student()
    result = db.api.onevone.study_service.get_service_detail_and_count(service_id=service_id)

    if result.is_error():
        raise Http404
    service = result.result()['service']
    if not service:
        raise Http404
    total_count = result.result()['total_count']
    if is_student:
        if user.id != service['user_id']:
            raise Http404
    else:
        if user.id != service['teacher_id']:
            raise Http404

    if request.method == 'GET':
        # 分页
        page = request.GET.get('page', 1)
        page_size = 10
        page_aroud = 2
        try:
            page = int(page)
        except ValueError:
            page = 1
        page_count_list, page_index, start_index, end_index = paginater(page, page_size, total_count,
                                                                        page_aroud)
        result = db.api.onevone.study_service.one_to_one_service_detail(service_id=service_id,
                                                                        start_index=start_index, end_index=end_index)
        if result.is_error():
            raise Http404
        comments = result.result()
        # 清除相应未读数目
        result = db.api.onevone.study_service.clean_service_message_count(service=service, user=request.user)
        if result.is_error():
            raise Http404
        if is_student:
            # 顶部职业课程信息
            result = db.api.onevone.study_service.get_lps4_student_career(user_id=user.id)
            if result.is_error():
                raise Http404
            if not result.result():
                raise Http404
            careers = []
            for career in result.result():
                result = db.api.lps.lps_index.get_lps_3_1_career_info(career['career_id'])
                if result.is_error():
                    raise Http404
                careers.append(result.result()[0])

            result = db.api.onevone.study_service.get_service_teacher(career_id=service['career_id'])
            if result.is_error():
                raise Http404
            teachers = result.result()
            return render(request, 'mz_lps4/one_to_one_detail.html', {'tab': '1v1',
                                                                      'user_id': user.id,
                                                                      'career_id': service['career_id'],
                                                                      'comments': comments,
                                                                      'service': service,
                                                                      'service_id': service_id,
                                                                      'careers': careers,
                                                                      'teachers': teachers,
                                                                      'page_count_list': page_count_list,
                                                                      'page_index': page_index,
                                                                      },
                          context_instance=get_lps4_context(request, service['career_id']))
        else:
            result = db.api.onevone.study_service.get_user_name(user_id=service['user_id'])
            if result.is_error():
                raise Http404
            student_name = result.result()['real_name'] or result.result()['nick_name']
            return render(request, 'mz_usercenter/teacher/oneVone_service_detail.html',
                          {'comments': comments,
                           'service': service,
                           'service_id': service_id,
                           'page_count_list': page_count_list,
                           'page_index': page_index,
                           'student_name': student_name})

    if request.method == 'POST':
        content = request.POST.get('content')
        if not is_student:
            try:
                result = db.api.onevone.study_service.get_first_onevone_service_by_teacher_and_student(
                    service['teacher_id'], service['user_id'], service['source_type'], service['career_id'])
                if result.is_error():
                    logger.warn('get_first_onevone_service_by_teacher_and_student error')
                else:
                    new_service_id = result.result().get('id', 0)
                    if new_service_id == int(service_id):
                        result = db.api.onevone.study_service. \
                            get_onevone_service_comment(service_id, service['teacher_id'])
                        if result.is_error():
                            logger.warn('get_onevone_service_comment error')
                        elif not result.result():
                            is_mq = True
            except Exception as e:
                logger.warn(str(e))

        result = db.api.onevone.study_service.add_service_reply(service=service, user=user, content=content)
        if result.is_error():
            return failed_json(u'服务器错误, 请稍后再试')

        if is_student:
            # 老师超过五条未读发送短信
            result = db.api.onevone.study_service.get_user_name(user_id=service['teacher_id'])
            if not result.is_error():
                if result.result()['mobile']:
                    unread_data = db.api.onevone.study_service.get_teacher_total_unread_count(teacher_id=service['teacher_id'])
                    if not unread_data.is_error():
                        try:
                            if int(unread_data.result()[0]['total_count']) >= 5:
                                key = 'teacher_service_has_send_sms_%s_%s' % (service['teacher_id'], service['user_id'])
                                cache_data = cache.get(key)
                                if not cache_data:
                                    send_sms.delay(settings.SMS_APIKEY,
                                                   get_templates_id('onevone_service_teacher_unread'),
                                                   result.result()['mobile'].encode('utf8'))
                                    cache.set(key, True, 60 * 60 * 2)
                        except Exception, e:
                            print e
                            logger.error(e)
        else:
            # 老师回复 需要结束待办(学生发起的问题)
            if service['source_type'] == 0:
                if service['source']:
                    pass
                else:
                    try:
                        # 加入消息队列
                        if is_mq:
                            mq_data = mq_service.publish({
                                "event": "new_student_communicate_finish",
                                "data": {
                                    "user_id": str(service['user_id']),
                                    "career_id": str(service['career_id'])
                                }
                            })
                            logger.info('mq_new_student_communicate_finish: %s' % str(mq_data))
                    except Exception as e:
                        logger.warn(str(e))
        return success_json()


@student_required
def student_service_list(request, career_id):
    """
    学生 学习建议列表
    :param request:
    :param career_id:
    :return:
    """
    result = db.api.onevone.study_service.get_teacher_by_lps4(career_id=career_id, student_id=request.user.id)
    if result.is_error():
        raise Http404
    if not result.result():
        raise Http404
    teacher_id = result.result()['teacher_id']

    student = request.user
    result = db.api.onevone.study_service.get_service_teacher(career_id=career_id)
    if result.is_error():
        raise Http404
    teachers = result.result()
    # 清除学生未读服务数
    result = db.api.onevone.study_service.clean_new_service_count(career_id=career_id, teacher_id=teacher_id,
                                                                  user_id=request.user.id,
                                                                  user=request.user)
    if result.is_error():
        raise Http404
    # 顶部职业课程信息
    result = db.api.onevone.study_service.get_lps4_student_career(user_id=student.id)
    if result.is_error():
        raise Http404
    if not result.result():
        raise Http404
    careers = []
    for career in result.result():
        result = db.api.lps.lps_index.get_lps_3_1_career_info(career['career_id'])
        if result.is_error():
            raise Http404
        careers.append(result.result()[0])

    detail = request.GET.get('detail', 0)
    if detail:
        # 进1v1详情
        onevone_meeting = get_onevone_meeting(detail)
        status = request.GET.get('status', '')
        return render(request, 'mz_lps4/oto_online_detail.html', {'career_id': int(career_id),
                                                                  'careers': careers,
                                                                  'teachers': teachers,
                                                                  'onevone_meeting': onevone_meeting,
                                                                  'status': status,
                                                                  },
                      context_instance=get_lps4_context(request, career_id))
    else:
        m = request.GET.get('m', '')
        page = request.GET.get('page', 1)
        page_size = 10
        page_aroud = 2
        try:
            page = int(page)
        except ValueError:
            page = 1
        result = db.api.onevone.study_service.student_service_count(career_id=int(career_id),
                                                                    student_id=int(student.id),
                                                                    teacher_id=0)
        if result.is_error():
            raise Http404
        if not result.result():
            total_count = 0
        else:
            total_count = result.result()['total_count']
        page_count_list, page_index, start_index, end_index = paginater(page, page_size, total_count, page_aroud)
        data = db.api.onevone.study_service.service_list(career_id=int(career_id),
                                                         student_id=int(student.id),
                                                         teacher_id=0,
                                                         start_index=start_index, end_index=end_index)
        if data.is_error():
            raise Http404
        data = data.result()
        for service in data:
            tmp = strip_tags(service['content'])
            service['content'] = '<p>%s</p>' % tmp

        # 剩余预约次数
        result = db.api.onevone.meeting.get_onevone_meeting_user_count(student.id, career_id)
        if result.is_error():
            logger.warn('get_latest_onevone_meeting is error techer_id:%s' % teacher_id)
            residue_count = 0
        else:
            residue_count = result.result()

        start_time, end_time = get_onevone_meeting_range_by_user_id_interface(teacher_id, student.id)

        return render(request, 'mz_lps4/one_to_one.html', {'data': data,
                                                           'career_id': int(career_id),
                                                           'page_count_list': page_count_list,
                                                           'page_index': page_index,
                                                           'careers': careers,
                                                           'teachers': teachers,
                                                           'residue_count': residue_count,
                                                           'm': m,
                                                           'start_time': start_time,
                                                           'end_time': end_time
                                                           }, context_instance=get_lps4_context(request, career_id))


def score_service(request):
    """
    学习建议打分
    :param request:
    :return:
    """
    service_id = request.POST.get('service_id')
    star = request.POST.get('star')
    text = request.POST.get('suggest')
    if not (service_id and star and text):
        return failed_json(u'数据错误')
    result = db.api.onevone.study_service.get_service_detail_and_count(service_id=service_id)
    if result.is_error():
        return failed_json(u'服务器错误, 请稍后再试')
    service = result.result()['service']
    if not service:
        return failed_json(u'没有对应学习建议')
    if service['user_id'] != request.user.id:
        return failed_json(u'权限错误')
    result = db.api.onevone.study_service.update_service_score(service_id=service_id, star=star, suggest=text)
    if result.is_error():
        return failed_json(u'服务器错误, 请稍后再试')
    return success_json()
