# -*- coding: utf-8 -*-

import urllib
import urlparse
from mz_course.models import Institute
from mz_lps.models import Class
from mz_user.models import UserProfile, UserJobInfo, UserStudyGoal, UserProfessionalSkill
import logging
import random
import string
import qrcode
import os
import datetime

from mz_usercenter.student.interface_study import get_course_domain

INVITATION_CODE_LENGTH = 8
SHARE_LINK = '/user/get_invitation_link_page/'
logger = logging.getLogger('mz_user.functions')
from django.conf import settings

# if not os.path.isdir('%s/%s' % (settings.MEDIA_ROOT, settings.QC_FOLDER)):
#     os.mkdir('%s/%s' % (settings.MEDIA_ROOT, settings.QC_FOLDER))


def url_add_params(url, **params):
    """ 在网址中加入新参数 """
    pr = urlparse.urlparse(url)
    query = dict(urlparse.parse_qsl(pr.query))
    query.update(params)
    prlist = list(pr)
    prlist[4] = urllib.urlencode(query)
    return urlparse.ParseResult(*prlist).geturl()


def url_remove_params(url, *params):
    """ 在网址中删除新参数 """
    pr = urlparse.urlparse(url)
    query = dict(urlparse.parse_qsl(pr.query))
    for k in params:
        if k in query:
            del query[k]
    prlist = list(pr)
    prlist[4] = urllib.urlencode(query)
    return urlparse.ParseResult(*prlist).geturl()


def set_invitation_code(user_id):
    """
    generate invitation code for user_id
    :param user_id:
    :return: invitation code will be returned if success else None
    """
    assert isinstance(user_id, long)
    finish_flag = False
    while not finish_flag:  # generate code and check if already exists,
        code = ''.join(random.choice('%s%s' % (string.ascii_uppercase, string.digits)) for _ in
                       range(INVITATION_CODE_LENGTH))
        if not UserProfile.objects.filter(invitation_code=code).exists():
            finish_flag = True
    UserProfile.objects.filter(id=user_id).update(invitation_code=code)
    return code


def get_invitation_code(user_id):
    """
    get invitation code for user_id
    first get from db, if not exists will created one
    :param user_id:
    :return: invitation code ill be returned if success else None
    """
    assert isinstance(user_id, long)
    invitation_code = UserProfile.objects.values_list('invitation_code', flat=True).get(id=user_id)
    if not invitation_code:
        invitation_code = set_invitation_code(user_id)
        try:
            generate_qrcode_file(invitation_code)
        except IOError as msg:
            logger.error(msg)
    return invitation_code


def generate_qrcode_file(invitation_code):
    """
    生成二维码文件
    should be wrapped by block of try...except
    :param invitation_code:
    :return: True is operation success
    """
    with open('%s/%s%s.png' % (settings.MEDIA_ROOT, settings.QC_FOLDER, invitation_code), 'wb') as img:
        (qrcode.make('%s%s%s' % (settings.SITE_URL, SHARE_LINK, invitation_code))).save(img)
    return True


def get_qrcode_file_path(invitation_code):
    """

    :param invitation_code:
    :return:
    """
    return '%s%s%s.png' % (settings.MEDIA_URL, settings.QC_FOLDER, invitation_code)


def get_user_id_from_invitation_code(invitation_code):
    users = UserProfile.objects.filter(invitation_code=invitation_code)
    if (len(users) == 0):
        return -1
    user = users[0]
    return user.id


def is_invitation_code_available(invitation_code):
    if invitation_code == None:
        return False

    user_id = get_user_id_from_invitation_code(invitation_code)
    if (-1 == user_id):
        return False

    return True


def save_job_info(user_id, parameters_dict):
    """
    保存就业信息 update:lewis
    """
    class_id = int(parameters_dict['class_id'])
    career_course_id = Class.objects.xall().get(id=class_id).career_course.id
    job_info, _ = UserJobInfo.objects.get_or_create(user_id=user_id, career_course_id=career_course_id)
    # job_info.goal = int(parameters_dict['learningGoals']) - 1
    for k, v in UserJobInfo.DEGREES.iteritems():
        if v == parameters_dict['education']:
            job_info.degree = int(k)
    job_info.graduate_institution = parameters_dict['university']
    job_info.intention_job_city = parameters_dict['goCity']
    for k, v in UserJobInfo.SERVICE_YEAR_CHOICES.iteritems():
        if v == parameters_dict['WorkingLife']:
            job_info.service_year = int(k)
    job_info.in_service = int(parameters_dict['onthejob'])
    job_info.position = parameters_dict['position']
    job_info.industry = parameters_dict['industry']
    job_info.to_industry = parameters_dict['goIndustry']
    job_info.save()


def is_basic_info_completed(class_student):
    user = class_student.user
    if user.real_name and \
            user.gender and \
            user.birthday and \
            user.qq and \
            user.mobile:
        return True
    else:
        return False


def is_basic_info_completed_lps4(class_student):
    if class_student.is_employment_contract:
        # 对于就业学生 需要判断是否填写省份证号码
        user = class_student.user
        if user.real_name and \
                user.gender and \
                user.birthday and \
                user.qq and \
                user.mobile and \
                user.id_number:

            if not class_student.created:
                return True
            if class_student.created > datetime.datetime(2016, 12, 5, 18, 0, 0):
                if user.wechat:
                    return True
                else:
                    return False
            return True
        else:
            return False
    else:
        user = class_student.user
        if user.real_name and \
                user.gender and \
                user.birthday and \
                user.qq and \
                user.mobile:
            if not class_student.created:
                return True
            if class_student.created > datetime.datetime(2016, 12, 5, 18, 0, 0):
                if user.wechat:
                    return True
                else:
                    return False
            return True
        else:
            return False


# 学习目标学习基础加入入学必填流程, 为不影响老用户,用上线时间判断
def is_completed_study_info(class_student):
    if not class_student.created:
        return True
    if class_student.created > datetime.datetime(2016, 12, 5, 18, 0, 0):
        try:
            institute = Institute.objects.get(id=class_student.student_class.career_course.institute_id)
        except Institute.DoesNotExist:
            return True
        domain_name = get_course_domain(institute.name)
        if not UserProfessionalSkill.objects.filter(user=class_student.user, skill__domain=domain_name).exists():
            return False
    return True


# def is_study_info_completed(user_id, class_id):
#     career_course_id = Class.objects.xall().get(id=class_id).career_course.id
#     user_goals = UserStudyGoal.objects.filter(user_id=user_id,
#                                              career_course_id=career_course_id)
#     if not user_goals:
#         return True
#     return False

# def get_study_goal_info(user_id, class_id):
#     career_course_id = Class.objects.xall().get(id=class_id).career_course.id
#     user_goal = 0
#     user_goals = UserJobInfo.objects.filter(user_id=user_id,
#                                              career_course_id=career_course_id)
#     user_goal_name = ''
#     if user_goals:
#         user_goal = user_goals[0].goal + 1
#         user_goal_name = UserJobInfo.GOAL_CHOICES[user_goals[0].goal]
#
#     return user_goal, user_goal_name


def is_job_intention_info_completed(user_id, class_id):
    # student = UserProfile.objects.get(id=user_id)
    cls = Class.objects.xall().get(id=class_id)
    try:
        job_info = UserJobInfo.objects.get(user_id=user_id,
                                  career_course_id=cls.career_course_id)
    except UserJobInfo.DoesNotExist:
        return False

    if job_info.degree and \
            job_info.graduate_institution and \
            job_info.intention_job_city and \
            job_info.service_year and \
            job_info.in_service and \
            job_info.to_industry:
        return True
    return False
