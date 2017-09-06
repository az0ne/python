# -*- coding: utf-8 -*-
import datetime, urllib

from django.http.response import HttpResponse, Http404

import db.api.onevone.meeting
import db.api.onevone.ops
import db.api.onevone.study_service
import db.api.lps.lps_index
from django.shortcuts import render, get_object_or_404
from mz_common.decorators import student_required
from mz_lps4.context import get_lps4_context
from mz_lps4.interface import serialize_onevone_meeting_date, get_onevone_meeting, get_student_meeting_list_interface
from mz_lps4.interface_lps import get_lps4_student_info_by_user_id_interface
from mz_usercenter.teacher.interface import serialize_onevone_meeting
from utils.is_logined import student_in_career_required
from utils.logger import logger as log
from utils.sensitive_word import sensitive_word
from utils.tool import get_param_by_request
from core.common.http.response import failed_json, success_json
from mz_user.interface import UserBaseInterface
from mz_common.models import MobileVerifyRecord
from django.db.models import Q
from mz_common.function_discuss import img_upload
from utils.sms_manager import send_sms, get_templates_id, send_sms_new
from django.conf import settings

from mz_lps.models import ClassStudents
from mz_usercenter.student.interface_job_info import get_job_info_by_class_student
from mz_lps3.views_student import student_month_salary
from website.api.user.decorators import app_user_required


@student_required
def send_mobile_captcha_from_onevone_meeting(request):
    """
    手机发送短信,用于1v1直播
    :param request:
    :return:
    """
    # 手机校验
    mobile = get_param_by_request(request.POST, "mobile", "", str)
    if not mobile:
        return failed_json(u'请输入手机号')

    ip = request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR']
    flags, msg = UserBaseInterface.can_send_sms(mobile, ip)
    if not flags:
        return failed_json(msg)

    # 发送短信
    UserBaseInterface.send_check_mobile(mobile, ip, mobile_type=3)  # 3.1v1直播预约

    return success_json()


@student_required
def order_onevone_meeting(request):
    """
    验证手机验证码
    :param request:
    :return:
    """
    mobile = get_param_by_request(request.POST, "mobile", "", str)
    mobile_code = get_param_by_request(request.POST, "mobile_code", "", str)
    if not mobile_code:
        return failed_json(u'请输入验证码')

    record = MobileVerifyRecord.objects.filter(Q(mobile=mobile), Q(code=mobile_code), Q(type=3)).order_by("-created")
    if record:
        if datetime.datetime.now() - datetime.timedelta(minutes=30) > record[0].created:
            return failed_json(u'验证码已过期')
    else:
        return failed_json(u'验证码不正确')

    return success_json()


@student_required
def old_onevone_meeting_list(request, career_id):
    """
    往期1v1直播列表
    :param request:
    :param career_id:
    :return:
    """
    user_id = request.user.id
    result = db.api.onevone.meeting.show_onevone_meeting_list_by_user_id(user_id, career_id)

    if result.is_error():
        log.warn('show_onevone_meeting_list_by_user_id is error user_id:%s career_id:%s' % (user_id, career_id))
        old_meeting_list = []
    else:
        old_meeting_list = result.result()

    html = render(request, 'mz_lps4/module/ajax_meeting_prev_lists.html',
                  dict(old_onevone_meeting_list=old_meeting_list)).content
    return success_json(data=dict(html=html))


@student_required
def update_onevone_meeting(request, meeting_id):
    """
    更新1v1直播详情的问题内容
    :param request:
    :param meeting_id:
    :return:
    """
    user_id = request.user.id
    small_image_path = get_param_by_request(request.POST, "small_image_url", "", str)
    image_path = get_param_by_request(request.POST, "image_url", "", str)
    question = get_param_by_request(request.POST, "question", 0, str)
    if len(question.encode('gbk')) > 1000:
        return failed_json('输入超过1000字，请重新输入。')
    if len(question.encode('gbk')) < 15:
        return failed_json('输入少于15字，请重新输入。')
    result = db.api.onevone.meeting.add_onevone_meeting(meeting_id, user_id, small_image_path, image_path, question)
    if result.is_error():
        log.warn('add_onevone_meeting is error id:%s user_id:%s' % (meeting_id, user_id))
        ordered_status = False
    else:
        ordered_status = result.result()
    if not ordered_status:
        return failed_json(u'问题内容更新失败')

    return success_json()


@student_required
def onevone_meeting_success(request, meeting_id):
    """
    预约成功的提示框
    :param request:
    :param meeting_id:
    :return:
    """
    result = db.api.onevone.meeting.get_onevone_meeting_by_id(meeting_id)
    if result.is_error():
        log.warn('get_onevone_meeting_by_id is error meeting_id:%s' % meeting_id)
        return failed_json()
    onevone_meeting = result.result()
    flags = False
    if onevone_meeting['start_time']-datetime.datetime.now() < datetime.timedelta(minutes=10):
        flags = True
    html = render(request, 'mz_lps4/module/ajax_appointment_success.html',
                  dict(onevone_meeting=onevone_meeting, flags=flags)
                  ).content
    return success_json(data=dict(html=html))


@student_required
def onevone_meeting_join_info(request, meeting_id):
    """
    1v1直播加入地址
    :param request:
    :param meeting_id:
    :return:
    """
    result = db.api.onevone.meeting.get_onevone_meeting_by_id(meeting_id)
    if result.is_error():
        log.warn('get_onevone_meeting_by_id is error meeting_id:%s' % meeting_id)
        return failed_json()
    onevone_meeting = result.result()

    user_nick_name = onevone_meeting['user_real_name'] or onevone_meeting['user_nick_name']
    # 客户端加入地址(学生以助教的身份加入)
    values = {'nickname': user_nick_name, 'token': onevone_meeting['assistant_token']}
    join_url = onevone_meeting['teacher_url'] + '?' + urllib.urlencode(values)
    # web端加入地址
    values = {'nickname': user_nick_name, 'token': onevone_meeting['student_web_token']}
    web_join_url = onevone_meeting['student_url'] + '?' + urllib.urlencode(values)

    return success_json(data=dict(join_url=join_url, web_join_url=web_join_url))


@student_required
def img_upload_onevone_meeting(request):
    """
    1v1 预约图片上传
    :param request:
    :return:
    """

    imgfile = request.FILES.get('image')
    try:
        flag, result, small_result = img_upload(imgfile, image_px=(120, 120), bucket='1v1tmp')
        if flag:
            return success_json({'result': result, 'small_result': small_result})
        else:
            return failed_json({'result': result, 'small_result': small_result})
    except Exception, e:
        log.warn('img_upload_onevone_meeting except:%s' % e)
        return failed_json(u'上传失败,请稍后再试')


# 学生查看入学须知
@student_required
def student_admission_infor(request):
    return render(request, 'mz_lps4/agreement/Freshers.html', locals())


# 学生查看无需就业服务
@student_required
def student_not_employment_agreement(request):
    return render(request, 'mz_lps4/agreement/not_employment.html', locals())


# 学生查看就业协议
@student_required
def student_employment_agreement(request, class_id):
    class_student = get_object_or_404(ClassStudents, student_class_id=class_id, user_id=request.user.id)
    salary = 5000
    if not (class_student.employment_contract_time and class_student.salary):
        job_info = get_job_info_by_class_student(class_student)
        class_student.student_degree = job_info.get('degree')
        class_student.student_intention_city = job_info.get('intention_job_city')
        class_student.salary = student_month_salary(class_student,
                                                    class_student.student_class.career_course.name)

        if not class_student.employment_contract_time:
            class_student.employment_contract_time = class_student.created
        class_student.save()
    degree = class_student.student_degree
    intention_job_city = class_student.student_intention_city
    salary = class_student.salary
    contract_time = class_student.employment_contract_time
    return render(request, 'mz_lps4/agreement/agreement.html', locals())


# 短信验证并计入运营表
@student_required
def verify_mobile_and_insert_ops(request):
    user = request.user
    mobile = get_param_by_request(request.POST, "mobile", 0, int)
    mobile_code = get_param_by_request(request.POST, "mobile_code", 0, str)
    career_id = get_param_by_request(request.POST, "career_id", 0, int)
    source = get_param_by_request(request.POST, "source", 1, int)
    real_name = request.POST.get("username", None)
    is_work = get_param_by_request(request.POST, "status", 0, int)
    time_interval = get_param_by_request(request.POST, "advisor", 1, int)
    if not real_name:
        return failed_json(u'请输入姓名')
    if not mobile_code:
        return failed_json(u'请输入验证码')
    record = MobileVerifyRecord.objects.filter(Q(mobile=mobile), Q(code=mobile_code), Q(type=3)).order_by("-created")
    if record:
        if datetime.datetime.now() - datetime.timedelta(minutes=30) > record[0].created:
            return failed_json(u'验证码已过期')
    else:
        return failed_json(u'验证码不正确')
    if time_interval not in [1, 2, 3]:
        time_interval = 1
    if is_work not in [0, 1]:
        is_work = 0
    if user.real_name != real_name:
        user.real_name = real_name
        user.save()
    result = db.api.onevone.ops.create_onevone_ops(user.id, career_id, source, mobile, time_interval, is_work)
    if result.is_error():
        return failed_json(u'预约失败, 请稍后再试')
    mobiles = ['15283908245']
    time_interval_dict = {1: '午休', 2: '下午', 3: '下班'}
    content_sms = [real_name, time_interval_dict.get(time_interval, '午休')]
    for mobile in mobiles:
        send_sms_new(mobile, 'ops_notify', content_sms)
    log.info('ops_notify sms success!')
    return success_json()


@student_required
def is_exist_onevone_ops(request):
    """
    判断是否已经预约过运营部收集信息1v1
    :param request:
    :return:
    """
    user_id = request.user.id
    career_id = get_param_by_request(request.POST, "career_id", 0, int)
    source = get_param_by_request(request.POST, "source", 1, int)

    result = db.api.onevone.ops.is_exist_onevone_ops(request.user.id, career_id, source)
    if result.is_error():
        log.warn('is_exist_onevone_ops is error user_id:%s career_id:%s source=%s' % (user_id, career_id, source))
        return failed_json(u'服务错误，请稍后再试！')
    flags = result.result()
    if flags:
        return success_json(data={'is_exist': True})
    else:
        return success_json(data={'is_exist': False})


@student_required
def ajax_onevone_add_list_student(request, career_id):
    """
    学生端1v1班会列表
    :param request:
    :param career_id:
    :return:
    """
    user_id = request.user.id
    student_dict = get_lps4_student_info_by_user_id_interface(user_id, career_id)
    if student_dict:
        teacher_id = student_dict['teacher_id']
        date_list = dict(request.POST).get('datelist[]', [])
        time_list = dict(request.POST).get('timelist[]', [])
        if user_id and date_list and time_list and teacher_id:
            data = serialize_onevone_meeting(teacher_id, time_list, date_list, user_id)
            return HttpResponse(success_json(data), content_type='application/json')
    else:
        return HttpResponse(failed_json(u'未找到学生信息'), content_type='application/json')


@student_required
def ajax_onevone_datelist(request, career_id):
    """
    学生端1v1班会可预约日期列表
    :param request:
    :param career_id:
    :return:
    """
    user_id = request.user.id
    student_dict = get_lps4_student_info_by_user_id_interface(user_id, career_id)
    if student_dict:
        teacher_id = student_dict['teacher_id']
        if teacher_id:
            data = serialize_onevone_meeting_date(teacher_id)
            return HttpResponse(success_json({'data': data}), content_type='application/json')
    else:
        return HttpResponse(failed_json(u'未找到学生信息'), content_type='application/json')


@student_required
def ajax_date_onovone_meeting(request, meeting_id):
    """
    预约1v1直播班会
    :param request:
    :param meeting_id:
    :return:
    """
    user_id = request.user.id
    mobile = get_param_by_request(request.POST, "mobile", "", str)
    career_id = get_param_by_request(request.POST, "career_id", 0, int)
    content = get_param_by_request(request.POST, "content", "", str)

    result = db.api.onevone.meeting.is_ordered_onevone_meeting(meeting_id)
    if result.is_error():
        log.warn('is_ordered_onevone_meeting is error id:%s' % meeting_id)
        is_ordered = False
    else:
        is_ordered = result.result()
    if is_ordered:
        return failed_json(u'你选择的时间已被预约，请重新选择时间', data=dict(type=True))

    if not(user_id and mobile and career_id and content and meeting_id):
        return failed_json(u'信息不全，预约失败', data=dict(type=True))
    else:
        result = db.api.onevone.meeting.order_onevone_meeting(meeting_id, career_id, user_id, mobile, content)
        if result.is_error():
            log.warn('is_ordered_onevone_meeting is error id:%s' % meeting_id)
            ordered_status = False
        else:
            ordered_status = result.result()
        if not ordered_status:
            return failed_json(u'直播课预约失败', data=dict(type=True))

        result = db.api.onevone.meeting.get_onevone_meeting_by_id(meeting_id)
        if result.is_error():
            log.warn('get_onevone_meeting_by_id is error meeting_id:%s' % meeting_id)
            return failed_json(u'直播课预约信息获取失败')
        onevone_meeting = result.result()
        # 预约成功短信(开始前30以上预约成功才发送)
        now = datetime.datetime.now()
        start_time = onevone_meeting.get('start_time', now)
        end_time = onevone_meeting.get('end_time', now)
        if datetime.datetime.now() + datetime.timedelta(minutes=30) <= start_time:
            teacher_name = onevone_meeting.get('teacher_real_name') or onevone_meeting.get('teacher_nick_name')
            start_date = start_time.strftime('%Y年%m月%d日')
            time_range = start_time.strftime('%H:%M')+'-'+end_time.strftime('%H:%M')
            send_sms(settings.SMS_APIKEY, get_templates_id('onevone_meeting_ordered'), mobile,
                     teacher_name, start_date, time_range)

        return success_json()


@student_required
def student_onevone_meeting_list(request, career_id):
    """
    学生 会议列表 与 详情
    :param request:
    :param career_id:
    :return:
    """
    student = request.user
    # 老师信息
    result = db.api.onevone.study_service.get_service_teacher(career_id=career_id)
    if result.is_error():
        raise Http404
    teachers = result.result()

    # 顶部职业课程信息
    result = db.api.onevone.study_service.get_lps4_student_career(user_id=student.id)
    if result.is_error() or not result.result():
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
        return render(request, 'mz_lps4/one_to_one_detail.html', {'career_id': int(career_id),
                                                                  'careers': careers,
                                                                  'teachers': teachers,
                                                                  'onevone_meeting': onevone_meeting,
                                                                  },
                      context_instance=get_lps4_context(request, career_id))
    else:
        # 剩余预约次数
        result = db.api.onevone.meeting.get_onevone_meeting_user_count(student.id, career_id)
        if result.is_error():
            log.warn('get_onevone_meeting_user_count is error student_id:%s' % student.id)
            residue_count = 0
        else:
            residue_count = result.result()

        data = get_student_meeting_list_interface(career_id, student, True)

        return render(request, 'mz_lps4/one_to_one.html', {'data': data,
                                                           'career_id': int(career_id),
                                                           'careers': careers,
                                                           'teachers': teachers,
                                                           'residue_count': residue_count,
                                                           }, context_instance=get_lps4_context(request, career_id))


@app_user_required
def score_meeting(request):
    """
    班会打分
    :param request:
    :return:
    """
    meeting_id = request.POST.get('meeting_id')
    star = request.POST.get('score')
    suggest = request.POST.get('comment', '')

    try:
        student_in_career_required(request)
    except Exception as e:
        log.warn('student_in_career_required error.meeting_id: %s.%s.' % (meeting_id, str(e)))
        return failed_json(unicode(e))

    # 检查字数
    if len(suggest.encode('gbk')) > 1000:
        return failed_json(u'输入超过1000字，请重新输入')

    if suggest:
        # 检查敏感词
        result = sensitive_word.filter(suggest)
        if result == sensitive_word.SERVER_ERROR:
            return failed_json(u'提交失败, 请稍后再试')
        if result == sensitive_word.FAIL:
            return failed_json(u'含有不正当词汇')

    # 插入评价
    result = db.api.onevone.meeting.evaluate_meeting_by_meeting_id(meeting_id, star, suggest)
    if result.is_error():
        log.warn('evaluate_meeting_by_meeting_id error, meeting_id %s' % meeting_id)
        return failed_json(u'提交失败, 请稍后再试')
    return success_json()
