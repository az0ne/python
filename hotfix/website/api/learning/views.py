# -*- coding: utf-8 -*-
"""
@version: 2016/3/29
@author: Jackie
@contact: jackie@maiziedu.com
@file: views.py
@time: 2016/3/29 15:23
@note:  ??
"""
from core.common.http.response import failed_json, success_json
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from mz_lps.models import Class, ClassStudents, PaperRecord
from mz_course.models import Lesson
from mz_lps3.models import StageTaskRelation, TaskKnowledgeRelation, UserTaskRecord, StudyHistory, KnowledgeItem, \
    UserKnowledgeItemRecord
from mz_lps3.functions_nj import StageTaskInterface, TaskKnowledgeInterface, exec_sql
from mz_lps3.functions_zxdt import TimedTestRecorder
from mz_lps4.class_dict import NORMAL_CLASS_DICT
from mz_lps4.interface_coach import create_coach_info_unlock_task
from website.api.course.interface import is_ios_check
from website.api.learning.interface import get_blank_task_map, get_student_task_map, start_exam, get_lesson_detail, \
    get_project_detail, get_free_class
from website.api.user.decorators import app_user_required
from mz_common.views import sys_send_message
from django.conf import settings
from utils.logger import logger as log
import db.api.course.career_course

import datetime
import logging

logger = logging.getLogger('api.learning.views')


def get_task_map(request):
    """
    任务地图
    :param request:
    :return:
    """
    ccourse_id = request.POST.get('ccourse_id', None)
    free_class = get_free_class(ccourse_id)
    _is_ios_check = is_ios_check(request)

    if request.user.id:
        student_id = request.user.id
        # 界定学生的班级
        free_class_student = ClassStudents.objects.filter(user_id=student_id,
                                                          student_class__career_course=ccourse_id,
                                                          student_class__class_type=Class.CLASS_TYPE_FREE,
                                                          student_class__lps_version='3.0')
        # 按id倒序排，显示最新的ClassStudents（lps3.1的学生暂停时需要在ClassStudents里也暂停）
        normal_class_student = ClassStudents.objects.filter(user_id=student_id,
                                                            student_class__career_course=ccourse_id,
                                                            student_class__class_type=Class.CLASS_TYPE_NORMAL,
                                                            is_pause=False, status=ClassStudents.STATUS_NORMAL,
                                                            student_class__lps_version='3.0').order_by('-id')
        # 首先判断是否在'正常付费班级'
        if normal_class_student:
            class_student = normal_class_student[0]

        # 若不在,再判断是否在'app免费班级'
        elif free_class_student:
            class_student = free_class_student[0]

        # 若没有在班里，则显示空地图
        else:
            return get_blank_task_map(free_class, _is_ios_check)

        # 有班，显示带学生信息的地图
        return get_student_task_map(class_student, student_id, _is_ios_check)

    # 未登陆，也显示空地图
    return get_blank_task_map(free_class, _is_ios_check)


@app_user_required
def fetch_task(request):
    """
    领取任务
    开始学习
    免费开始
    :param request:
    :return:
    """
    stagetask_id = request.POST.get('stagetask_id', None)

    task = get_object_or_404(StageTaskRelation, id=stagetask_id).task
    objs = TaskKnowledgeRelation.objects.filter(task=task).values('knowledge__name').order_by('index')
    knowledges = list(dict(name=obj.get('knowledge__name')) for obj in objs)

    data = dict(
        task_name=task.name,
        expect_time=task.expect_time,
        knowledges=knowledges,
    )

    return success_json(data)


@app_user_required
def get_task_info(request):
    """
    进入任务详情
    点'task球'
    :param request:
    :return:
    """
    try:
        ccourse_id = int(request.POST.get('ccourse_id', 0))
        class_id = int(request.POST.get('class_id', 0))
        stagetask_id = int(request.POST.get('stagetask_id', 0))
    except ValueError as e:
        return failed_json(e.message)

    user = request.user
    student_id = user.id

    # 如果没有接收到班级，则加入免费班
    if not class_id:
        free_class = get_free_class(ccourse_id)
        new_free_class_student = ClassStudents(user_id=student_id, student_class=free_class)
        new_free_class_student.save()
        free_class.current_student_count += 1
        free_class.save()
        class_id = free_class.id
        # 推送消息
        content = '您已经定制了%s的学习计划，想获取更详细的服务请登录麦子学院官网' % free_class.course_name
        sys_send_message(0, student_id, 17, content, free_class.id)

    # if not class_has_stage_task(class_id, stagetask_id):
    #     return failed_json(u'该班级不存在该任务')

    # 查询任务纪录
    usertasks = UserTaskRecord.objects.filter(stage_task=stagetask_id, student_id=student_id, class_id=class_id)

    # 如果没有任务纪录则写入
    if not usertasks:
        new_usertask = UserTaskRecord.objects.not_in_sequence_all().\
            filter(stage_task=stagetask_id, student_id=student_id, class_id=class_id)
        if not new_usertask:
            new_usertask = UserTaskRecord()
            new_usertask.class_id = class_id
            new_usertask.stage_task_id = stagetask_id
            new_usertask.student_id = student_id
        else:
            new_usertask = new_usertask[0]
        new_usertask.is_in_sequence = 1
        new_usertask.save()

        st_iface = StageTaskInterface(class_id)
        st_iface.load_student_data(student_id)
        userstage = st_iface.get_student_stage_by_stagetask(student_id, stagetask_id)

        if userstage and userstage.is_undo():  # 阶段第一个任务
            history = StudyHistory()
            history.class_id = class_id
            history.student_id = student_id
            history.content = u"我开始了[%s]的学习" % userstage.name
            history.save()
        # 如果班级号在NORMAL_CLASS_DICT里，触发1v1服务提醒
        if class_id in NORMAL_CLASS_DICT.values():
            curr_task = st_iface.get_student_task(student_id, stagetask_id)
            source = userstage.name + '-' + curr_task.task_name
            create_coach_info_unlock_task(request.user, source, ccourse_id, curr_task.task_id)

        usertask = new_usertask

    else:
        usertask = usertasks[0]

    # 取数据
    class_type = Class.objects.xall().get(id=class_id).class_type

    if not (class_type in (Class.CLASS_TYPE_FREE, Class.CLASS_TYPE_NORMAL)):
        return failed_json(u'班级类型出错')

    stagetask = get_object_or_404(StageTaskRelation, id=stagetask_id)

    iface = TaskKnowledgeInterface(class_id, stagetask_id, class_type=class_type)
    knowledges = iface.get_student_data(student_id)

    all_items_have_done = iface.all_items_have_done(student_id)
    done_item_count = iface.done_item_count(student_id)

    # 分享之后'DOING'会改成'DONE'
    to_be_share = False
    if (class_type == Class.CLASS_TYPE_FREE) and all_items_have_done and (usertask.status == 'DOING'):
        to_be_share = True

    # 已完成的item,这里task_project也看做一个item
    done_item = done_item_count + \
                (int(usertask.status in ('DONE', 'PASS')) if class_type == Class.CLASS_TYPE_NORMAL else 0)

    # 组织数据
    item_list = []
    task_video_list = []
    for knowledge in knowledges:
        for item in knowledge.get_items():
            # 取TEST分数begin
            accuracy_percent = -1
            lesson = None
            if item.obj_type == 'TEST':
                accuracy_percents = PaperRecord.objects. \
                    filter(is_active=1, student_id=student_id, paper_id=item.obj_id).values('accuracy')
                if accuracy_percents:
                    accuracy_percent = int(accuracy_percents[0]['accuracy'] * 100)
            # 取TEST分数over
            if item.obj_type == "LESSON":
                try:
                    useritem = get_object_or_404(UserKnowledgeItemRecord, class_id=class_id, student_id=student_id,
                                                 knowledge_item_id=item.id, user_task_record_id=usertask.id)
                except Http404:
                    useritem = UserKnowledgeItemRecord(status="DOING", knowledge_item_id=item.id, student_id=student_id,
                                                       class_id=class_id, user_task_record_id=usertask.id)
                    useritem.save()
                try:
                    lesson = Lesson.objects.get(id=item.obj_id)
                    task_video_list.append(dict(
                        item_id=item.id,
                        useritem_id=useritem.id,
                        video_name=lesson.name,
                        video_url=lesson.video_url,
                        video_time=lesson.video_length,
                        item_done=item.is_done,
                    ))
                except Lesson.DoesNotExist:
                    lesson = None
            item_list.append(dict(
                item_id=item.id,
                video_time=lesson.video_length if lesson else 0,
                item_name=item.get_name(),
                item_type=item.obj_type,
                item_done=item.is_done,
                item_can_be_unlocked=item.can_be_unlocked() is None or item.can_be_unlocked(),
                expect_time=item.get_expect_time() or -1,
                quiz_count=item.get_quiz_count() or -1,
                is_item=True,
                accuracy_percent=accuracy_percent,
            ))

    # 单独加入task的PROJECT
    item_list.append(dict(
        item_id=-1,
        item_name=stagetask.task.project.title,
        item_type="TASK_PROJECT",
        item_done=not usertask.is_going(),
        item_can_be_unlocked=all_items_have_done,
        expect_time=-1,
        quiz_count=-1,
        is_item=False,
        accuracy_percent=-1,
    ))

    data = dict(
        class_id=class_id,
        stagetask_id=stagetask_id,
        stage_name=stagetask.stage.name,
        task_name=stagetask.task.name,
        class_type=class_type,
        all_items_have_done=all_items_have_done,
        current_item=usertask.learning_item_id or 0,
        to_be_share=to_be_share,
        done_item=done_item,
        item_list=item_list,
        is_can_pay=stagetask.stage.career_course.is_class,
        task_video_list=task_video_list,
        img_url=settings.SITE_URL + settings.MEDIA_URL + str(stagetask.stage.career_course.app_offline_image)
    )

    # 加亚马逊广告
    result = db.api.course.career_course.get_app_career_ad(ccourse_id)
    if result.is_error():
        log.warn("db get_app_career_ad is error, career_id is %s" % ccourse_id)
        return failed_json(u'服务器开小差了，请稍后再试')
    ad = result.result()
    if ad:
        # value int to str
        for k, v in ad.iteritems():
            if isinstance(v, (int, long)):
                ad[k] = str(v)
        _full_url = settings.SITE_URL + settings.MEDIA_URL + ad.get('img_url', '')
        ad.update({'img_url': _full_url})
    data.update({'ad': ad})

    return success_json(data)


@app_user_required
def unlock_task(request):
    """
    解锁任务(分享成功后)
    :param request:
    :return:
    """
    class_id = request.POST.get('class_id', None)
    stagetask_id = request.POST.get('stagetask_id', None)
    user = request.user
    student_id = user.id

    usertask = UserTaskRecord.objects.filter(stage_task=stagetask_id, student_id=student_id, class_id=class_id)
    if usertask:
        usertask.update(status='DONE', done_time=datetime.datetime.now())
        return success_json(dict())
    else:
        return failed_json(u'没有此用户记录')


@app_user_required
def get_item_detail(request):
    """
    学生知识点item
    :param request:
    :return:
    """
    class_id = request.POST.get('class_id', None)
    stagetask_id = request.POST.get('stagetask_id', None)
    item_id = request.POST.get('item_id', None)
    user = request.user
    student_id = user.id

    usertask = get_object_or_404(UserTaskRecord, class_id=class_id, student_id=student_id, stage_task_id=stagetask_id)

    knowledgeitem = get_object_or_404(KnowledgeItem, id=item_id)

    try:
        useritem = get_object_or_404(UserKnowledgeItemRecord, class_id=class_id, student_id=student_id,
                                     knowledge_item_id=item_id, user_task_record_id=usertask.id)
    except Http404:
        # iface = TaskKnowledgeInterface(class_id, stagetask_id)
        # iface.load_student_data(student_id)
        useritem = UserKnowledgeItemRecord(status="DOING", knowledge_item=knowledgeitem, student_id=student_id,
                                           class_id=class_id, user_task_record_id=usertask.id)
        useritem.save()
    # 当前学习的item
    usertask.learning_item_id = item_id
    usertask.save()
    item_type = useritem.knowledge_item.obj_type
    if item_type == "LESSON":
        return get_lesson_detail(user, useritem)
    elif item_type == "PROJECT":
        project_id = knowledgeitem.obj_id
        return success_json(get_project_detail(project_id, class_id, student_id, useritem))
    elif item_type == "TEST":
        return start_exam(student_id, class_id, stagetask_id, item_id)
    assert 1 == 2


@app_user_required
def get_task_project(request):
    """
    项目详情(task)
    :param request:
    :return:
    """
    class_id = request.POST.get('class_id', None)
    stagetask_id = request.POST.get('stagetask_id', None)
    student_id = request.user.id
    try:
        usertask = UserTaskRecord.objects.get(class_id=class_id, student_id=student_id, stage_task_id=stagetask_id)
    except UserTaskRecord.DoesNotExist:
        return failed_json(u'找不到对应任务记录')
    project_id = usertask.stage_task.task.project_id

    return success_json(get_project_detail(project_id, class_id, student_id, usertask))


@app_user_required
def submit_exam_answer(request):
    """
    提交测验答案
    :param request:
    :return:
    """
    class_id = request.POST.get('class_id', None)
    stagetask_id = request.POST.get('stagetask_id', None)
    item_id = request.POST.get('item_id', None)
    paper = eval(request.POST.get('paper', None))
    if not paper:
        return failed_json(u'未接收到答案数据')

    user = request.user
    student_id = user.id

    result = TimedTestRecorder(student_id, class_id, item_id, stagetask_id, paper).record()

    if len(result) > 0:
        data = dict(
            correct_quizs=result[0],
            false_quizs=result[1],
        )

        return success_json(data)

    else:
        return failed_json(u'交卷发生错误')


@app_user_required
def get_his_task(request):
    """
    他的任务记录(学员)
    :param request:
    :return:
    """
    target_user_id = request.POST.get('target_user_id', None)

    sql = """
    SELECT
        t.`name`,
        c.career_course_id
    FROM
        mz_lps3_task AS t
    INNER JOIN mz_lps3_stagetaskrelation AS str ON (
        t.id = str.task_id
    )
    INNER JOIN mz_lps3_usertaskrecord AS utr ON (
        str.id = utr.stage_task_id AND is_in_sequence = 1
    )
    INNER JOIN mz_lps_class AS c ON (
        c.id = utr.class_id
    )
    WHERE
        utr.student_id = %s
    GROUP BY
        t.id
    """ % target_user_id
    task_list = list()
    for task_name, ccourse_id in exec_sql(sql):
        task_list.append(dict(
            task_name=task_name,
            ccourse_id=ccourse_id,
        ))
    data = dict(
        task_list=task_list
    )

    return success_json(data)


@app_user_required
def update_lesson(request):
    """
    接收数据,把user_knowledge_item状态改为'DONE'(当视频播放到某一点的时候)
    :param request:
    :return:
    """
    try:
        useritem_id = request.POST.get('useritem_id')
        user_knowledge_item = UserKnowledgeItemRecord.objects.get(pk=useritem_id)
        if user_knowledge_item.status == 'DOING':
            user_knowledge_item.status, user_knowledge_item.done_time = 'DONE', datetime.datetime.now()
            user_knowledge_item.save()
        return success_json(dict())
    except UserKnowledgeItemRecord.DoesNotExist:
        return failed_json(u'用户知识点项纪录出错')
