# -*- coding: utf-8 -*-

"""
@version: 2016/5/13 0013
@author: lewis
@contact: lewis@maiziedu.com
@file: interface_job_info.py
@time: 2016/5/13 0013 15:07
@note:  学生端-就业意向
"""
import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
# import django
#
# django.setup()
from mz_lps.models import Class, ClassStudents
from mz_user.models import UserJobInfo




def get_job_info_by_class_student(class_student):
    """
    获取就业信息,根据职业课程ID
    :param class_student:班级学生对象
    :return job_info={
        teacher_name:老师名字（utf8）
        edu_admin_name：教务名字（utf8)
        edu_admin_name：教务名字（utf8)
        join_date：加入时间（datebase)
        study_goal：学习目的（utf8)
        intention_job_city：意向就业城市（utf8)
        to_industry：想从事的行业（utf8)
        degree：学历（utf8)
        service_year：工作年限（utf8）
        position: 职位（utf8）
        graduate_institution:毕业院校（utf8）
        in_service:是否在职（utf8）
        industry:所在行业（utf8）
    }
    """
    job_info = dict()
    user_id = class_student.user_id
    cls = class_student.student_class
    career_course_id = class_student.student_class.career_course_id
    try:
        user_job_info = UserJobInfo.objects.get(user_id=user_id, career_course_id=career_course_id)
    except UserJobInfo.DoesNotExist:
        return job_info
    job_info['career_course_id'] = career_course_id  # 职业课程ID
    job_info['career_course_name'] = cls.career_course.name  # 职业课程名称
    job_info['teacher_name'] = cls.teacher_name
    job_info['edu_admin_name'] = cls.edu_admin.real_name \
        if cls.edu_admin.real_name else cls.edu_admin.nick_name  # 教务名字
    job_info['join_date'] = class_student.created  # 加入时间
    job_info['study_goal'] = get_study_goal(class_student.is_employment_contract)  # 学习目标
    job_info[
        'intention_job_city'] = user_job_info.intention_job_city if user_job_info.intention_job_city else ''  # 意向就业城市
    job_info['to_industry'] = user_job_info.to_industry if user_job_info.to_industry else ''  # 想从事的行业
    job_info['degree'] = UserJobInfo.DEGREES.get(user_job_info.degree, '')  # 学历
    job_info['service_year'] = UserJobInfo.SERVICE_YEAR_CHOICES.get(user_job_info.service_year)  # 工作年限
    job_info['position'] = user_job_info.position if user_job_info.position else ''  # 职位
    job_info['graduate_institution'] = user_job_info.graduate_institution  # 毕业院校
    job_info['in_service'] = UserJobInfo.IS_SERVICE_CHOICES.get(user_job_info.in_service)  # 是否在职
    job_info['industry'] = user_job_info.industry if user_job_info.industry else ''  # 所在行业
    return job_info


def get_job_info_list(user_id):
    """
    获取用户的所有就业信息
    :param user_id:用户ID
    :return job_infos=[{
        teacher_name:老师名字（utf8）
        edu_admin_name：教务名字（utf8)
        edu_admin_name：教务名字（utf8)
        join_date：加入时间（datebase)
        study_goal：学习目的（utf8)
        intention_job_city：意向就业城市（utf8)
        to_industry：想从事的行业（utf8)
        degree：学历（utf8)
        service_year：工作年限（utf8）
        position: 职位（utf8）
        graduate_institution:毕业院校（utf8）
        in_service:是否在职（utf8）
        industry:所在行业（utf8）
    }, {...}, ...]
    """
    job_info_list = list()
    class_students = ClassStudents.objects.filter(user_id=user_id, student_class__class_type=Class.CLASS_TYPE_NORMAL,
                                                  status=ClassStudents.STATUS_NORMAL)
    for class_student in class_students:
        job_info = get_job_info_by_class_student(class_student)
        if job_info:
            job_info_list.append(job_info)
    return job_info_list


def save_job_info_part(user_id, career_course_id, position=None, industry=None):
    """
    保存就业信息（部分）
    :param user_id:用户ID（int）
    :param career_course_id:职业课程ID(int)
    :param position:职位(utf8)
    :param industry:所在行业(utf8)
    :return Ture or False
    """
    try:
        job_info = UserJobInfo.objects.get(user_id=user_id, career_course_id=career_course_id)
    except UserJobInfo.DoesNotExist:
        return False, u'职业课程ID不匹配'
    if position:
        job_info.position = position
    if industry:
        job_info.industry = industry
    job_info.save()
    return True, u''


def get_study_goal(is_employment_contract):
    """
    获取就业目标
    :param is_employment_contract:是否需要就业（ClassStudent中的属性）
    :return str
    """
    if is_employment_contract == True:
        return u'就业'

    if is_employment_contract == False:
        return u'技能提升'

    if is_employment_contract == None:
        return u''
