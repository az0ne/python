#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from db.api.course import careerIntroduce as api_careerIntroduce
from db.api.course import careerIntroduceStudent as api_careerIntroduceStudent
from db.api.course import careerIntroduceTeacher as api_careerIntroduceTeacher
from db.api.course import careerIntroduceDuty as api_careerIntroduceDuty
from db.api.course import careerIntroduceEnterprise as api_careerIntroduceEnterprise
from db.api.apiutils import APIResult
from utils.decorators import dec_login_required
from utils import tool
from utils.logger import logger as log
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def career_introduce_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)

    career_introduce = APIResult()
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        career_introduce = api_careerIntroduce.delete_career_introduce(_id)
        if career_introduce.is_error():
            # 处理错误
            log.warn("delete career introduce by id failed!"
                     'career_introduce_id:{0}'.format(_id))
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect('/course/careerIntroduce/list/?action=query')

    if action == "query":
        career_introduce = api_careerIntroduce.list_career_introduce()

    if action == "search":
        if key_word == '%':  # 处理查询时，有%，搜索全部信息
            key_word1 = '\\' + key_word
        else:
            key_word1 = key_word
        career_introduce = api_careerIntroduce.list_career_introduce_by_name('%' + key_word1 + '%')

    if career_introduce.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"careerIntroduces": career_introduce.result(),
         "key_word": key_word}

    return render_to_response("mz_course/careerIntroduce/careerIntroduce_list.html", c,
                              context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def career_introduce_all_edit(request):
    """
    get career introduce all data,include teacher introduce,student introduce,duty introduce....
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)

    career_introduce = APIResult()
    if action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        career_introduce = api_careerIntroduce.get_career_introduce_by_id(_id)
        career_introduce_student = api_careerIntroduceStudent.list_career_page_student_by_career_id(_id)
        career_introduce_teacher = api_careerIntroduceTeacher.list_career_page_teacher_by_career_id(_id)
        career_introduce_duty = api_careerIntroduceDuty.list_career_page_duty_by_career_id(_id)
        career_introduce_enterprise = api_careerIntroduceEnterprise.list_career_page_enterprise_by_career_id(_id)

        if career_introduce.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"careerIntroduce": career_introduce.result()[0],
         "careerIntroduceStudents": career_introduce_student.result(),
         "careerIntroduceTeachers": career_introduce_teacher.result(),
         "careerIntroduceDuties": career_introduce_duty.result(),
         "careerIntroduceEnterprises": career_introduce_enterprise.result(),
         "action": action, "page_index": page_index}

    return render_to_response("mz_course/careerIntroduce/careerIntroduce_show.html", c,
                              context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def career_introduce_edit(request):
    """
    修改/添加页面跳转，并填充基本数据
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    field = tool.get_param_by_request(request.GET, 'field', '', str)

    career_introduce = APIResult()

    if "add" in action:
        c = {"action": action}

    if "edit" in action:
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        career_introduce = api_careerIntroduce.get_career_introduce_by_id(_id)
        c = {"careerIntroduce": career_introduce.result()[0], "action": action}
    if career_introduce.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    if "info" in field:
        return render_to_response("mz_course/careerIntroduce/careerIntroduce_info_edit.html", c,
                                  context_instance=RequestContext(request))
    elif "story" in field:
        return render_to_response("mz_course/careerIntroduce/careerIntroduce_story_edit.html", c,
                                  context_instance=RequestContext(request))
    elif "discuss" in field:
        return render_to_response("mz_course/careerIntroduce/careerIntroduce_discuss_edit.html", c,
                                  context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def career_introduce_info_save(request):
    """
    添加/修改职业课程中的基本介绍信息
    :param request:
    :return:重定向到《查看》职业课程页面
    """
    action = tool.get_param_by_request(request.POST, 'action', 'edit', str)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    name = tool.get_param_by_request(request.POST, 'name', '', str)
    img_url = request.FILES.get('img_url', '')
    old_image_path = tool.get_param_by_request(request.POST, 'old_image_path', '', str)
    short_info = tool.get_param_by_request(request.POST, 'short_info', "", str)
    info = tool.get_param_by_request(request.POST, 'info', "", str)
    student_count = tool.get_param_by_request(request.POST, 'student_count', 0, int)
    career_outline = tool.get_param_by_request(request.POST, 'career_outline', "", str)
    reason = tool.get_param_by_request(request.POST, 'reason', "", str)

    career_introduce = APIResult()
    image_path = old_image_path
    if img_url:
        # os.remove(os.path.join(settings.MEDIA_ROOT, old_image_path))  # 删除旧的图片
        image_path = tool.upload(img_url, settings.UPLOAD_IMG_PATH)
    if "add" in action:
        id1 = name.split('_')[0]
        name1 = name.split('_')[1]
        career_introduce = api_careerIntroduce.insert_career_introduce(id1, name1, image_path, short_info, info,
                                                                       student_count, career_outline, reason)
        if career_introduce.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/course/careerIntroduce/list/?action=query')
    if "edit" in action:
        career_introduce = api_careerIntroduce.update_career_introduce_info(_id, image_path, short_info, info,
                                                                            student_count, career_outline, reason)

        if career_introduce.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/course/careerIntroduce/edit/?action=show&id=' + str(_id))


@dec_login_required
@handle_http_response_exception(501)
def career_introduce_story_save(request):
    """
    添加/修改职业课程中的学员成功故事
    :param request:
    :return:重定向到《查看》职业课程页面
    """
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    story_info = tool.get_param_by_request(request.POST, 'story_info', "", str)
    story_name = tool.get_param_by_request(request.POST, 'story_name', "", str)
    story_title = tool.get_param_by_request(request.POST, 'story_title', "", str)
    story_img_url = request.FILES.get('story_img_url', "")
    old_image_path = tool.get_param_by_request(request.POST, 'old_image_path', "", str)
    story_video_url = tool.get_param_by_request(request.POST, 'story_video_url', "", str)

    image_path = old_image_path  # 如果更新数据时，未更改图片，image_url为空，设置图片的路径为老路径
    if story_img_url:
        image_path = tool.upload(story_img_url, settings.UPLOAD_IMG_PATH)

    career_introduce = api_careerIntroduce.update_career_introduce_story(_id, story_info, story_name, story_title,
                                                                         image_path, story_video_url)

    if career_introduce.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/course/careerIntroduce/edit/?action=show&id=' + str(_id))


@dec_login_required
@handle_http_response_exception(501)
def career_introduce_discuss_save(request):
    """
    添加/修改职业课程中的评论
    :param request:
    :return:重定向到《查看》职业课程页面
    """
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    discuss_id1 = tool.get_param_by_request(request.POST, 'discuss_id1', 0, int)
    discuss_id2 = tool.get_param_by_request(request.POST, 'discuss_id2', 0, int)
    discuss_id3 = tool.get_param_by_request(request.POST, 'discuss_id3', 0, int)

    career_introduce = api_careerIntroduce.update_career_introduce_discuss(_id, discuss_id1, discuss_id2, discuss_id3)

    if career_introduce.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/course/careerIntroduce/edit/?action=show&id=' + str(_id))

