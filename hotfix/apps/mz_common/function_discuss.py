# -*- coding: utf-8 -*-
import datetime
import StringIO
import json
from django.core.cache import cache

from core.common.upload.local import upload
import db.api.course.career_course
import db.api.common.new_discuss
import db.api.common.new_discuss_post
import db.api.user.user
import db.api.onevone.study_service
from utils.logger import logger as log
from mz_usercenter.base.interface import create_discuss_my_message
from django.conf import settings

try:
    from PIL import ImageFile, Image
except:
    import ImageFile, Image


def get_one_question(user_id, discuss_id, last_id=0, limit=5):
    answer_list = []
    try:
        user_id = int(user_id)
        discuss_id = int(discuss_id)
        last_id = int(last_id)
        limit = int(limit)
    except Exception as e:
        log.warn('_get_one_questions, user: %s, %s' % (user_id, e))
        raise e

    # 获取第一级回答
    first_answers = db.api.common.new_discuss_post.get_one_question_first_level_answer_of_one_project_id(
        discuss_id, limit, last_id)
    if first_answers.is_error():
        log.warn('get_one_question_first_level_answer_of_one_project_id is error. user_id: %s' % user_id)
        return answer_list
    else:
        first_answers = first_answers.result()

    id_list = []
    for a in first_answers:
        id_list.append(a['id'])

    # 获取第二级回答
    if id_list:
        second_answers = db.api.common.new_discuss_post.get_one_question_second_level_answer_of_one_project_id(id_list)
        if second_answers.is_error():
            log.warn('get_one_question_second_level_answer_of_one_project_id is error. user_id: %s' % user_id)
            return answer_list
        else:
            second_answers = second_answers.result()

        for i, fa in enumerate(first_answers):
            answer_list.append([fa, []])
            for sa in second_answers:
                if sa['parent_id'] == fa['id']:
                    answer_list[i][1].append(sa)

    # 更新用户状态为已读
    result = db.api.common.new_discuss.update_status(user_id, discuss_id, 2, 1)
    if result.is_error():
        log.warn('update_status is error. user_id: %s; discuss_id:%s; status:%s' % (user_id, discuss_id, 2))

    return answer_list


def answer_post_api(user, comment, parent_id, problem_id, answer_user_id, answer_nick_name):
    """
    接收回复并存储接口
    :param args:
    :return:
    """
    user_id = user.id
    nick_name = user.nick_name
    head = user.avatar_small_thumbnall
    fail_msg = ''
    result = {}
    if len(comment.encode('gbk')) > 1000:
        return False, u'输入超过1000字，请重新输入。',result

    # 取出问题的object相关属性
    question_info = db.api.common.new_discuss_post.get_question_info(problem_id)
    if question_info.is_error():
        log.warn('is_enterprise_student_or_teacher is error. user_id: %s' % user_id)
        return False, fail_msg, result
    question_info = question_info.result()
    if not question_info:
        return False, fail_msg, result
    object_id = question_info['object_id']
    object_content = question_info['object_content']
    object_location = question_info['object_location']
    object_name = question_info['object_name']
    object_type = question_info['object_type']
    problem_user_id = question_info['user_id']

    # 判断是企业直通班学生还是老师
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    group_name_student = db.api.common.new_discuss_post.is_enterprise_student(user_id, now)
    group_name_teacher = db.api.common.new_discuss_post.is_teacher(user_id)
    if group_name_student.is_error() or group_name_teacher.is_error():
        log.warn('is_enterprise_student_or_teacher is error. user_id: %s' % user_id)
        return False, fail_msg, result

    group_name = 'student' if group_name_student.result() else ''
    group_name = group_name or ('teacher' if group_name_teacher.result() else '')

    data = dict(
        object_id=object_id,
        object_type=object_type,
        object_content=object_content,
        object_name=object_name,
        object_location=object_location,
        comment=comment,
        user_id=user_id,
        nick_name=nick_name,
        head=head,
        create_date=now,
        parent_id=parent_id,
        group_name=group_name,
        weight=int(group_name == 'teacher'),
        problem_id=problem_id,
        answer_user_id=answer_user_id,
        answer_nick_name=answer_nick_name
    )

    # 回复接口
    _add_answer = db.api.common.new_discuss.add_answer(**data)
    if _add_answer.is_error():
        log.warn('_add_answer is error. user_id: %s' % user_id)
        return False, fail_msg, result
    new_discuss_id = _add_answer.result()

    result = dict(
        chance_left=-1,
        create_date=now,
        group_name=group_name,
        new_discuss_id=new_discuss_id
    )
    # 个人中心我的信息
    try:
        # 提问被回复
        if problem_id == parent_id:
            if problem_user_id != user_id:
                create_discuss_my_message(problem_user_id, nick_name, object_name, '21', new_discuss_id, problem_id,
                                          None)
        # 回复被回复
        else:
            if int(answer_user_id) != user_id:
                create_discuss_my_message(answer_user_id, '', object_name, '22', new_discuss_id, problem_id,
                                          problem_user_id)
    except Exception, e:
        log.warn('create_discuss_my_message fail new_discuss_id=%s, msg=%s' % (new_discuss_id, str(e)))

    # 更新用户状态为已读
    if group_name == 'teacher':
        update_status_result = db.api.common.new_discuss.update_status(user_id, problem_id, 3, 2)
        if update_status_result.is_error():
            log.warn('update_status is error. user_id: %s; discuss_id:%s; status:%s' % (user_id, problem_id, 3))

    return True, fail_msg, result


def question_post_api(discuss_location, object_name, object_id, user, comment, object_content,
                      material, small_material):
    """
    提问api
    :param discuss_location:
    :param object_id:
    :param comment:
    :param material:
    :return:
    """
    user_id = user.id
    nick_name = user.nick_name
    head = user.avatar_small_thumbnall
    fail_msg = ''
    result = {}
    if len(comment.encode('gbk')) > 1000:
        return False, u'输入超过1000字，请重新输入。', result
    # 对象相关属性
    object_type = 'LESSON'
    # 需要推送的老师对象

    discuss_location_list = []
    if discuss_location.find('_') > 0:
        discuss_location_list = discuss_location.split('_')
    # 来源lps3
    if len(discuss_location_list) == 3:
        # 提问的位置
        object_location = '{"lps":[%s]}' % ','.join(discuss_location_list)

    # 来源课程
    elif len(discuss_location_list) == 2:
        object_location = '{"course":[%s]}' % ','.join(discuss_location_list)
    else:
        return False, fail_msg, result

    # 判断提问者是企业直通班学生还是老师
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    group_name_student = db.api.common.new_discuss_post.is_enterprise_student(user_id, now)
    group_name_teacher = db.api.common.new_discuss_post.is_teacher(user_id)
    if group_name_student.is_error() or group_name_teacher.is_error():
        log.warn('is_enterprise_student_or_teacher is error. user_id: %s' % user_id)
        return False, fail_msg, result

    group_name = 'student' if group_name_student.result() else ''
    group_name = group_name or ('teacher' if group_name_teacher.result() else '')

    data = dict(
        object_id=object_id,
        object_type=object_type,
        object_content=object_content,
        object_name=object_name,
        object_location=object_location,
        comment=comment,
        user_id=user_id,
        nick_name=nick_name,
        head=head,
        create_date=now,
        parent_id=0,
        group_name=group_name,
        weight=int(group_name == 'teacher'),
        problem_id=0,
        answer_user_id=0,
        answer_nick_name='',
        material=material,
        small_material=small_material
    )

    _add_question = db.api.common.new_discuss_post.add_question(**data)
    if _add_question.is_error():
        log.warn('_add_answer is error. user_id: %s' % user_id)
        return False, fail_msg, result
    new_discuss_id = _add_question.result()

    result = dict(
        chance_left=-1,
        create_date=now,
        group_name=group_name,
        new_discuss_id=new_discuss_id,
    )

    return True, fail_msg, result


def get_questons(lesson_id, user_id, limit=5):
    """
    获取初始的全部和我的问答各5条
    :param lesson_id:
    :param user_id:
    :param limit:
    :return:
    """
    all_questions = db.api.common.new_discuss_post.get_all_question_and_answer_of_one_project_id(lesson_id, limit,
                                                                                                 luser_id=user_id)
    if all_questions.is_error():
        log.warn('get_all_question_and_answer_of_one_project_id is error. user_id: %s' % user_id)
        all_questions = []
    else:
        all_questions = all_questions.result()

    my_questions = db.api.common.new_discuss_post.get_my_question_and_answer_of_one_project_id(lesson_id, limit,
                                                                                               user_id)
    if my_questions.is_error():
        log.warn('get_my_question_and_answer_of_one_project_id is error. user_id: %s' % user_id)
        my_questions = []
    else:
        my_questions = my_questions.result()

    return all_questions, my_questions


def get_all_questions(lesson_id, user_id, limit=20):
    """
    获取问答列表
    :param lesson_id:
    :param user_id:
    :param limit:
    :return:
    """
    all_questions = db.api.common.new_discuss_post.get_all_question_and_answer_of_one_project_id(lesson_id, limit,
                                                                                                 luser_id=user_id)
    if all_questions.is_error():
        log.warn('get_all_question_and_answer_of_one_project_id is error. user_id: %s' % user_id)
        all_questions = []
    else:
        all_questions = all_questions.result()

    return all_questions


def img_upload(file_data, image_px=(180, 180), bucket='temp'):
    """
    头像原始文件上传
    :param file_data:
    :param image_px:
    :param bucket:
    :return:文件URL,,,不包括前面的MEDIA_URL
    """
    parser = ImageFile.Parser()
    data = file_data.read()
    parser.feed(data)
    img = parser.close()
    width, height = img.size

    if img.mode != "RGB":
        img = img.convert("RGB")

    # 图片裁剪
    if width >= height:
        left = (width - height) / 2
        upper = 0
        right = (width + height) / 2
        lower = height
    else:
        left = 0
        upper = (height - width) / 2
        right = width
        lower = (height + width) / 2

    region = (left, upper, right, lower)
    crop_img = img.crop(region)

    # 缩略图
    small_img = crop_img.resize(image_px, Image.ANTIALIAS)

    io = StringIO.StringIO()
    img.save(io, 'jpeg', quality=100)
    io.name = file_data.name
    io.seek(0)
    src_url = upload(io, bucket)
    del io

    small_io = StringIO.StringIO()
    small_img.save(small_io, 'jpeg', quality=100)
    small_io.name = file_data.name
    small_io.seek(0)
    small_src_url = upload(small_io, bucket)
    del small_io

    img = dict(img_url=settings.MEDIA_URL + src_url, width=width, height=height)
    crop_img = dict(img_url=settings.MEDIA_URL + small_src_url, width=180, height=180)

    return True, img, crop_img
