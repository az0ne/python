# -*- coding: utf-8 -*-
"""
@version: 2016/3/29
@author: Jackie
@contact: jackie@maiziedu.com
@file: interface.py
@time: 2016/3/29 15:23
@note:  ??
"""
import datetime
from django.shortcuts import get_object_or_404
from core.common.http.response import success_json, failed_json
from mz_course.models import Lesson, CareerCourse
from mz_lps.models import Quiz, Paper, Project, ProjectImage, Class, ProjectRecord
from mz_lps3.functions_nj import StageTaskInterface
from mz_lps3.functions_zxdt import StudentTimedTest
from mz_lps3.models import KnowledgeItem, ClassRank
from django.conf import settings
from mz_lps4.class_dict import NORMAL_CLASS_DICT
from utils.logger import logger as log


def get_free_class(ccourse_id):
    """
    返回免费班
    :param ccourse_id:
    :return:
    """
    now = datetime.datetime.now()

    # 确定有无此专业
    try:
        short_name = CareerCourse.objects.get(id=ccourse_id).short_name
        coding = short_name.upper() + now.strftime('%Y%m%d')
    except CareerCourse.DoesNotExist:
        return failed_json(u'没有该专业')

    try:
        free_class = Class.objects.xall(). \
            get(class_type=Class.CLASS_TYPE_FREE, lps_version='3.0', career_course=ccourse_id)
    except Class.DoesNotExist:
        # 如果该专业没有免费班,创建之
        free_class = Class(student_limit=999999, is_active=1, status=1, meeting_enabled=0,
                           career_course_id=ccourse_id, lps_version="3.0", class_type=Class.CLASS_TYPE_FREE,
                           date_open=now, coding=coding)
        free_class.save()

    return free_class


def get_blank_task_map(free_class, _is_ios_check=False):
    """
    空任务地图
    :param free_class:
    :param _is_ios_check:
    :return:
    """
    class_id = free_class.id

    st_interface = StageTaskInterface(class_id)

    total = st_interface.count_all_tasks()  # 总任务数量
    stages = StageTaskInterface.get_stage_tasks_by_class_id(class_id)
    total_knowledge, done_knowledge, total_test_item, done_test_item = st_interface.count_knowledges()
    total_test_item += total

    stage_task_id = None

    # 组织数据
    stage_list = []
    for stage in stages:
        task_list = []
        for task in stage['tasks']:
            task_can_be_unlocked = False
            if stage_task_id == None:
                stage_task_id = task['rid']
                task_can_be_unlocked = True
            task_list.append(dict(
                stage_task_id=task['rid'],
                task_name=task['name'],  # 任务名称
                task_can_be_unlocked=task_can_be_unlocked,
            ))

        stage_list.append(dict(
            stage_name=stage['name'],
            task_list=task_list,
        ))

    data = dict(
        lps_version=4,
        careercourse_name=free_class.career_course.name,
        total=total,
        toal_knowledge=total_knowledge,
        toal_test_item=total_test_item,
        stage_list=stage_list,
        the_first_task=stage_task_id,
    )

    if _is_ios_check:
        data_ios_check = dict(
            class_id=0,
            rank_number=0,
            class_students_count=0,
            done=0,
            done_knowledge=0,
            done_test_item=0,
            is_just_beginning=1,
        )
        _data = data.copy()
        _data.update(data_ios_check)
        data = _data

    return success_json(data)


def get_student_task_map(class_student, student_id, _is_ios_check=False):
    """
    有班用户任务地图
    :param class_student:
    :param student_id:
    :param _is_ios_check:
    :return:
    """
    class_id = class_student.student_class_id
    sclass = class_student.student_class
    assert isinstance(sclass, Class)

    # 取任务数据
    st_interface = StageTaskInterface(class_id)

    stages = st_interface.get_student_data(student_id)
    current_task = st_interface.get_student_latest_task(student_id)  # 当前任务
    is_just_beginning = st_interface.is_just_beginning(student_id)  # 是否刚开始
    the_first_task = st_interface.get_the_first_task(student_id).task_rid  # 第一个任务

    # 如果班级号在NORMAL_CLASS_DICT里，班级和排名等数据全部不用取
    if class_id in NORMAL_CLASS_DICT.values():
        lps_version = 4
        total_knowledge, done_knowledge, total_test_item, done_test_item = 0, 0, 0, 0
        class_students_count, rank_number = 0, 0
        total, done = 0, 0
    else:
        lps_version = 3
        total = st_interface.count_all_tasks()  # 总任务数量
        done = st_interface.count_student_tasks_finished(student_id)  # 完成数量
        # 免费班级的task的PROJECT不计入test项,正常付费班级要计入
        # 免费班级不计算排名,正常付费班级要计算
        if st_interface._class_type == Class.CLASS_TYPE_FREE:
            _total, _done = 0, 0

            class_students_count, rank_number = -1, -1

            if _is_ios_check:
                class_students_count, rank_number = 30, 1

        else:
            _total, _done = total, done

            class_students_count = sclass.current_student_count  # 班级总人数
            last_class_rank = ClassRank.objects.filter(class_id=class_id, student_id=student_id).order_by('-id').first()
            rank_number = last_class_rank.rank if last_class_rank else 0  # 排名

        total_knowledge, done_knowledge, total_test_item, done_test_item = st_interface.count_knowledges(student_id)
        total_test_item += _total
        done_test_item += _done

    currenttask_need_share = False
    # 组织数据
    stage_list = []
    for stage in stages:
        task_list = []
        for task in stage.tasks:
            is_pass_timeout = False
            if task.is_pass:
                try:
                    is_pass_timeout = task._done_timeout
                except Exception:
                    log.info('user_task_record does not have done_time')
            task_detail = dict(
                stage_task_id=task.task_rid,
                task_name=task.task_name,  # 任务名称
                task_is_locked=task.is_locked,  # 是否锁定
                task_can_be_unlocked=task._can_be_unlocked or False,  # 是否可以解锁,针对锁定任务
                task_score=(task.score if hasattr(task, 'score') else '') or '',  # 分数
                task_progress=task.get_progress() if hasattr(task, 'student_id') else -1,  # 任务完成度
                task_timeout=is_pass_timeout or (task.is_doing and task.get_timeleft() <= 0),
                # 任务是否超时
                task_status=task.status or '',  # 用户任务状态
                is_focus=task.is_focus or False,  # 是否是焦点任务
            )
            task_list.append(task_detail)
            # 是否需要分享
            if st_interface._class_type == Class.CLASS_TYPE_FREE:
                if current_task:
                    if current_task.stage_task_id == task_detail['stage_task_id']:
                        if task_detail['task_progress'] == 100 and task_detail['task_status'] == 'DOING':
                            currenttask_need_share = True

        stage_list.append(dict(
            stage_name=stage.name,
            task_list=task_list,
        ))

    data = dict(
        careercourse_name=sclass.career_course.name,
        class_id=class_id,
        sclass_coding=sclass.coding,
        total=total,
        done=done,
        toal_knowledge=total_knowledge,
        done_knowledge=done_knowledge,
        toal_test_item=total_test_item,
        done_test_item=done_test_item,
        class_students_count=class_students_count,
        rank_number=rank_number,
        current_task=current_task.stage_task_id if current_task else -1,
        is_just_beginning=is_just_beginning,
        the_first_task=the_first_task,
        stage_list=stage_list,
        currenttask_need_share=currenttask_need_share,
        is_can_pay=sclass.career_course.is_class,
        lps_version=lps_version
    )

    return success_json(data)


def get_lesson_detail(user, useritem):
    """
    通过item找视频
    :param user:
    :param useritem:
    :return:
    """
    lesson = get_object_or_404(Lesson, pk=useritem.knowledge_item.obj_id)
    data = video_detail(user, lesson)
    data['useritem_id'] = useritem.id
    data['useritem_is_done'] = useritem.status == 'DONE'
    return success_json(data)


def video_detail(user, lesson):
    """
    视频详情
    :param user:
    :param lesson:
    :return:
    """
    course = lesson.course
    teacher = course.teacher

    data = dict(
        lesson_id=lesson.id,
        course_id=course.id,
        video_name=lesson.name,
        video_url=lesson.video_url,
        study_number=course.click_count,
        is_favorite=1 if user.myfavorite.filter(id=course.id).exists() else 0,
        teacher_info=dict(
            teacher_id=teacher.id,
            teacher_name=teacher.nick_name,
            teacher_avatar=settings.SITE_URL + settings.MEDIA_URL + teacher.avatar_small_thumbnall.url,
            teacher_description=teacher.description,
        )
    )
    return data


def start_exam(student_id, class_id, stagetask_id, item_id):
    """
    做测验
    :param student_id:
    :param class_id:
    :param stagetask_id:
    :param item_id:
    :return:
    """
    knowledgeitem = get_object_or_404(KnowledgeItem, id=item_id)
    paper_id = knowledgeitem.obj_id
    paper = Paper.objects.filter(examine_type=6, pk=paper_id)
    # 排除两种异常
    if not paper:
        return failed_json(u'还没有试卷,请联系带班老师')
    else:
        quizs = Quiz.objects.filter(paper=paper)
        if not quizs:
            return failed_json(u'试卷下没有题目,请联系带班老师')
        else:
            student_timed_test = StudentTimedTest(student_id, class_id, item_id, stagetask_id)
            _dict = student_timed_test.get_context()

            paper_completed_state = _dict['paper_completed_state']

            if paper_completed_state:
                accuracy_percent, false_quizs, correct_quizs, paper_details = \
                    _dict['accuracy_percent'], _dict['false_quizs'], _dict['correct_quizs'], _dict['completed_paper']

                paper_detail = list()
                for quiz in eval(paper_details)['paper']:
                    option = list()
                    for item in quiz[1]:
                        option.append(
                            dict(
                                key=item[0],
                                val=eval("u'" + str(item[1]) + "'"),
                            )
                        )
                    paper_detail.append(
                        dict(
                            title=eval("u'" + str(quiz[0]) + "'"),
                            option=option,
                            correct_answer=quiz[2],
                            user_answer=quiz[3],
                        )
                    )

            else:
                accuracy_percent, false_quizs, correct_quizs, paper_details = None, None, None, _dict['new_paper']
                paper_detail = list()
                for quiz in eval(paper_details)['paper']:
                    option = list()
                    for item in quiz[2]:
                        option.append(
                            dict(
                                key=item[0],
                                val=eval("u'" + str(item[1]) + "'"),
                            )
                        )
                    paper_detail.append(
                        dict(
                            quiz_id=quiz[0],
                            title=eval("u'" + str(quiz[1]) + "'"),
                            option=option,
                        )
                    )

            data = dict(
                paper_id=paper_id,
                item_id=item_id,
                accuracy_percent=accuracy_percent or -1,
                false_quizs=false_quizs or -1,
                correct_quizs=correct_quizs or -1,
                paper_completed_state=paper_completed_state,
                expect_time=knowledgeitem.expect_time,
                paper_detail=paper_detail,
            )

            return success_json(data)


def get_project_detail(project_id, class_id, student_id, userrecord):
    """
    项目详情(item)
    :param project_id:
    :param class_id:
    :param student_id:
    :param userrecord:
    :return:
    """

    class_type = Class.objects.xall().get(id=class_id).class_type

    if class_type == Class.CLASS_TYPE_NORMAL:
        project_record = ProjectRecord.objects.filter(student_id=student_id, examine_id=project_id)
        if project_record and (userrecord.status == 'DOING'):
            userrecord.status = 'DONE'
            userrecord.save()

    project = Project.objects.get(id=project_id)
    project_images = ProjectImage.objects.filter(project=project)
    img_list = []
    for project_image in project_images:
        img_list.append(settings.SITE_URL + settings.MEDIA_URL + project_image.image.name)
    data = dict(
        project_id=project_id,
        project_name=project.title,
        project_desc=project.description,
        img_list=img_list,
        career_url=settings.SITE_URL + '/course/'
    )
    return data
