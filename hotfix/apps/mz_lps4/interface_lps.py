# -*- coding: utf-8 -*-
import os

import db.api.course.course_task

import datetime
from django.db import transaction
from django.shortcuts import get_object_or_404

from mz_lps.models import ProjectRecord
from mz_lps3.models import UserTaskRecord, StageTaskRelation
from mz_lps3.views_student import student_month_salary
from mz_user.functions import is_basic_info_completed_lps4, is_job_intention_info_completed, is_completed_study_info
from mz_user.models import UserJobInfo
from mz_usercenter.student.interface_job_info import get_job_info_by_class_student
from utils.logger import logger as log
from mz_lps3.functions_nj import StageTaskInterface
import db.api.lps.student
import db.api.lps.lps_index

TASK_TYPE_NORMAL = StageTaskRelation.STAGE_TASK_TYPE_NORMAL


def lps4_task_map(class_id, user_id):
    """
    在班的任务地图
    :param class_id:
    :return:
    """
    st_interface = StageTaskInterface(class_id)
    stages = st_interface.get_student_data(user_id)
    current_task = st_interface.get_student_latest_task(user_id)
    current_task_rid = current_task.task_rid if current_task else None
    is_just_begging = st_interface.is_just_beginning(user_id)
    the_first_task = st_interface.get_the_first_task(user_id)

    data = dict(
        stages=stages,
        current_task=current_task,
        current_task_rid=current_task_rid,
        is_just_begging=is_just_begging,
        the_first_task=the_first_task
    )

    return data


def lps4_public(career_id):
    """
    lps面板公共信息
    :param career_id:
    :return:
    """
    px = db.api.lps.lps_index.get_lps_3_1_career_info(career_id)
    if px.is_error():
        log.warn('get_lps_3_1_career_info is error. user_id: %s' % career_id)
        px = {}
    else:
        px = px.result()
    if px:
        px = px[0]

    return px


def lps4_data(user_id, class_id, career_id):
    """
    lps4总体数据
    :param user_id:
    :param class_id:
    :param career_id:
    :return:
    """
    try:
        user_id = int(user_id)
        class_id = int(class_id)
        career_id = int(career_id)
    except ValueError:
        return {}
    if user_id <= 0 or class_id <= 0 or career_id <= 0:
        return {}

    # 取lps相关数据
    task_data = lps4_task_map(class_id, user_id)

    return task_data


def lps4_get_try_class_id(career_id):
    """
    lps3.1获取免费班级，如果没有就创建
    :param career_id:
    :return:
    """
    try_class_id = db.api.lps.student.get_lps_3_1_experience_class_id_by_career_id(career_id)
    if try_class_id.is_error():
        log.warn('get_lps_3_1_experience_class_id_by_career_id is error. career_id: %s' % career_id)
        try_class_id = ()
    else:
        try_class_id = try_class_id.result()

    if try_class_id:
        try_class_id = try_class_id[0]['id']
    else:
        # 找到career_course的short_name
        career = db.api.lps.lps_index.get_lps_3_1_career_info(career_id)
        try_class_id = 0
        if career.is_error():
            log.warn('get_career_by_career_id is error. career_id: %s' % career_id)
        else:
            career = career.result()
        if career:
            short_name = career[0]['short_name']
            date = datetime.datetime.now()
            try_class_id = db.api.lps.student.create_lps_3_1_experience_class_id_by_career_id(career_id, short_name, date)
            if try_class_id.is_error():
                log.warn('create_lps_3_1_experience_class_id_by_career_id is error. career_id: %s' % career_id)
                try_class_id = 0
            else:
                try_class_id = try_class_id.result()

    return try_class_id

@transaction.commit_on_success
def lps4_change_rebuild_to_rebuilding(class_id, stagetask_id, user_id):
    """
    删除ProjectRecord，把任务状态变为rebuilding
    :param class_id:
    :param stagetask_id:
    :param user_id:
    :return:
    """
    usertask = get_object_or_404(UserTaskRecord, class_id=class_id, student_id=user_id, stage_task_id=stagetask_id)
    user_project = ProjectRecord.objects.filter(
        project_id=usertask.stage_task.task.project_id,
        student_id=user_id
    )
    usertask.status = "REDOING"
    usertask.save()

    if user_project:
        user_project[0].delete()


def get_free_task_id_by_class_id(class_id):
    """
    根据class_id取该专业的免费任务球id
    :param class_id:
    :return:
    """
    free_task_ids = []
    stages = StageTaskInterface.get_real_stage_tasks_by_class_id(class_id)
    for stage in stages:
        for task in stage['tasks']:
            if task['task_type'] != TASK_TYPE_NORMAL:
                free_task_ids.append(task['task_id'])
    return free_task_ids


def get_lps_3_1_careers_by_user_id_interface(user_id):
    """
    取该生所有报班的专业
    :param user_id:
    :return:
    """
    careers = db.api.lps.student.get_lps_3_1_careers_by_user_id(user_id)
    if careers.is_error():
        log.warn('get_lps_3_1_class_ids_by_user_id is error. user_id: %s' % user_id)
        careers = ()
    else:
        careers = list(careers.result())

    return careers


def get_career_course_knowledge_task_count_interface(career_id):
    """
    支付信息
    :param career_id:
    :return:
    """
    lps_count = db.api.course.course_task.get_career_course_knowledge_task_count(career_id)

    if lps_count.is_error():
        log.warn('get_career_course_knowledge_task_count is error. career_id: %s' % career_id)
        lps_count = {}
    else:
        lps_count = lps_count.result()

    return lps_count

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


def authenticate_user_info_interface(user_id, career_id):
    """
    取该生所有报班的专业
    :return:
    """
    careers = db.api.lps.student.get_lps_3_1_careers_by_user_id(user_id)
    if careers.is_error():
        log.warn('get_lps_3_1_class_ids_by_user_id is error. user_id: %s' % user_id)
        careers = ()
    else:
        careers = list(careers.result())

    lps_count = db.api.course.course_task.get_career_course_knowledge_task_count(career_id)

    if lps_count.is_error():
        log.warn('get_lps_3_1_class_ids_by_user_id is error. user_id: %s' % user_id)
        lps_count = {}
    else:
        lps_count = lps_count.result()

    data = dict(
        careers=careers,
        lps_count=lps_count,
    )

    return data


def get_skill_radar_by_career_id_interface(career_id):
    """
    雷达图
    :param career_id:
    :return:
    """
    skill_radar = db.api.lps.lps_index.get_skill_radar_by_career_id(career_id)
    if skill_radar.is_error():
        log.warn('get_skill_radar_by_career_id is error. career_id: %s' % career_id)
        skill_radar = ()
    else:
        skill_radar = skill_radar.result()

    return skill_radar


def get_skill_tree_by_class_id_career_id_user_id_interface(class_id, career_id, user_id, current_task_rid):
    """
    取技能树
    :param class_id:
    :param career_id:
    :param user_id:
    :return:
    """
    stage_tree_list = []
    stage_tree = db.api.lps.lps_index.get_skill_tree_by_class_id_career_id_user_id(class_id, career_id, user_id)
    if stage_tree.is_error():
        log.warn('get_skill_radar_by_career_id is error. career_id: %s' % user_id)
    else:
        stage_tree = stage_tree.result()
        if stage_tree:
            task_status_flag = False
            stage_status_flag = False
            last_stage_status_flag = False
            _last_stage_status_flag = False

            last_st = {}
            for st in stage_tree:
                tasks_dict = dict(
                    task_rid=st['str_id'],
                    task_name=st['title'],
                    task_status=st['status']
                )


                if st['status'] in ['PASS', 'DONE', 'FAIL', 'REDOING'] \
                        and (not last_st.has_key('status') or not last_st.get('status')) and task_status_flag is False:
                    task_status_flag = True

                if last_stage_status_flag:
                    _last_stage_status_flag = True

                if st['s_id'] == last_st.get('s_id', None):
                    stage_dict['tasks'].append(tasks_dict)
                else:
                    stage_dict = dict(
                        stage_name=st['stage_name'],
                        stage_is_current=False,
                        stage_is_finish=False,
                        last_stage_status_flag=False,
                        tasks=[tasks_dict]
                    )
                    if _last_stage_status_flag:
                        stage_dict['last_stage_status_flag'] = True
                    stage_tree_list.append(stage_dict)

                if task_status_flag:
                    stage_dict['stage_is_finish'] = True
                    tasks_dict['task_status'] = True
                    if stage_status_flag is False:
                        stage_dict['stage_is_current'] = True
                        stage_status_flag = True
                        last_stage_status_flag = True

                if st['status'] == 'DOING' and task_status_flag is False:
                    task_status_flag = True

                last_st = st

    return stage_tree_list


def get_lps_3_1_teacher_by_career_id_interface(career_id):
    """
    获取老师
    :param career_id:
    :return:
    """
    teacher = db.api.lps.student.get_lps_3_1_teacher_by_career_id(career_id)
    if teacher.is_error():
        log.warn('get_lps_3_1_teacher_by_career_id is error. career_id: %s' % career_id)
        teacher = None
    else:
        teacher = teacher.result()

    return teacher


def get_lps4_teacher_by_career_student_id_interface(career_id, student_id):
    """
    获取老师
    :param career_id:
    :param student_id
    :return:
    """
    teacher = db.api.lps.student.get_lps4_teacher_by_career_student_id(
        career_id, student_id)
    if teacher.is_error():
        log.warn('get_lps4_teacher_by_career_student_id_interface is error. '
                 'career_id: {0}, student_id: {1}'.format(career_id, student_id))
        teacher = None
    else:
        teacher = teacher.result()

    return teacher


def get_student_enter_data(class_student, student_type):
    """
    入学弹窗信息
    :param class_student: lps3的学生对象
    :param student_type: 学生报班类型
    :return:
    """
    user_id = class_student.user_id
    class_id = class_student.student_class_id
    # 是否补全学生信息
    is_user_info = is_basic_info_completed_lps4(class_student)
    is_student_study_info = is_completed_study_info(class_student)
    student_info = is_user_info and is_student_study_info
    # 是否补全就业信息
    # type是就业，且没有补全就业信息
    # 就业信息表单
    degrees = UserJobInfo.DEGREES.values()
    service_years = UserJobInfo.SERVICE_YEAR_CHOICES.values()
    is_job_intention_info = student_type == 1 \
                            and not is_job_intention_info_completed(user_id, class_id) \
                            and not class_student.is_view_employment_contract
    # 是否弹出就业协议
    is_view_employment_contract = student_type == 1 \
                                  and is_job_intention_info_completed(user_id, class_id) \
                                  and not class_student.is_view_employment_contract
    # 就业协议薪资
    intention_job_city = ''
    salary = 0
    degree = ''
    if not class_student.is_view_employment_contract:
        job_info = get_job_info_by_class_student(class_student)
        degree = job_info.get('degree')
        intention_job_city = job_info.get('intention_job_city')
        setattr(class_student, 'student_intention_city', intention_job_city)
        setattr(class_student, 'student_degree', degree)
        salary = student_month_salary(class_student, class_student.student_class.career_course.name)
    # 是否弹出不需要就业的服务
    is_view_not_employment_contract = student_type == 0 \
                                      and not class_student.is_view_not_employment_contract

    return dict(
        student_info=student_info,
        is_user_info=is_user_info,
        degree=degree,
        degrees=degrees,
        service_years=service_years,
        is_job_intention_info=is_job_intention_info,
        is_view_employment_contract=is_view_employment_contract,
        intention_job_city=intention_job_city,
        salary=salary,
        is_view_not_employment_contract=is_view_not_employment_contract,
    )


def get_lps_3_1_career_info_list_interface(career_id):
    """
    取当前职业课程
    :param career_id:
    :return:
    """
    this_career = db.api.lps.lps_index.get_lps_3_1_career_info(career_id)
    if this_career.is_error():
        log.warn('get_career_by_career_id is error. career_id: %s' % career_id)
        this_career = []
    else:
        this_career = this_career.result()
    if this_career:
        this_career = list(this_career)
    else:
        this_career = []

    return this_career

