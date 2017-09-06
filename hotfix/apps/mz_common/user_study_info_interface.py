# coding: utf-8
import db.api.lps.classes
import db.api.lps.student
import db.api.common.new_discuss_post
import db.api.onevone.study_service
from utils.logger import logger as log


def get_class_and_student_info_by_user_id_and_class_id_interface(user_id, class_id):
    """
    取班级和学生信息接口
    :param user_id:
    :param career_id:
    :return:
    """
    student_dict = db.api.lps.classes.get_class_and_student_info_by_user_id_and_class_id(user_id, class_id)
    if student_dict.is_error():
        log.warn(
            'get_class_and_student_info_by_user_id_and_class_id is error. user_id: %s, career_id: %s' % (
                user_id, class_id))
        student_dict = {}
    else:
        student_dict = student_dict.result()

    return student_dict


def get_teachers_by_class_id_interface(class_id):
    """
    通过class_id获取老师接口
    :param class_id:
    :return:
    """
    teacher_result = db.api.common.new_discuss_post.get_teachers_by_class_id(class_id)
    if teacher_result.is_error():
        log.warn('get_teachers_by_class_id is error. class_id:%s' % class_id)
        teacher_result = []
    else:
        teacher_result = teacher_result.result()

    return teacher_result


def get_user_info_interface(id_list):
    """
    通过user_id获取用户信息接口
    :param user_id:
    :return:
    """
    user_info = db.api.lps.classes.get_user_info(id_list)
    if user_info.is_error():
        log.warn('get_user_info is error. user_id:%s' % id_list)
        user_info = []
    else:
        user_info = user_info.result()

    return user_info


def get_lps4_student_info_by_user_id_interface(user_id, career_id):
    """
    is student in lps4_student
    :param user_id:
    :param career_id:
    :return:
    """
    student_result = db.api.lps.student.get_lps4_student_info_by_user_id(user_id, career_id)
    if student_result.is_error():
        log.warn(
            'get_lps_3_1_class_id_by_user_id_and_career_id is error. user_id: %s, career_id: %s' % (
                user_id, career_id))
        student_dict = {}
    else:
        student_dict = student_result.result()

    return student_dict
