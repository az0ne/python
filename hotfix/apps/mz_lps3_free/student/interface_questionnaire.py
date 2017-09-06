# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from db.api.common.questionnaire import get_questionnaire_id_questionnaire_item
from django.http.response import Http404, JsonResponse
import db.api
from mz_lps.models import Class
from utils.logger import logger as log


def render_questionnaire(questionnaire_id, course_name=None):
    why_quit_questionnaire_id = short_name_to_questionnaire_id('why_quit')
    try_satis_questionnaire_id = short_name_to_questionnaire_id('try_satis')
    res = get_questionnaire_id_questionnaire_item(questionnaire_id)
    if res.is_error():
        log.warn("get_questionnaire_id_questionnaire_item is error")
        raise Http404
    qn = res.result()
    return render_to_string('mz_lps3_free/student/div_popup_wenjuan.html', locals())


def student_free_questionnaire_is_done(class_id, user_id, questionnaire_id):
    """
    判定学生是否做过免费试学满意度问卷
    :param class_id:
    :param user_id:
    :return:
    """
    rel = db.api.get_student_questionnaire_is_done(class_id, user_id, questionnaire_id)
    if rel.is_error():
        return False

    if rel.result():
        return True
    else:
        return False


def free_student_can_quit_questionnaire(class_id, user_id, questionnaire_id):
    """
    学生从学习页面返回到任务面板
    :param class_id:
    :return:
    """
    try:
        career_course_id = Class.objects.xall().get(id=class_id).career_course_id
    except:
        log.warn('get Class error')
        raise Http404
    tmp = db.api.get_free488_task_id(career_course_id)
    if tmp.is_error():
        log.warn('db.api.get_free488_task_id(career_course_id) is error')
        raise Http404
    task_id, stagetask_id = tmp.result()
    user_task_info = db.api.get_user_task_info(stagetask_id, class_id, user_id).result()

    rel = db.api.get_student_questionnaire_is_done(class_id, user_id, questionnaire_id)
    if rel.is_error():
        return False

    if user_task_info['status'] in ("DONE", 'PASS') or bool(rel.result()):
        return True

    return False


def short_name_to_questionnaire_id(short_name):
    """
    根据short_name找问卷id
    :param short_name:
    :return: {'id': id}
    """
    # 免费试学班在此页面点击返回的时候应该弹出问卷,问卷short_name为why_quit
    rel = db.api.get_short_name_questionnaire_id(short_name)
    if rel.is_error():
        raise Http404
    # 如果没查到数据,questionnaire的id为0
    questionnaire_id = '0'
    if rel.result():
        questionnaire_id = str(rel.result()[0].get('id', 0))

    return questionnaire_id
