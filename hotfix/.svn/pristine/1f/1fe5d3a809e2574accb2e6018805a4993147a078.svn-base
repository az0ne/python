# -*- coding: utf-8 -*-
import datetime
import json

from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context import RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from mz_common.function_discuss import get_questons
from mz_common.user_study_info import UserStudyInfo
from mz_common.lps_version import get_user_study_version
from mz_lps3_free.student.interface_questionnaire import short_name_to_questionnaire_id
from mz_lps4.class_dict import NORMAL_CLASS_DICT, LPS4_DICT
from mz_lps4.interface import is_lps_class
from mz_usercenter.student.interface_resume import get_resume_user_info_interface, list_user_work_interface, \
    list_user_edu_interface
from utils.constants import CoachUserType
from utils.decorators_cache import cache_data
from mz_common.decorators import student_required
from django.contrib.auth.decorators import login_required
from mz_eduadmin.stats.interface import is_questionnaire_to_be_done
from mz_lps.models import ClassStudents, Class, ProjectRecord, Quiz, Paper
from mz_lps3.decorators import check_student_status
from mz_lps3.functions_yf import get_top_data, get_grade_rank_of_class, \
    get_progress_rank_of_class
from mz_lps3.functions_zxdt import StudentTimedTest, TimedTestRecorder
from mz_user.functions import is_basic_info_completed, is_job_intention_info_completed
from mz_user.models import UserJobInfo
from mz_lps3.models import ClassRank, StageTaskRelation, UserTaskRecord, ClassMeetingVideo, UserKnowledgeItemRecord, \
    KnowledgeItem, TaskKnowledgeRelation, StudyHistory, Task
from mz_course.models import Lesson, Course_User_Score, CareerCourse
from calc_functions import get_class_rank_record
import functions
from mz_lps3.functions_scf import ClassDyMsgQueue
from mz_usercenter.student.interface_job_info import get_job_info_by_class_student
from mz_lps4.interface_coach import create_coach_info_student_join_class

import logging
import db.api.onevone.study_service

# zhangyu
from mz_user.models import MyCourse, UserProfile

logger = logging.getLogger('mz_lps3.views')


@student_required
@check_student_status
def student_class(request, class_id):
    """学生班级总览"""
    if is_lps_class(class_id):  # 不让lps4学员进入LPS3
        raise Http404
    student = request.user
    student_id = request.user.id
    class_id = int(class_id)
    class_student = request.cstudent
    sclass = class_student.student_class
    student_class_studing_paused = class_student.is_pause
    teachers = sclass.teachers.all()
    assert isinstance(sclass, Class)

    locals().update(get_top_data(student, sclass))  # 获取顶部动态数据 by feng
    grade_top3 = get_grade_rank_of_class(sclass.id, 3)  # 获取成绩前三名
    progress_top3 = get_progress_rank_of_class(sclass.id, 3)  # 获取进度前三名

    # 以下开始取任务数据
    st_interface = functions.StageTaskInterface(class_id)

    # total = st_interface.count_all_tasks()
    stages = st_interface.get_student_data(student_id)
    # done = st_interface.count_student_tasks_finished(student_id)  # 完成数量
    current_task = st_interface.get_student_latest_task(student_id)
    # total_progress = int(round(done * 100.0 / total)) if total else 100
    is_just_begging = st_interface.is_just_beginning(student_id)
    the_first_task = st_interface.get_the_first_task(student_id)
    url_pay = "/pay/view/?career_id=%s" % class_student.student_class.career_course_id

    if sclass.is_normal():  # 正常班级
        # 班会 guotao
        classmeeting_lst = functions.get_classmeeting_list(class_id, student_id)
        is_classmeeting_video = True if ClassMeetingVideo.objects.filter(class_id=class_id).exists() else False

        # 是否补全学生信息
        student_info = is_basic_info_completed(class_student)

        # 是否参加班会提醒

        # 是否弹出满意度调查问卷 zhangyunrui
        is_pop_up_questionnaire = is_questionnaire_to_be_done(class_student.id)

        # 是否选择就业 guotao add for 入学流程优化
        is_employment_contract = functions.is_employment_contract(class_student)

        # 是否补全就业信息
        is_job_intention_info = True if functions.is_choose_employment_contract(class_student) and \
                                        not is_job_intention_info_completed(student_id, class_id) and \
                                        not class_student.is_view_employment_contract else False

        # 是否弹出就业协议
        is_view_employment_contract = True if functions.is_choose_employment_contract(class_student) and\
                                              is_job_intention_info_completed(student_id, class_id) and\
                                              not class_student.is_view_employment_contract else False

        # 就业协议薪资
        if not class_student.is_view_employment_contract:
            contract_time = datetime.datetime.now()
            job_info = get_job_info_by_class_student(class_student)
            degree = job_info.get('degree')
            intention_job_city = job_info.get('intention_job_city')
            setattr(class_student, 'student_intention_city', intention_job_city)
            setattr(class_student, 'student_degree', degree)
            salary = student_month_salary(class_student, class_student.student_class.career_course.name)
        # 是否弹出不需要就业的服务
        is_view_not_employment_contract = True if class_student.is_employment_contract == False and \
                                                  not class_student.is_view_not_employment_contract else False
        # 学生完善个人信息以后，且还没有给老师和教务发送过加班短信，则发送加班短信 add for 入学流程优化
        if student_info and not class_student.is_send_sms:
            functions.send_joinclass_sms_t_e(class_student)
            class_student.is_send_sms = True
            class_student.save()

        # 是否弹出完善简历弹窗
        user_study_info = cache.get('user_study_info_%s_%s_lps4' % (student_id, class_id))
        if not user_study_info:
            """
                没有命中用户学习数据缓存
            """
            user_study_info = UserStudyInfo(student_id, class_id).__dict__
            cache.set('user_study_info_%s_lps4' % student_id, user_study_info, 5 * 60)

        # 离毕业天数
        if user_study_info['end_time']:
            end_days = (user_study_info['end_time'] - datetime.datetime.now()).days
            if end_days > 0:
                user_info = get_resume_user_info_interface(student_id)
                user_work = list_user_work_interface(student_id)
                user_edu = list_user_edu_interface(student_id)
                if not (user_study_info['start_work_time'] and user_info and user_edu and user_work):
                    is_pop_complete_resume = True
                    if end_days <= 7 and (not user_study_info['is_stop']):
                        is_force_pop_complete_resume = True

    # 就业信息表单
    degrees = UserJobInfo.DEGREES.values()
    service_years = UserJobInfo.SERVICE_YEAR_CHOICES.values()
    # study_goal_list =UserJobInfo.GOAL_CHOICES.values()
    # user_goal, user_goal_name = get_study_goal_info(student_id, class_id)

    if sclass.is_normal():
        return render(request, 'mz_lps3/student/class_index.html', locals())
    elif sclass.is_experience():  # 体验班
        url_pay = "/pay/view/?career_id=%s" % sclass.career_course_id
        return render(request, 'mz_lps3/student/experience_class_index.html', locals())
    else:
        return HttpResponse(u"未知班级类型")


@student_required
def student_class_dynmsg(request, class_id):
    student_id = request.user.id
    class_id = int(class_id)
    class_student = get_object_or_404(ClassStudents, student_class_id=class_id, user_id=student_id)
    sclass = class_student.student_class
    student_class_studing_paused = class_student.is_pause
    assert isinstance(sclass, Class)
    if sclass.is_experience():  # 免费试学班级
        url_pay = "/pay/view/?career_id=%s" % sclass.career_course_id
        return render(request, "mz_lps3/student/experience_class_dynmsg.html", locals())
    else:
        return HttpResponse(u"程序员正在赶码中,稍安勿躁,敬候佳音~~~")


@student_required
@check_student_status
def unlock_new_task(request, class_id, stagetask_id):
    """点击新任务
    :param class_id: id of Class
    :param stagetask_id: id of StageTaskRelation
    :return:解锁任务
    """
    student_id = request.user.id
    class_id = int(class_id)
    stagetask_id = int(stagetask_id)
    # 首先判断学生在这个班级
    class_student = request.cstudent

    # 判断班级有这个任务
    if not functions.class_has_stage_task(class_id, stagetask_id):
        raise Http404
    # 早已经解锁
    if UserTaskRecord.objects.filter(class_id=class_id, student_id=student_id,
                                     stage_task_id=stagetask_id).exists():
        return redirect(
            reverse("lps3:student_stagetask",
                    kwargs=dict(class_id=class_id, stagetask_id=stagetask_id))
        )

    # 全款用户休学状态
    if class_student.is_full_payment_user and class_student.is_pause:
        raise PermissionDenied(u'休学中,无法解锁')
    # 试学时间到,需要支付
    if class_student.need_pay():
        raise PermissionDenied(u'')

    iface = functions.StageTaskInterface(class_id)
    iface.load_student_data(student_id)
    # 用户是否可以开启新任务
    flag, reason = iface.student_can_unlock_task(student_id, stagetask_id)
    userstage = iface.get_student_stage_by_stagetask(student_id, stagetask_id)
    if flag:
        # 写入用户记录
        usertask = UserTaskRecord()
        usertask.class_id = class_id
        usertask.stage_task_id = stagetask_id
        usertask.student_id = student_id
        usertask.save()

        if userstage and userstage.is_undo():  # 阶段第一个任务
            history = StudyHistory()
            history.class_id = class_id
            history.student_id = student_id
            history.content = u"我开始了[%s]的学习" % userstage.name
            history.save()

        # 跳转至任务详情页面
        return redirect(
            reverse("lps3:student_stagetask",
                    kwargs=dict(class_id=class_id, stagetask_id=stagetask_id))
        )
    else:
        return HttpResponse(reason)


@student_required
@check_student_status
def unlock_new_task_guide(request, class_id, stagetask_id):
    """点击新任务
    :param class_id: id of Class
    :param stagetask_id: id of StageTaskRelation
    :return:弹出提示页
    """
    assert request.is_ajax(), u'unlock_new_task_guide 只提供ajax访问'
    student_id = request.user.id
    class_id = int(class_id)
    stagetask_id = int(stagetask_id)
    # 首先判断学生在这个班级
    class_student = request.cstudent

    # 班级是否为免费体验班级
    is_experience_class = class_student.student_class.is_experience()

    # 判断班级有这个任务
    if not functions.class_has_stage_task(class_id, stagetask_id):
        raise Http404

    task = get_object_or_404(StageTaskRelation, id=stagetask_id).task
    objs = TaskKnowledgeRelation.objects.filter(task=task).values('knowledge__name').order_by('index')
    knowledges = list(dict(name=obj.get('knowledge__name')) for obj in objs)

    eduadmin = class_student.student_class.edu_admin
    url_pay = "/pay/view/?career_id=%s" % class_student.student_class.career_course_id

    if is_experience_class:
        iface = functions.StageTaskInterface(class_id)
        iface.load_student_data(student_id)
        task_can_be_unlocked, reason = iface.student_can_unlock_task(student_id, stagetask_id)

    elif class_student.is_full_payment_user:  # 全款用户
        if class_student.is_pause:
            task_can_be_unlocked, reason = False, u'休学中'
        else:
            iface = functions.StageTaskInterface(class_id)
            iface.load_student_data(student_id)
            task_can_be_unlocked, reason = iface.student_can_unlock_task(student_id, stagetask_id)
    elif class_student.is_trial_user:  # 试学用户
        if class_student.need_pay():
            task_can_be_unlocked, reason = False, u'试学到期'
        else:
            iface = functions.StageTaskInterface(class_id)
            iface.load_student_data(student_id)
            task_can_be_unlocked, reason = iface.student_can_unlock_task(student_id, stagetask_id)
            T_UNLOCK_ERR_NOT_PAID = functions.T_UNLOCK_ERR_NOT_PAID

    return render(request, "mz_lps3/student/div_task_info.html", locals())


@student_required
@check_student_status
def rebuild_task(request, class_id, stagetask_id):
    """重修任务
    :param request:
    :param class_id:
    :param stagetask_id:
    """
    student_id = request.user.id
    class_id = int(class_id)
    stagetask_id = int(stagetask_id)
    # 首先判断学生在这个班级
    class_student = request.cstudent
    # 判断用户是否为暂停状态
    if class_student.is_pause:
        return HttpResponse(u"用户暂停状态,禁止操作,请联系您的代课老师!")
    # 判断班级有这个任务
    if not functions.class_has_stage_task(class_id, stagetask_id):
        raise Http404
    usertask = get_object_or_404(UserTaskRecord, class_id=class_id, student_id=student_id, stage_task_id=stagetask_id)
    assert usertask.status == "FAIL"

    if request.is_ajax():  # 点击任务面板
        task = usertask.stage_task.task
        knowledges = task.knowledges.all().order_by('index')
        return render(request, "mz_lps3/student/div_task_rebuild_info.html", locals())
    else:
        assert usertask.status == "FAIL"
        user_project = ProjectRecord.objects.filter(
            project_id=usertask.stage_task.task.project_id,
            student_id=student_id
        )
        usertask.status = "REDOING"
        usertask.save()
        if user_project:
            user_project[0].delete()
        return redirect(
            reverse("lps3:student_stagetask",
                    kwargs=dict(class_id=class_id, stagetask_id=stagetask_id))
        )


@student_required
@check_student_status
def student_stagetask(request, class_id, stagetask_id):
    """学生阶段任务详情"""
    student_id = request.user.id
    stagetask_id = int(stagetask_id)
    class_id = int(class_id)
    # 首先判断学生在这个班级
    cstudent = request.cstudent

    # 判断班级有这个stage_task
    if not functions.class_has_stage_task(class_id, stagetask_id):
        raise Http404

    # 用户任务
    usertask = get_object_or_404(UserTaskRecord, class_id=class_id, student_id=student_id, stage_task_id=stagetask_id)
    if usertask.status == "FAIL":
        return redirect(
            reverse("lps3:student_class", kwargs=dict(class_id=class_id))
        )

    task = usertask.stage_task.task
    if task.is_free488_task():
        raise Http404
    guide_task_id = Class.objects.xall().get(id=class_id).career_course.lps3_guide_task_id
    task_is_guide = task.id in (guide_task_id, settings.GUIDE_TASK_ID)

    iface = functions.TaskKnowledgeInterface(class_id, stagetask_id)
    knowledges = iface.get_student_data(student_id)
    progress = iface.get_utask_progress(student_id)
    # 剩余时长
    timeleft = functions.calc_timeleft(
        usertask.created, task.expect_time, usertask.paused_seconds, usertask.is_pause, usertask.pause_datetime)
    # 当前项目(上次的记录)
    current_item = iface.get_student_item(student_id, usertask.learning_item_id)
    # 当前知识点id
    current_knowledge_id = current_item.parent_id if current_item else None

    # 所有已做完的项目
    all_items_have_done = iface.all_items_have_done(student_id)
    # 是否为刚刚开始(还未进行第一个item)
    is_just_beginning = iface.is_just_beginning(student_id)
    # 第一个item
    first_item = iface.get_the_first_item(student_id)

    div_template = get_template("mz_lps3/student/div_usertask_item_list.html")
    html_usertask_item_list = div_template.render(RequestContext(request, locals()))

    return render(request, "mz_lps3/student/usertask.html", locals())


def render_study_right_item_list_div(request, class_id, student_id, stagetask_id, item_id=None):
    """渲染学习界面右侧 目录"""
    class_id = int(class_id)
    student_id = int(student_id)
    stagetask_id = int(stagetask_id)
    item_id = int(item_id) if item_id else None

    # 用户任务
    _class = Class.objects.xall().get(id=class_id)
    iface = functions.TaskKnowledgeInterface(class_id, stagetask_id, class_type=_class.class_type)
    knowledges = iface.get_student_data(student_id)
    usertask = iface.get_student_usertask_model(student_id)

    all_items_have_done = iface.all_items_have_done(student_id)
    clas = request.cclass
    div_template = get_template("mz_lps3/student/div_study_right_item_list.html")

    # 如果只有一个知识点,并且item少于15项,直接展开就是了  jackie
    all_menus_open = (len(knowledges) == 1) and (len(knowledges[0].get_items()) < 15)

    # 免费试学班在此页面点击返回的时候应该弹出问卷,问卷short_name为why_quit
    questionnaire_id = short_name_to_questionnaire_id('why_quit')

    if item_id is not None:
        active_knowledge_id = iface.get_knowledge_id_by_item(item_id)
    html_usertask_item_list = div_template.render(
        RequestContext(request, locals()))
    return html_usertask_item_list


def check_status_and_redirect(request):
    """对用户的状态检测,并跳转提示页面"""
    class_student = request.cstudent
    eduadmin = class_student.student_class.edu_admin

    if class_student.is_full_payment_user and class_student.is_pause:
        if request.is_ajax():
            raise PermissionDenied
        return render(request, 'mz_lps3/student/errorpage_pause.html', locals())
    elif class_student.is_trial_user and class_student.need_pay():
        if request.is_ajax():
            raise PermissionDenied
        url_pay = "/pay/view/?career_id=%s" % class_student.student_class.career_course_id
        return render(request, 'mz_lps3/student/errorpage_needpay.html', locals())


@student_required
@check_student_status
def student_knowledgeitem(request, class_id, stagetask_id, item_id):
    """学生知识点item"""
    student_id = request.user.id
    class_id = int(class_id)
    item_id = int(item_id)
    # 找到用户任务记录
    try:
        # 乱序解锁任务球，加not_in_sequence_all。正序乱序都能进item
        usertask = UserTaskRecord.objects.not_in_sequence_all().\
            get(class_id=class_id, student_id=student_id, stage_task_id=stagetask_id)
    except Exception:
        # 如果没有找到记录，且是lps4的班，就在UserTaskRecord加入乱序记录
        if class_id in NORMAL_CLASS_DICT.values():
            usertask = UserTaskRecord()
            usertask.class_id = class_id
            usertask.stage_task_id = stagetask_id
            usertask.student_id = student_id
            usertask.is_in_sequence = 0
            usertask.save()
        else:
            raise Http404

    try:
        useritem = get_object_or_404(UserKnowledgeItemRecord,
                                     class_id=class_id, student_id=student_id,
                                     knowledge_item_id=item_id, user_task_record_id=usertask.id)
    except Http404:  # 新建
        knowledgeitem = get_object_or_404(KnowledgeItem, id=item_id)

        if knowledgeitem.obj_type != 'LESSON':
            ret = check_status_and_redirect(request)
            if ret is not None:
                return ret

        iface = functions.TaskKnowledgeInterface(class_id, stagetask_id, class_type=request.cclass.class_type)
        iface.load_student_data(student_id)
        item = iface.get_student_item(student_id, knowledgeitem.id)
        if item is None:
            return HttpResponse(u"你娃在逗我呢,你确定有这个url?")
        if not item.can_be_unlocked() and not item.is_lesson:
            return HttpResponse(u"消停的先把前面东西做完再来吧~~~")
        useritem = UserKnowledgeItemRecord()
        useritem.status = "DOING"
        useritem.knowledge_item = knowledgeitem
        useritem.student_id = student_id
        useritem.class_id = class_id
        useritem.user_task_record_id = usertask.id
        useritem.save()
    # 当前学习的item
    usertask.learning_item_id = item_id
    usertask.save()
    item_type = useritem.knowledge_item.obj_type
    if item_type == "LESSON":
        # 长福
        p_id = request.GET.get('p_id')
        _url = "/lps3/student/item_lesson/%s_%s_%s" + (('?p_id=' + p_id) if p_id else '')
        return redirect(_url % (class_id, stagetask_id, item_id))
    elif item_type == "PROJECT":
        # 转转
        return redirect("/lps3/student/item_project/%s_%s_%s" % (class_id, stagetask_id, item_id))
    elif item_type == "TEST":
        # 云瑞
        return redirect("/lps3/student/item_test/%s_%s_%s" % (class_id, stagetask_id, item_id))
    assert 1 == 2


def student_study_history(request, class_id):
    return HttpResponse('有事请找弋老师')


@student_required
@check_student_status
def student_classmeeting(request, class_id):
    video_dict = functions.get_classmeetings_by_class_id(class_id)
    datetime.datetime.now().weekday()
    content = {"video_dict": video_dict, 'now_month': datetime.datetime.now().month,
               'now_year': datetime.datetime.now().year, 'class_id': class_id}
    return render(request, 'mz_lps3/student/live_meeting.html', content)


@login_required(login_url="/")
def class_meeting_player(request, class_id, play_id):
    # ownerid = "vBVV5jdMJp"
    class_video = functions.get_class_video_by_play_id(class_id, play_id)

    if request.user.is_student():
        class_student = get_object_or_404(
            ClassStudents, student_class_id=class_id, user_id=request.user.id, status=ClassStudents.STATUS_NORMAL)
        if class_student.is_trial_user and class_video.create_time > class_student.deadline:
            eduadmin = class_student.student_class.edu_admin
            url_pay = "/pay/view/?career_id=%s" % class_student.student_class.career_course_id
            return render(request, 'mz_lps3/student/errorpage_needpay.html', locals())

    return render(request, "mz_lps3/class_meeting_player.html", {"play_id": play_id, "class_video": class_video})


# 限时测试
@student_required
@check_student_status
def timed_test(request, class_id, knowledgeitem_id, stage_task_id):
    # 取基础数据
    context = {}
    paper_id = get_object_or_404(KnowledgeItem, id=knowledgeitem_id).obj_id
    paper = Paper.objects.filter(examine_type=6, pk=paper_id)
    # 排除两种异常
    if not paper:
        context['reason'] = '还没有试卷,请联系带班老师。<a href="' + str(settings.SITE_URL) + '">返回首页</a>'
    else:
        quizs = Quiz.objects.filter(paper=paper)
        if not quizs:
            context['reason'] = '试卷下没有题目,请联系带班老师。<a href="' + str(settings.SITE_URL) + '">返回首页</a>'
        else:
            student_timed_test = StudentTimedTest(request.user.id, class_id, knowledgeitem_id, stage_task_id)
            _dict = student_timed_test.get_context()
            _dict['html_usertask_item_list'] = render_study_right_item_list_div(
                request, class_id, request.user.id, stage_task_id, knowledgeitem_id)
            _dict['student_class'] = request.cclass
            _dict['is_lps4'] = is_lps_class(class_id)

            _type = get_user_study_version(request.user.id)
            task = get_object_or_404(Task, stagetaskrelation__id=stage_task_id)
            career = get_object_or_404(CareerCourse, class__id=class_id)

            _dict['trace_pay_type'] = _type['pay_type']
            _dict['trace_user_type'] = _type['user_type']
            _dict['trace_taskball_name'] = task.name
            _dict['trace_career_name'] = career.name
            _dict['trace_test_name'] = paper[0].title
            return render(request, 'mz_lps3/student/study_exam.html', _dict)
    return render(request, 'mz_common/failure.html', context)


# 限时测试提交
@csrf_exempt
@check_student_status
def submit_paper(request, class_id, stage_task_id, knowledgeitem_id):
    if (request.method == 'POST'):
        payload = {}
        paper = request.POST.dict()
        result = TimedTestRecorder(request.user.id, class_id, knowledgeitem_id, stage_task_id, paper).record()
        # 如果result为空,则return空json,当前端接收到空data,请求方式变为GET
        if len(result) > 0:
            payload['correct_quizs'] = result[0]
            payload['false_quizs'] = result[1]
            payload['accuracy_percent'] = result[2]
            # 推送班级动态消息
            knowledgeitem = KnowledgeItem.objects.get(pk=knowledgeitem_id)  # 取得知识点
            message = dict(user_id=request.user.id,
                           nick_name=request.user.real_name if request.user.real_name else request.user.nick_name,
                           avatar_url=request.user.avatar_url.url,
                           message='完成测评%s' % knowledgeitem.name,
                           time=datetime.datetime.now())
            ClassDyMsgQueue.push(class_id, ClassDyMsgQueue.format_message(message))
        return HttpResponse(json.dumps(payload), content_type='application/json')
    else:
        return render(request, 'mz_common/failure.html',
                      {'reason': '交卷发生错误。<a href="' + str(settings.SITE_URL) + '">返回首页</a>'})


# @student_required
@check_student_status
def student_item_lesson(request, class_id, stagetask_id, item_id):
    use_cache = False

    def _render_html(request, class_id, stagetask_id, item_id):

        template = 'mz_course/lessonVideo.html'
        student_id, class_id, item_id = request.user.id, int(class_id), int(item_id)
        # student_id = 69736
        # 是否需要验证前面的任务已经完成？
        # TODO： implement a decorator to confirm if user can access an item.
        try:
            # 乱序解锁任务球，加not_in_sequence_all。正序乱序都能进lesson
            usertask = UserTaskRecord.objects.not_in_sequence_all().\
                get(class_id=class_id, student_id=student_id, stage_task_id=stagetask_id)
        except Exception:
            raise Http404

        task = get_object_or_404(Task, stagetaskrelation__id=stagetask_id)
        career = get_object_or_404(CareerCourse, class__id=class_id)

        # 课程所在任务是否为新手引导任务
        guide_task_id = Class.objects.xall().get(id=class_id).career_course.lps3_guide_task_id
        task_is_guide = usertask.stage_task.task.id in (guide_task_id, settings.GUIDE_TASK_ID)
        try:
            useritem = get_object_or_404(UserKnowledgeItemRecord, class_id=class_id, student_id=student_id,
                                         knowledge_item_id=item_id, user_task_record_id=usertask.id)
        except Http404:
            return u"消停的先把前面东西做完再来吧~~~"
        template_vars = dict()
        lesson = get_object_or_404(Lesson, pk=useritem.knowledge_item.obj_id)
        course = lesson.course
        template_vars['lesson'] = lesson
        template_vars['course'] = course
        template_vars['student_class'] = request.cclass
        template_vars['usertask'] = usertask
        template_vars['task_is_guide'] = task_is_guide
        template_vars['stage_task_id'] = stagetask_id
        template_vars['useritem'] = useritem.id
        template_vars['lesson_id'] = lesson.id
        template_vars['video_url'] = lesson.video_url
        template_vars['video_name'] = lesson.name
        template_vars['video_length'] = lesson.video_length
        template_vars['VIDEO_EXAM_COMPLETE'] = settings.VIDEO_EXAM_COMPLETE
        template_vars['class_id'] = class_id
        template_vars['course_id'] = course.id
        template_vars['discuss_location'] = '%s_%s_%s' % (class_id, stagetask_id, item_id) # 回复讨论的位置
        template_vars['study_number'] = course.click_count  # 学习人数
        # 打分, 逻辑仍然沿用2.0
        template_vars['my_score'] = True if Course_User_Score.objects.filter(user_id=student_id,
                                                                             course_id=course.id).exists() else False
        template_vars['score'] = round(course.score_ava, 1)
        # 收藏, 逻辑仍然沿用2.0
        # from mz_user.models import UserProfile
        # user = UserProfile.objects.get(pk=student_id)
        # template_vars['is_favorite'] = True if user.myfavorite.filter(id=course.id).count() > 0 else False
        template_vars['is_favorite'] = True if request.user.myfavorite.filter(id=course.id).count() > 0 else False
        try:
            template_vars['qq_group'] = get_object_or_404(Class, pk=class_id).career_course.qq  # qq number
        except Http404:
            template_vars['qq_group'] = None
        template_vars['task_index'] = render_study_right_item_list_div(
            request, class_id, student_id, stagetask_id, item_id)  # 任务目录
        template_vars['course_resource_list'] = list(course.courseresource_set.all())  # 课程课件, same as LPS 2.0
        template_vars['lesson_resource_list'] = list(lesson.lessonresource_set.all())  # 章节课件, same as LPS 2.0

        # 问答加的代码
        teachers = UserProfile.objects.\
            filter(teachers__id=class_id).values('id', 'nick_name', 'avatar_small_thumbnall')
        if teachers:
            teachers = teachers[0]
        template_vars['teachers'] = teachers

        all_questions, my_questions = get_questons(lesson.id, student_id)
        template_vars['all_questions'] = all_questions
        template_vars['my_questions'] = my_questions

        # 免费试学班在此页面点击返回的时候应该弹出问卷,问卷short_name为why_quit
        questionnaire_id = short_name_to_questionnaire_id('why_quit')
        template_vars['questionnaire_id'] = questionnaire_id
        template_vars['is_lps4'] = is_lps_class(class_id)
        if template_vars['is_lps4']:
            # lps4取class_id对应的职业课程id
            career_id = LPS4_DICT.get(int(class_id), -1)
            template_vars['lps4_teacher'] = db.api.onevone.study_service\
                .get_teacher_info_by_lps4(int(career_id), int(student_id)).result()
        template_vars['CoachUserType'] = CoachUserType

        _type = get_user_study_version(student_id)
        template_vars['trace_pay_type'] = _type['pay_type']
        template_vars['trace_user_type'] = _type['user_type']
        template_vars['trace_taskball_name'] = task.name
        template_vars['trace_career_name'] = career.name
        template_vars['trace_video_name'] = lesson.name
        template_vars['career'] = career
        return get_template(template).render(RequestContext(request, template_vars))

    if use_cache:
        # set cache here
        pass
    else:
        return HttpResponse(_render_html(request, class_id, stagetask_id, item_id))


# @student_required
# def student_info_submit(request):
#     real_name = request.POST.get('real_name')
#     qq = request.POST.get('qq')
#     email = request.POST.get('email')
#     mobile = request.POST.get('mobile')
#     address = request.POST.get('address')
#     city = request.POST.get('city')
#     study_goal_opt = request.POST.get('study_goal_opt')
#     study_base_opt = request.POST.get('study_base_opt')
#
#     if StudentInfo.objects.filter(student_id=request.user.id):
#         return HttpResponse(json.dumps(dict(status=False, error='学生信息已提交过')), content_type='application/json')
#
#     if qq:
#         request.user.qq = qq
#     if city:
#         request.user.city_id = city
#     if study_goal_opt:
#         request.user.study_goal_opt_id = study_goal_opt
#     if study_base_opt:
#         request.user.study_base_opt_id = study_base_opt
#     request.user.save()
#     if real_name and email and mobile and address:
#         data = dict(student_id=request.user.id,
#                     real_name=real_name,
#                     email=email,
#                     mobile=mobile,
#                     address=address,
#                     )
#         try:
#             StudentInfo.objects.create(**data)
#             return HttpResponse(json.dumps(dict(status=True)), content_type='application/json')
#         except Exception, e:
#             logger.error(e)
#             return HttpResponse(json.dumps(dict(status=False, error=str(e))), content_type='application/json')
#     return HttpResponse(json.dumps(dict(status=False, error='未知错误')), content_type='application/json')


@student_required
@check_student_status
def contract_submit(request):
    checked = request.POST.get('checked')
    class_id = request.POST.get('class_id')
    contract = request.POST.get('contract')
    if checked == 'true' and class_id and contract:
        class_student = request.cstudent
        if contract == u'入学':
            class_student.is_view_contract = True
        if contract == u'服务':
            class_student.is_view_not_employment_contract = True
        if contract == u'就业':
            job_info = get_job_info_by_class_student(class_student)
            class_student.student_degree = job_info.get('degree')
            class_student.student_intention_city = job_info.get('intention_job_city')
            class_student.salary = student_month_salary(class_student,
                                                        class_student.student_class.career_course.name)
            # if class_student.user.intention_job_city and class_student.user.degree:
            #     class_student.student_degree = UserProfile.DEGREES[class_student.user.degree]
            #     class_student.student_intention_city = class_student.user.intention_job_city
            #     class_student.salary = student_month_salary(class_student.user,
            #                                                 class_student.student_class.career_course.name)
            class_student.employment_contract_time = datetime.datetime.now()
            class_student.is_view_employment_contract = True
        class_student.save()
        # 添加新学院入班 的学习建议
        if contract in [u'服务', u'就业']:
            # 添加新学员入班1v1服务消息
            career_course = class_student.student_class.career_course
            create_coach_info_student_join_class(request.user, career_course.id, career_course.name)
        return HttpResponse(json.dumps(dict(status=True)), content_type='application/json')
    return HttpResponse(json.dumps(dict(status=False)), content_type='application/json')


@student_required
@check_student_status
def qq_hints_close(request):
    """关闭一键加QQ群提醒"""
    class_id = request.POST.get('class_id')
    class_student = request.cstudent
    class_student.is_qq_hints = True
    class_student.save()
    return HttpResponse(json.dumps(dict(status=True)), content_type='application/json')


@student_required
@check_student_status
def employment_contract_submit(request):
    """学生选择是否需要就业"""
    class_id = request.POST.get('class_id')
    is_employment_contract = request.POST.get('is_employment_contract')
    class_student = request.cstudent
    class_student.is_employment_contract = True if is_employment_contract == 'true' else False
    class_student.save()
    return HttpResponse(json.dumps(dict(status=True)), content_type='application/json')


def student_rank_list(request):
    from functions_zy import StudentClassRank

    user_id = request.GET.get('user_id', None)
    if not user_id:
        return HttpResponse(json.dumps({}), content_type='application/json')
    user = UserProfile.objects.get(id=user_id)
    mycourse = MyCourse.objects.filter(user=user) \
        .filter(course_type=2).order_by('index', '-id')
    data = {}
    for course in mycourse:
        data[course.course] = StudentClassRank(user.id, course.course).get_rank()
    return HttpResponse(json.dumps(data), content_type='application/json')


# 学生查看入学须知
@student_required
def student_admission_infor(request):
    return render(request, 'mz_lps3/student/Freshers.html', locals())


# 学生查看无需就业服务
@student_required
def student_not_employment_agreement(request):
    return render(request, 'mz_lps3/student/not_employment.html', locals())


# 学生查看就业协议
@student_required
def student_employment_agreement(request, class_id):
    class_student = get_object_or_404(ClassStudents, student_class_id=class_id, user_id=request.user.id)
    salary = 5000
    contract_time = class_student.created
    new = True
    if contract_time:
        if contract_time < datetime.datetime(2016, 3, 11):
            new = False
            return render(request, 'mz_lps3/student/agreement.html', locals())
    else:
        new = False
        return render(request, 'mz_lps3/student/agreement.html', locals())
    if not (class_student.employment_contract_time and class_student.salary):
        job_info = get_job_info_by_class_student(class_student)
        class_student.student_degree = job_info.get('degree')
        class_student.student_intention_city = job_info.get('intention_job_city')
        class_student.salary = student_month_salary(class_student,
                                                    class_student.student_class.career_course.name)
        # if class_student.user.intention_job_city and class_student.user.degree:
        #     class_student.student_degree = UserProfile.DEGREES[class_student.user.degree]
        #     class_student.student_intention_city = class_student.user.intention_job_city
        #     class_student.salary = student_month_salary(class_student.user,
        #                                                 class_student.student_class.career_course.name)
        if not class_student.employment_contract_time:
            class_student.employment_contract_time = class_student.created
        class_student.save()
        # intention_job_city = class_student.student_intention_city
        # salary = class_student.salary
        # contract_time = class_student.employment_contract_time
        # degree = class_student.student_degree
    # else:
    degree = class_student.student_degree
    intention_job_city = class_student.student_intention_city
    salary = class_student.salary
    contract_time = class_student.employment_contract_time
    return render(request, 'mz_lps3/student/agreement.html', locals())


# 根据学生学历及城市选择就业协议月薪
def student_month_salary(class_student, career_course_name):
    if not (class_student.student_intention_city and class_student.student_degree):
        return 5000
    city_dict = {1: ['北京', '上海', '广州', '深圳', '天津'],
                 2: ['南京', '武汉', '沈阳', '西安', '成都', '重庆', '杭州', '青岛', '大连', '宁波', '济南', '哈尔滨', '长春', '厦门', '郑州', '长沙',
                     '福州', '乌鲁木齐', '昆明', '兰州', '苏州', '无锡']}
    city = None
    for key, value in city_dict.items():
        if class_student.student_intention_city in value:
            city = key
            break
    if not city:
        city = 3
    if career_course_name == u'软件测试':
        city += 1
    if class_student.student_degree in [u'硕士', u'博士']:  # '硕士', '博士'
        student_salary = 6000 - (city - 1) * 500
    elif class_student.student_degree == u'大学本科':  # 大学本科
        student_salary = 5500 - (city - 1) * 500
    else:
        student_salary = 5000 - (city - 1) * 500
    return student_salary


@student_required
def class_rank(request, class_id, student_id):
    """
    获取班级进度排名和班级成绩排名．缓存一天，缓存过期之后，重新计算，并存数据库
    :param request:
    :param class_id:
    :param student_id:
    :return:
    """
    cache_time = 60 * 60 * 12
    template = 'mz_lps3/student/class_ranking.html'
    student_id = int(student_id)
    class_score_rank = cache_data(cache_time, key='class_score_rank_%s' % class_id) \
        (get_class_rank_record)(class_id, rank_type='1')
    class_progress_rank = cache_data(cache_time, key='class_progress_rank_%s' % class_id) \
        (get_class_rank_record)(class_id, rank_type='2')
    locals().update(get_top_data(student_id, class_id))  # 获取顶部动态数据
    fps_center = settings.FPS_CENTER
    # return get_template(template).render(RequestContext(request, locals())) # strange error
    return render(request, template, locals())
