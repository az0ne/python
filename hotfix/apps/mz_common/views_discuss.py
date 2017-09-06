# -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from mz_common.decorators import student_required
from mz_common.function_discuss import img_upload as _img_upload
from core.common.http.response import success_json, failed_json
import db.api.common.new_discuss
import db.api.common.new_discuss_post
from mz_common.function_discuss import answer_post_api, question_post_api, get_one_question
from utils.logger import logger as log


@login_required
def view_get_one_question(request, discuss_id, last_id):
    """
    获取一个item及他的五条回答
    :return:
    """
    user_id = request.user.id
    try:
        discuss_id = int(discuss_id)
        last_id = int(last_id)
    except Exception as e:
        log.warn('get_one_questions, user: %s, %s' % (user_id, e))
        raise Http404

    result = db.api.common.new_discuss.get_problem_by_id(discuss_id, user_id)
    if result.is_error():
        log.warn('get_problem_by_id not data,problem_id is %s' % discuss_id)
        raise Http404
    question_dict = result.result()

    limit = 5
    try:
        answer_list = get_one_question(user_id, discuss_id, last_id, limit)
    except Exception, e:
        log.warn('function get_one_questions is error, user: %s, discuss_id:%s  %s' % (user_id, discuss_id, e))
        answer_list = []

    if last_id == 0:
        _template = 'mz_course/video_right_side/lesson_one_questions_item_div.html'
    else:
        _template = 'mz_course/video_right_side/lesson_one_questions_answer_div.html'

    html = render(request, _template, {'q': question_dict, 'answer_list': answer_list, 'last_id': last_id}).content
    if answer_list:
        return HttpResponse(json.dumps({'status': 'success', 'html': html, 'has_answer': True}))
    else:
        return HttpResponse(json.dumps({'status': 'failed', 'html': html, 'has_answer': False}))


@login_required
def get_all_questions(request, object_id, last_id):
    """
    获取一个item(以lesson_id/examine_id为标记)的所有问答
    :return:
    """
    user_id = request.user.id
    try:
        object_id = int(object_id)
        last_id = int(last_id)
    except Exception as e:
        log.warn('get_all_questions, user: %s, %s' % (user_id, e))
        raise e

    limit = 5
    questions = db.api.common.new_discuss_post.get_all_question_and_answer_of_one_project_id(object_id, limit, last_id)
    if questions.is_error():
        log.warn('get_all_question_and_answer_of_one_project_id is error. user_id: %s' % request.user.id)
        raise Http404
    else:
        questions = questions.result()

    if questions:
        html = render(request, 'mz_course/video_right_side/lesson_all_questions_item_div.html',
                      {'all_questions': questions, 'lesson_id': object_id}).content
        return HttpResponse(json.dumps({'status': 'success', 'html': html}))
    else:
        return HttpResponse(json.dumps({'status': 'failed'}))


@login_required
def get_all_questions_lps4(request, object_id, last_id, limit=20):
    """
    获取一个item(以lesson_id/examine_id为标记)的所有问答
    :return:
    """
    user_id = request.user.id
    try:
        object_id = int(object_id)
        last_id = int(last_id)
    except Exception as e:
        log.warn('get_all_questions, user: %s, %s' % (user_id, e))
        raise e

    questions = db.api.common.new_discuss_post.get_all_question_and_answer_of_one_project_id(
        object_id, limit, last_id)
    if questions.is_error():
        log.warn('get_all_question_and_answer_of_one_project_id is error. user_id: %s' % request.user.id)
        raise Http404
    else:
        questions = questions.result()

    if questions:
        html = render(request, 'mz_course/video_play/all_questions_item.html',
                      {'questions': questions, 'lesson_id': object_id}).content
        return HttpResponse(json.dumps({'status': 'success', 'html': html}))
    else:
        return HttpResponse(json.dumps({'status': 'failed'}))


@login_required
def get_my_questions(request, object_id, last_id):
    """
    获取一个item(以lesson_id/examine_id为标记)的我参加的问答
    :return:
    """
    user_id = request.user.id
    try:
        object_id = int(object_id)
        last_id = int(last_id)
    except Exception as e:
        log.warn('get_my_questions, user: %s, %s' % (user_id, e))
        raise e

    limit = 5
    user_id = request.user.id
    questions = db.api.common.new_discuss_post.get_my_question_and_answer_of_one_project_id(object_id, limit, user_id,
                                                                                            last_id)
    if questions.is_error():
        log.warn('get_my_question_and_answer_of_one_project_id is error. user_id: %s' % user_id)
        raise Http404
    else:
        questions = questions.result()

    if questions:
        html = render(request, 'mz_course/video_right_side/lesson_my_questions_item_div.html',
                      {'my_questions': questions, 'lesson_id': object_id}).content
        return HttpResponse(json.dumps({'status': 'success', 'html': html}))
    else:
        return HttpResponse(json.dumps({'status': 'failed'}))


@login_required
def get_my_questions_lps4(request, object_id, last_id, limit=20):
    """
    获取一个item(以lesson_id/examine_id为标记)的我参加的问答
    :return:
    """
    user_id = request.user.id
    try:
        object_id = int(object_id)
        last_id = int(last_id)
    except Exception as e:
        log.warn('get_my_questions, user: %s, %s' % (user_id, e))
        raise e

    user_id = request.user.id
    questions = db.api.common.new_discuss_post.get_my_question_and_answer_of_one_project_id(
        object_id, limit, user_id, last_id)

    if questions.is_error():
        log.warn('get_my_question_and_answer_of_one_project_id is error. user_id: %s' % user_id)
        raise Http404
    else:
        questions = questions.result()

    if questions:
        html = render(request, 'mz_course/video_play/all_questions_item.html',
                      {'questions': questions, 'lesson_id': object_id}).content
        return HttpResponse(json.dumps({'status': 'success', 'html': html}))
    else:
        return HttpResponse(json.dumps({'status': 'failed'}))


@login_required
def answer_post(request):
    """
    接收回复并存储
    :param request:
        object_id(lesson.id/examine.id) #
        object_type
        object_name
        object_content(视频的帧数) #
        comment #
        user_id #
        nick_name #
        head #
        create_date #
        group_name #

        parent_id
        problem_id
        weight
        # class_id, stage_task_id, item_id
    :return:
    """
    user = request.user
    _post = request.POST

    user_id = user.id
    nick_name = user.nick_name
    head = user.avatar_small_thumbnall

    comment = _post['comment']
    parent_id = _post['parent_id']
    problem_id = _post['problem_id']
    answer_user_id = _post['answer_user_id']
    answer_nick_name = _post['answer_nick_name']

    is_succeed, fail_msg, result = answer_post_api(user, comment, parent_id, problem_id,
                                                   answer_user_id, answer_nick_name)

    if is_succeed:
        new_discuss_id = result.get('new_discuss_id', 0)
        group_name = result.get('group_name', '')
        create_date = result.get('create_date', None)
        chance_left = result.get('chance_left', 0)

        data = dict(
            id=new_discuss_id,
            problem_id=problem_id,
            parent_id=parent_id,
            user_id=user_id,
            nick_name=nick_name,
            head=head,
            group_name=group_name,
            comment=comment,
            create_date=create_date,
        )

        html = render(request, 'mz_course/video_right_side/add_one_questions_answer_div.html', {'ca': data}).content

        return HttpResponse(json.dumps(
            {'status': 'success', 'chance_left': chance_left, 'html': html, 'parent_id': parent_id,
             'problem_id': problem_id}))
    else:
        return HttpResponse(json.dumps({'status': 'fail', 'msg': fail_msg}))


@login_required
def answer_post_lps4(request):
    """
    接收回复并存储
    :param request:
        object_id(lesson.id/examine.id) #
        object_type
        object_name
        object_content(视频的帧数) #
        comment #
        user_id #
        nick_name #
        head #
        create_date #
        group_name #

        parent_id
        problem_id
        weight
        # class_id, stage_task_id, item_id
    :return:
    """
    user = request.user
    _post = request.POST

    user_id = user.id
    nick_name = user.nick_name
    head = user.avatar_small_thumbnall

    comment = _post['comment']
    parent_id = _post['parent_id']
    problem_id = _post['problem_id']
    answer_user_id = _post['answer_user_id']
    answer_nick_name = _post['answer_nick_name']

    is_succeed, fail_msg, result = answer_post_api(user, comment, parent_id, problem_id,
                                                   answer_user_id, answer_nick_name)

    if is_succeed:
        new_discuss_id = result.get('new_discuss_id', 0)
        group_name = result.get('group_name', '')
        create_date = result.get('create_date', None)
        chance_left = result.get('chance_left', 0)

        data = dict(
            id=new_discuss_id,
            problem_id=problem_id,
            parent_id=parent_id,
            user_id=user_id,
            nick_name=nick_name,
            head=head,
            group_name=group_name,
            comment=comment,
            create_date=create_date,
            answer_user_id=answer_user_id,
            answer_nick_name=answer_nick_name
        )

        html = render(request, 'mz_course/video_play/add_answer_item.html', {'ca': data}).content

        return HttpResponse(json.dumps(
            {'status': 'success', 'chance_left': chance_left, 'html': html, 'parent_id': parent_id,
             'problem_id': problem_id}))
    else:
        return HttpResponse(json.dumps({'status': 'fail', 'msg': fail_msg}))


@student_required
def question_post(request):
    """
    接收提问并存储(lps3,lps4,学习面板)
    :param request:
    :return:
    """
    user = request.user
    _post = request.POST

    user_id = user.id
    nick_name = user.nick_name
    head = user.avatar_small_thumbnall

    discuss_location = _post.get('discuss_location', '')
    object_name = _post.get('object_name', '')
    object_id = _post.get('object_id', 0)
    comment = _post.get('comment', '')
    object_content = _post.get('object_content', '')
    material = dict(_post).get('material_arr[]', [])
    small_material = dict(_post).get('small_material_arr[]', [])
    # 提交数据
    try:
        is_succeed, fail_msg, result = question_post_api(discuss_location, object_name, object_id, user, comment,
                                                         object_content, material, small_material)
    except Exception, e:
        log.warn('question_post_api is error. user_id: %s, object_id:%s, msg:%s' % (user_id, object_id, str(e)))
        is_succeed, fail_msg = False, ''

    if is_succeed:
        new_discuss_id = result.get('new_discuss_id', 0)
        group_name = result.get('group_name', '')
        create_date = result.get('create_date', None)
        chance_left = result.get('chance_left', 0)

        data = dict(
            id=new_discuss_id,
            object_id=object_id,
            user_id=user_id,
            nick_name=nick_name,
            head=head,
            group_name=group_name,
            comment=comment,
            create_date=create_date,
            object_content=object_content,
            materials=material,
            small_materials=small_material
        )

        html = render(request, 'mz_course/video_right_side/add_questions_item_div.html', {'q': data}).content

        return HttpResponse(json.dumps(
            {'status': 'success', 'chance_left': chance_left, 'html': html}))
    else:
        return HttpResponse(json.dumps({'status': 'fail', 'msg': fail_msg}))


@student_required
def question_post_lps4(request):
    """
    接收提问并存储（课程播放页面改版）
    :param request:
    :return:
    """
    user = request.user
    _post = request.POST

    user_id = user.id
    nick_name = user.nick_name
    head = user.avatar_small_thumbnall

    discuss_location = _post.get('discuss_location', '')
    object_name = _post.get('object_name', '')
    object_id = _post.get('object_id', 0)
    comment = _post.get('comment', '')
    object_content = _post.get('object_content', '')
    material = dict(_post).get('material_arr[]', [])
    small_material = dict(_post).get('small_material_arr[]', [])
    # 提交数据
    try:
        is_succeed, fail_msg, result = question_post_api(discuss_location, object_name, object_id, user,
                                                         comment, object_content, material, small_material)
    except Exception, e:
        log.warn('question_post_api is error. user_id: %s, object_id:%s, msg:%s' % (user_id, object_id, str(e)))
        is_succeed, fail_msg = False, ''

    if is_succeed:
        new_discuss_id = result.get('new_discuss_id', 0)
        group_name = result.get('group_name', '')
        create_date = result.get('create_date', None)
        chance_left = result.get('chance_left', 0)

        data = dict(
            id=new_discuss_id,
            object_id=object_id,
            user_id=user_id,
            nick_name=nick_name,
            head=head,
            group_name=group_name,
            comment=comment,
            create_date=create_date,
            object_content=object_content,
            materials=zip(material, small_material),
            small_materials=small_material
        )

        html = render(request, 'mz_course/video_play/add_questions_item.html', {'q': data}).content

        return HttpResponse(json.dumps(
            {'status': 'success', 'chance_left': chance_left, 'html': html}))
    else:
        return HttpResponse(json.dumps({'status': 'fail', 'msg': fail_msg}))


@login_required
def img_upload(request):
    """
    上传图片
    :param request:
    :return:
    """
    imgfile = request.FILES.get('image')
    try:
        flag, result, small_result = _img_upload(imgfile)
        if flag:
            return success_json({'result': result, 'small_result': small_result})
        else:
            return failed_json({'result': result, 'small_result': small_result})
    except:
        return failed_json(u'上传失败,请稍后再试')

