# -*- coding: utf-8 -*-
import json
import db.api
from django.http.response import Http404, HttpResponse
from core.common.http.response import success_json, failed_json
from mz_lps.models import ClassStudents
from mz_lps3_free.student.interface_questionnaire import render_questionnaire, student_free_questionnaire_is_done, \
    free_student_can_quit_questionnaire, short_name_to_questionnaire_id
from utils.logger import logger as log
from db.api.lps import usertask as api_user_task
from mz_lps3.decorators import check_student_status


@check_student_status
def get_student_q_status(request, class_id, questionnaire_id):
    """
    问卷
    :param request:
    :param class_id:
    :param questionnaire_id:
    :return: success_json object or failed_json object
    """
    try:
        user_id = request.user.id
    except AttributeError as e:
        log.warn('request.user.id: ' + str(e))
        raise Http404

    # 根据questionnaire_id选择判断特定的"是否直接跳转的函数"
    if questionnaire_id == short_name_to_questionnaire_id('try_satis'):
        func = student_free_questionnaire_is_done
    elif questionnaire_id == short_name_to_questionnaire_id('why_quit'):
        func = free_student_can_quit_questionnaire
    else:
        return success_json()

    if func(class_id, user_id, questionnaire_id):
        return success_json()
    else:
        try:
            course_name = request.cclass.career_course.name
        except AttributeError as e:
            log.warn('request.cclass.career_course.name: ' + str(e))
            raise Http404
        form_div = render_questionnaire(questionnaire_id, course_name)
        return failed_json(data={'html': form_div})


def receive_questionnaire(request, class_id, questionnaire_id):
    """
    提交问卷
    :param request:
    :param class_id:
    :param questionnaire_id:
    :return:
    """
    try:
        questionnaire_record = request.POST
        student_id = request.user.id
    except AttributeError as e:
        log.warn(str(e))
        raise Http404

    if not isinstance(questionnaire_record, dict):
        log.warn("questionnaire_record is not a dict")
        raise Http404

    try:
        questionnaire_id = int(questionnaire_id)
        student_id = int(student_id)
        class_id = int(class_id)
    except ValueError:
        log.warn("questionnaire_id/student_id/class_id is not a int")
        raise Http404

    flag = True
    res = db.api.get_questionnaire_id_questionnaire_item(questionnaire_id)
    if res.is_error():
        log.warn("get_questionnaire_id_questionnaire_item is error")
        raise Http404
    qn = res.result()

    if qn:
        # 判断接收到的records的id是否正确
        if set(questionnaire_record.keys()) != set([str(q['id']) for q in qn]):
            flag = False

        if flag:
            # 判断student_id与class_id是否配对
            if ClassStudents.objects.filter(user_id=student_id, student_class_id=class_id).exists():
                # 组织插入的数据
                questionnaire_record = sorted(questionnaire_record.iteritems(), key=lambda x: x[0])
                qr_list = list()
                for qr in questionnaire_record:
                    qr = [student_id, class_id, questionnaire_id] + list(qr)
                    qr_list.append(tuple(qr))

                sub_res = db.api.submit_questionnaire(qr_list)
                if sub_res.is_error():
                    log.warn("submit_questionnaire is error")
                    raise Http404
                return HttpResponse(json.dumps({'msg': 'success'}), content_type="application/json")

        return HttpResponse(json.dumps({'data': u'请填完再提交'}), content_type="application/json")

    return HttpResponse(json.dumps({'msg': 'fail', 'data': u'提交失败'}), content_type="application/json")
