# coding: utf-8
__author__ = 'Administrator'
from django.conf import settings
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

import utils.tool
import utils.handle_exception
import utils.decorators
import db.api.apiutils
import db.api.common.onevone.career_teacher
from utils.logger import logger as log

URL = ''
@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def careerTeacherList(request):
    """
    :param
    :return
    """
    global URL
    URL = request.get_full_path()
    result_dict = {
        'message': '',
        'state': ''
    }

    _id = utils.tool.get_param_by_request(request.GET, 'id', 0, int)
    action = utils.tool.get_param_by_request(request.GET, 'action', '', str)

    if action == 'delete':
        careerTeacherDelete = db.api.common.onevone.career_teacher.career_teacher_delete(_id=_id)

        if careerTeacherDelete.is_error():
            log.warn(
                "careerTeacherDelete.is_error()"
                "id:{0}".format(_id)
            )
            result_dict['state'] = 'false'
            result_dict['message'] = 'delete error'
            return JsonResponse(result_dict)

        if not careerTeacherDelete.result():
            log.info(
                "careerTeacherDelete.result back None"
                "id:{0}".format(_id)
            )
            return render(request, 'mz_common/onevone/careerTeacher_list.html', result_dict)

        result_dict['state'] = 'success'
        result_dict['message'] = ''

        return JsonResponse(result_dict)

    careerTeacherList = db.api.common.onevone.career_teacher.career_teacher_list()

    if careerTeacherList.is_error():
        log.warn(
            """
            get careerTeacherList is_error
            """
        )
        return render(request, '404.html', {})
    if not careerTeacherList.result():
        log.info(
            """
            careerTeacherList result is None
            """
        )
        return render(request, '404.html', {})
    return render(request, 'mz_common/onevone/careerTeacher_list.html', {'careerTeacherList': careerTeacherList.result()})


@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def careerTeacherEdit(request):
    """
    :return edit page
    """
    _id = utils.tool.get_param_by_request(request.GET, 'id', 0, int)
    action = utils.tool.get_param_by_request(request.GET, 'action', '', str)
    careerList = db.api.common.onevone.career_teacher.career_list()
    careerTeacherDetail = db.api.common.onevone.career_teacher.careerTeacherDetail(_id=_id)

    if careerList.is_error():
        log.warn(
            """
            get careerList is_error
            """
        )
        return render(request, '404.html', {})
    if not careerList.result():
        log.info(
            """
            careerList result is None
            """
        )
        return render(request, '404.html', {})

    result_dict = {
        'action': action,
        'careerList': careerList.result(),
        'careerTeacherDetail': careerTeacherDetail.result()
    }

    return render(request, 'mz_common/onevone/careerTeacher_edit.html', result_dict)

@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def careerTeacherSave(request):
    """
    :param
    :return
    """
    def check_none(param):
        if param == 'None':
            return 'Null'
        else:
            return param

    careerTeacherSave = db.api.apiutils.APIResult()

    action = utils.tool.get_param_by_request(request.POST, 'action', '', str)
    _id = utils.tool.get_param_by_request(request.POST, 'id', 0, int)
    career_id = utils.tool.get_param_by_request(request.POST, 'career_id', 0, int)
    teacher_id = utils.tool.get_param_by_request(request.POST, 'teacher_id', 0, int)
    qq = utils.tool.get_param_by_request(request.POST, 'qq', '', str)
    qq_key = utils.tool.get_param_by_request(request.POST, 'qq_key', '', str)
    old_image_url = utils.tool.get_param_by_request(request.POST, 'old_image_url', '', str)
    image_file = request.FILES.get('qq_image_url', '')

    image_path = check_none(old_image_url)
    qq = check_none(qq)
    qq_key = check_none(qq_key)


    if image_file:
        image_path = utils.tool.upload(image_file, settings.UPLOAD_IMG_PATH)

    if action == 'update':
        careerTeacherSave = db.api.common.onevone.career_teacher.career_teacher_update(_id=_id,career_id=career_id,
                                                                                       teacher_id=teacher_id,
                                                                                       qq=qq,qq_key=qq_key,
                                                                                       qq_image_url=image_path)

    if action == 'add':
        careerTeacherSave = db.api.common.onevone.career_teacher.career_teacher_add(career_id=career_id,teacher_id=teacher_id,
                                                                                    qq=qq,qq_key=qq_key,
                                                                                    qq_image_url=image_path)

    if careerTeacherSave.is_error():
        log.warn(
            "careerTeacherSave is_error"
            "career_id:{0}"
            "teacher_id:{1}"
            "action:{2}"
            "image_path:{3}".format(career_id, teacher_id, action, image_path)
        )
        return render(request, '404.html', {})

    if not careerTeacherSave.result():
        log.info(
            "careerTeacherSave not result()"
            "career_id:{0}"
            "teacher_id:{1}"
            "action:{2}"
            "image_path:{3}".format(career_id, teacher_id, action, image_path)
        )
        return render(request, '404.html', {})

    return HttpResponseRedirect(utils.tool.get_correct_url(URL, reverse('mz_common:careerTeacher_list')))


@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def careerTeacherDelete(request):
    """
    :ajax request
    """
















