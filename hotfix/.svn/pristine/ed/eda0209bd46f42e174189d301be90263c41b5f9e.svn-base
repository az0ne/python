# -*- coding: utf-8 -*-
import json
import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.context import RequestContext
from django.template.loader import render_to_string, get_template_from_string
from django.core.cache import cache

from mz_common.lps_version import get_user_study_version
from mz_common.models import MyMessage
from mz_lps.models import ClassStudents
from mz_lps3.functions_nj import StageTaskInterface
from mz_lps3.models import UserTaskRecord, Task, StageTaskRelation, StudyHistory
from mz_lps4.class_dict import TRY_CLASS_DICT, NORMAL_CLASS_DICT, CAREER_ID_TO_SHORT_NAME
from mz_lps4.context import get_lps4_context
from mz_lps4.interface_lps import lps4_data, lps4_change_rebuild_to_rebuilding, \
    get_skill_radar_by_career_id_interface, get_skill_tree_by_class_id_career_id_user_id_interface, \
    get_lps_3_1_teacher_by_career_id_interface, get_student_enter_data, get_lps_3_1_career_info_list_interface, \
    lps4_public, get_lps_3_1_careers_by_user_id_interface, get_career_course_knowledge_task_count_interface, \
    get_lps4_student_info_by_user_id_interface, get_lps4_teacher_by_career_student_id_interface
from mz_lps4.interface_index import get_career_teachers, get_career_student_work, get_career_relate_article, \
    get_career_discuss
from mz_lps4.interface import get_onevone_meeting_info, generate_oneveone_meeting
from mz_lps4.interface_coach import create_coach_info_unlock_task
from mz_lps4.lps_template import CAREERS, STAGES, CURRENT_TASK
from apps.mz_lps4.class_dict import SHORT_NAME_TO_CAREER_ID
from utils.is_logined import is_logined
from utils.logger import logger as log
from mz_lps3 import functions
import db.api.lps.student
import db.api.lps.lps_index
import db.api.course.course_task

import HTMLParser

html_parser = HTMLParser.HTMLParser()

CLASS_TYPE_EXPERIENCE_3_1 = 2
TASK_TYPE_NORMAL = StageTaskRelation.STAGE_TASK_TYPE_NORMAL


def get_unlogined_data(career_id):
    """
    获取未登录数据
    :param career_id:
    :return:
    """
    # 获取二次渲染模板
    careers = CAREERS
    stages = STAGES
    current_task = CURRENT_TASK
    try:  # 获取页面右侧数据
        teachers = get_career_teachers(career_id)
        student_works = get_career_student_work(career_id)
        articles = get_career_relate_article(career_id)
        discuss = get_career_discuss(career_id)
        px = lps4_public(career_id)
    except Exception:
        raise Http404

    data = dict(
        stages=stages,
        careers=careers,
        current_task=current_task,
        task_type_normal=TASK_TYPE_NORMAL,
        class_type=CLASS_TYPE_EXPERIENCE_3_1,
        teachers=teachers,
        student_works=student_works,
        articles=articles,
        discuss=discuss,
        px=px,
        lps_count=get_career_course_knowledge_task_count_interface(career_id),
    )

    return data


def lps4_index(request, career_id):
    """
    在首页点职业课程图标进任务地图
    :param request:
    :param career_id:
    :return:
    """
    # check career_id is int
    try:
        career_id = int(career_id)

        try:
            # get short_name from CAREER_ID_TO_SHORT_NAME by career_id
            short_name = CAREER_ID_TO_SHORT_NAME[career_id]
        except KeyError:
            log.warn('get CAREER_ID_TO_SHORT_NAME %s error' % career_id)
            raise Http404

    except ValueError:
        log.info('career_id is not int %s' % career_id)

        # if is not int, get real career_id from SHORT_NAME_TO_CAREER_ID
        try:
            short_name = career_id
            career_id = SHORT_NAME_TO_CAREER_ID[career_id]
        except KeyError:
            log.warn('get SHORT_NAME_TO_CAREER_ID %s error' % career_id)
            raise Http404

    if career_id <= 0:
        log.warn('career_id is not bigger than 0 %s' % career_id)
        raise Http404

    user = None
    user_id = None
    user_is_already_guided = False

    try:
        user = request.user
        if user.is_teacher():
            return redirect(reverse('home:index'))
        user_id = user.id
        user_is_already_guided = user.is_already_guided
    except Exception as e:
        pass

    _template = loader.get_template('mz_lps4/study_panel.html')

    # 如果没有登陆，或者没有在3.1和3.0的班里，找到lps3.1试学班的class_id，作为暂时的容器
    try_class_id = 0
    try:
        try_class_id = TRY_CLASS_DICT[career_id]
    except KeyError:
        log.warn('TRY_CLASS_DICT does not has key %s: ' % career_id)

    if not try_class_id:
        raise Http404
    else:
        if not is_logined(request):
            cache_data = cache.get('lps_data_cache_unlogined_%s_%s' % (0, career_id))
            if cache_data:
                """
                    命中未登陆缓存
                """
                return HttpResponse(cache_data)
            else:
                """
                    未命中未登陆缓存
                """
                # 获取未登录数据
                data = dict(get_unlogined_data(career_id),
                            class_id=try_class_id,
                            user_is_already_guided=user_is_already_guided,
                            trace_pay_type=u'未登陆',
                            trace_user_type=u'未登录',
                )

                # lps3学习信息
                stages = functions.StageTaskInterface.get_real_stage_tasks_by_class_id(try_class_id)
                # 取当前职业课
                careers = get_lps_3_1_career_info_list_interface(career_id)
                career_name = ''
                if careers:
                    career_name = careers[0]['name']
                    data["trace_career_name"] = career_name

                # 当前任务
                current_task = []
                # 对未登录的用户构造假的1v1直播
                teacher = get_lps_3_1_teacher_by_career_id_interface(career_id)  # 获取老师qq
                if teacher:
                    oneveone_meeting = generate_oneveone_meeting(teacher.get('teacher_id'))
                    data.update(dict(oneveone_meeting=oneveone_meeting))

                data.update(get_lps4_context(request, career_id).dicts[1])
                rendered = get_template_from_string(
                    html_parser.unescape(_template.render(RequestContext(request, data)))).render(
                    RequestContext(request, {
                        "careers": careers,
                        "career_id": career_id,
                        "stages": stages,
                        "current_task": current_task,
                        "task_type_normal": TASK_TYPE_NORMAL,
                    }))
                cache.set('lps_data_cache_unlogined_%s_%s' % (0, career_id), rendered, 5 * 60)
                return HttpResponse(rendered)

    student_dict = {}
    if user_id:
        student_dict = get_lps4_student_info_by_user_id_interface(user_id, career_id)

        if student_dict:
            # 跳转此学生此专业的lps3.1班（加正式班的时候需要删除免费班）
            class_type = student_dict['type']
            try:
                if class_type != CLASS_TYPE_EXPERIENCE_3_1:
                    class_id = NORMAL_CLASS_DICT[career_id]
                else:
                    class_id = TRY_CLASS_DICT[career_id]

            except KeyError:
                log.warn('get CLASS_DICT failed, career_id: %s' % career_id)
                raise Http404

            if class_id and class_type != CLASS_TYPE_EXPERIENCE_3_1:
                # 获取学生
                class_student = ClassStudents.objects.filter(student_class_id=class_id, user_id=user_id)
                if class_student:
                    class_student = class_student[0]

                    # lps学习系统数据
                    normal_lps4_data = lps4_data(user_id, class_id, career_id)

                    # 公用基础数据
                    now_time = datetime.datetime.now()

                    # 1v1班会
                    oneveone_meeting_data = get_onevone_meeting_info(user_id, career_id)

                    # 取雷达图
                    skill_radar = get_skill_radar_by_career_id_interface(career_id)

                    # 取技能树
                    stage_tree_list = get_skill_tree_by_class_id_career_id_user_id_interface(
                        class_id, career_id, user_id, normal_lps4_data['current_task_rid'])

                    # 获取老师qq
                    teacher = get_lps4_teacher_by_career_student_id_interface(career_id, user_id)

                    # 入学弹窗信息
                    enter_data = get_student_enter_data(class_student, student_dict['type'])
                    # 职业课程对象
                    px = lps4_public(career_id)

                    this_career = get_lps_3_1_career_info_list_interface(career_id)
                    career_name = ''
                    if this_career:
                        career_name = this_career[0]['name']

                    _type = get_user_study_version(user_id)
                    final_data = dict(
                        normal_lps4_data,
                        trace_career_name=career_name,
                        careers=get_lps_3_1_careers_by_user_id_interface(user_id),
                        lps_count=get_career_course_knowledge_task_count_interface(career_id),
                        class_id=class_id,
                        class_type=class_type,
                        task_type_normal=TASK_TYPE_NORMAL,
                        user_is_already_guided=True,
                        skill_radar=skill_radar,
                        stage_tree_list=stage_tree_list,
                        teacher=teacher,
                        class_student=class_student,
                        real_name=user.real_name,
                        now_time=now_time,
                        px=px,
                        trace_pay_type=_type['pay_type'],
                        trace_user_type=_type['user_type'],
                        **oneveone_meeting_data
                    )
                    final_data = dict(
                        final_data,
                        **enter_data
                    )
                    return render(request, 'mz_lps4/study_panel.html', final_data,
                                  context_instance=get_lps4_context(request, career_id))

        # 跳转lps3最近报名的正式班
        class_id = db.api.lps.student.get_lps_3_newest_normal_class_id_by_user_id_and_career_id(user_id, career_id)
        if class_id.is_error():
            log.warn(
                'get_lps_3_newest_normal_class_id_by_user_id_and_career_id is error. user_id: %s, career_id: %s' % (
                    user_id, career_id))
        else:
            class_id = class_id.result()
            if class_id:
                class_id = class_id[0]['id']
                return redirect(reverse("lps3:student_class", kwargs=dict(class_id=class_id)))

    if not try_class_id:
        # raise error
        raise Http404
    else:
        careers = get_lps_3_1_career_info_list_interface(career_id)
        career_name = ''
        if careers:
            career_name = careers[0]['name']
        _type = get_user_study_version(user_id)
        if student_dict:  # 学生是否报了该课程
            careers = get_lps_3_1_careers_by_user_id_interface(user_id)
            """
            if in class, get real stages by real user_id
            """
            st_interface = StageTaskInterface(try_class_id)
            stages = st_interface.get_student_data(user_id)
            current_task = st_interface.get_student_latest_task(user_id)
        else:
            careers = careers + get_lps_3_1_careers_by_user_id_interface(user_id)
            """
            if not in class, get stages from cache where user_id is 0
            """
            stages_cache = cache.get('lps_stages_cache_%s' % career_id)
            if stages_cache:
                stages, current_task = stages_cache
            else:
                st_interface = StageTaskInterface(try_class_id)
                stages = st_interface.get_student_data(0)
                current_task = st_interface.get_student_latest_task(0)
            cache.set('lps_stages_cache_%s' % career_id, [stages, current_task], 5 * 60)

        login_change_data_dict = {
            "careers": careers,
            "career_id": career_id,
            "stages": stages,
            "current_task": current_task,
            "task_type_normal": TASK_TYPE_NORMAL,
            "short_name": short_name,
        }

        # 获取未登录数据
        data = dict(get_unlogined_data(career_id),
                    class_id=try_class_id,
                    user_is_already_guided=user_is_already_guided)
        data.update({
            "trace_career_name": career_name,
            "trace_pay_type": _type['pay_type'],
            "trace_user_type": _type['user_type']
        })

        # 当前的1v1直播
        teacher = get_lps_3_1_teacher_by_career_id_interface(career_id)  # 获取老师qq
        if teacher:
            oneveone_meeting = generate_oneveone_meeting(teacher.get('teacher_id'))
            data.update(dict(oneveone_meeting=oneveone_meeting))

        data.update(get_lps4_context(request, career_id).dicts[1])
        rendered = html_parser.unescape(_template.render(RequestContext(request, data)))

        return HttpResponse(
            get_template_from_string(rendered).render(RequestContext(request, login_change_data_dict)))


def lps4_stage_task(request, class_id, stagetask_id):
    """
    任务详情
    :param request:
    :param class_id:
    :param stagetask_id:
    :return:
    """
    is_struct = False
    status = request.POST.get('status', 'lock')
    class_type = int(request.POST.get('class_type', CLASS_TYPE_EXPERIENCE_3_1))
    task_type = int(request.POST.get('task_type', TASK_TYPE_NORMAL))

    need_pay = class_type == CLASS_TYPE_EXPERIENCE_3_1 and task_type == TASK_TYPE_NORMAL
    try_class_lock = class_type == CLASS_TYPE_EXPERIENCE_3_1

    _template = 'mz_lps4/module/ajax_stage_lists.html'
    try:
        class_id = int(class_id)
        stagetask_id = int(stagetask_id)
    except ValueError:
        return HttpResponse(json.dumps({'status': 'fail'}))
    if class_id <= 0 or stagetask_id <= 0:
        return HttpResponse(json.dumps({'status': 'fail'}))

    user_id = None
    try:
        user_id = request.user.id
    except Exception:
        pass

    stage_task = get_object_or_404(StageTaskRelation, id=stagetask_id)

    # 如果任务是锁定的，或者其它没有用户的情况，取任务详情空架子
    if not user_id:
        is_struct = True
    # 如果任务不是锁定的，取带用户数据的任务详情
    else:
        # 如果是重修，删除ProjectRecord
        if status == 'rebuild':
            # 删除ProjectRecord，把任务状态变为rebuilding
            lps4_change_rebuild_to_rebuilding(class_id, stagetask_id, user_id)

        # 开始取
        # 判断班级有这个stage_task
        if not functions.class_has_stage_task(class_id, stagetask_id):
            return HttpResponse(json.dumps({'status': 'fail'}))
        # 取任务数据时已经排除TASK_TYPE_FREE_488
        # 乱序解锁任务球，加not_in_sequence_all。正序乱序都能进lesson
        usertasks = UserTaskRecord.objects.not_in_sequence_all().\
            filter(class_id=class_id, student_id=user_id, stage_task_id=stagetask_id)
        if not usertasks:
            is_struct = True
        else:
            usertask = usertasks[0]

            iface = functions.TaskKnowledgeInterface(class_id, stagetask_id)
            knowledges = iface.get_student_data(user_id)
            current_item = iface.get_student_item(user_id, usertask.learning_item_id)
            all_items_have_done = iface.all_items_have_done(user_id)

            data = dict(
                knowledges=knowledges,
                stagetask_id=stagetask_id,
                class_id=class_id,
                status=status,
                stage_task=stage_task,
                usertask=usertask,
                current_item=current_item,
                all_items_have_done=all_items_have_done,
                try_class_lock=try_class_lock
            )

    if is_struct:
        task_id = get_object_or_404(Task, stagetaskrelation__id=stagetask_id).id
        knowledges = functions.TaskKnowledgeInterface.get_task_knowledge_struct(task_id)

        data = dict(
            knowledges=knowledges,
            stagetask_id=stagetask_id,
            class_id=class_id,
            status=status,
            stage_task=stage_task,
            need_pay=need_pay,
            try_class_lock=try_class_lock
        )

    html = render(request, _template, data).content
    return HttpResponse(json.dumps({'status': 'success', 'html': html}))


def lps4_unlock_task(request, class_id, stagetask_id):
    """
    解锁任务
    :param request:
    :param class_id:
    :param stagetask_id:
    :return:
    """
    try:
        class_id = int(class_id)
        stagetask_id = int(stagetask_id)
    except ValueError:
        return HttpResponse(json.dumps({'status': 'fail'}))
    if class_id <= 0 or stagetask_id <= 0:
        return HttpResponse(json.dumps({'status': 'fail'}))

    try:
        user_id = request.user.id
    except Exception:
        return HttpResponse(json.dumps({'status': 'fail'}))

    # 判断class_type是试学，且学生不在班，做加班操作
    class_type = int(request.POST.get('class_type', CLASS_TYPE_EXPERIENCE_3_1))
    try:
        career_id = int(request.POST.get('career_id'))
    except (KeyError, ValueError):
        return HttpResponse(json.dumps({'status': 'fail'}))

    # 取学生
    try:
        cstudent = ClassStudents.objects.get(student_class_id=class_id, user_id=user_id)
    except Exception:
        if class_type != CLASS_TYPE_EXPERIENCE_3_1:
            return HttpResponse(json.dumps({'status': 'fail'}))
        else:
            # 加班
            teacher = db.api.lps.student.get_lps_3_1_teacher_by_career_id(career_id)
            if teacher.is_error():
                log.warn('get_lps_3_1_teacher_by_career_id is error. career_id: %s' % career_id)
                return HttpResponse(json.dumps({'status': 'fail'}))
            else:
                teacher_id = teacher.result()['teacher_id']

            time_now = datetime.datetime.now()
            insert_stu = db.api.lps.student.insert_user_to_try_class(class_id, user_id, career_id, teacher_id, time_now)
            if insert_stu.is_error():
                log.warn('insert_user_to_class is error.  user_id: %s, career_id: %s' % (user_id, career_id))
                return HttpResponse(json.dumps({'status': 'fail'}))

            # 插入了之后再次取学生
            try:
                cstudent = ClassStudents.objects.get(student_class_id=class_id, user_id=user_id)
            except Exception:
                log.warn('get cstudent is error.  user_id: %s, class_id: %s' % (user_id, class_id))
                return HttpResponse(json.dumps({'status': 'fail'}))

    # 全款用户休学状态
    if cstudent.is_full_payment_user and cstudent.is_pause:
        return HttpResponse(json.dumps({'status': 'fail', 'msg': u'休学中,无法解锁'}))

    # 判断班级有这个任务
    if not functions.class_has_stage_task(class_id, stagetask_id):
        return HttpResponse(json.dumps({'status': 'fail'}))

    # 用户是否可以开启新任务
    iface = functions.StageTaskInterface(class_id)
    iface.load_student_data(user_id)
    flag, reason = iface.student_can_unlock_task(user_id, stagetask_id)
    userstage = iface.get_student_stage_by_stagetask(user_id, stagetask_id)
    if flag:
        # 写入用户记录
        # 乱序解锁任务球，加not_in_sequence_all
        try:
            usertask = UserTaskRecord.objects.not_in_sequence_all().\
                get(class_id=class_id, stage_task_id=stagetask_id, student_id=user_id)
        except Exception:
            usertask = UserTaskRecord()
        usertask.class_id = class_id
        usertask.stage_task_id = stagetask_id
        usertask.student_id = user_id
        usertask.is_in_sequence = 1
        usertask.save()

        if userstage and userstage.is_undo():  # 阶段第一个任务
            history = StudyHistory()
            history.class_id = class_id
            history.student_id = user_id
            history.content = u"我开始了[%s]的学习" % userstage.name
            history.save()
        if class_type != CLASS_TYPE_EXPERIENCE_3_1:
            curr_task = iface.get_student_task(user_id, stagetask_id)
            source = userstage.name + '-' + curr_task.task_name
            create_coach_info_unlock_task(request.user, source, career_id, curr_task.task_id)
        return HttpResponse(json.dumps({'status': 'success'}))
    return HttpResponse(json.dumps({'status': 'fail'}))


def update_is_already_guided(request):
    """
    更新用户的is_already_guided状态
    :param request:
    :return:
    """
    user = request.user
    if user.is_authenticated():
        try:
            user.is_already_guided = True
            user.save()
        except (AttributeError, NotImplementedError, ValueError) as e:
            log.warn('DEF update_is_already_guided %s' % str(e))
    return HttpResponse(json.dumps({'status': 'success'}))


@login_required
def task_score_message(request):
    """
    进入任务面板，确定是否显示任务分数消息。
    :param request:
    :return:
    """
    template = 'mz_lps4/popup/ajax_task_score.html'
    if request.method != 'GET':
        return JsonResponse({'status': False, 'data': 'wrong method'})
    user_id = request.user.id
    if user_id:
        try:
            messages = MyMessage.objects.filter(userB=user_id, action_type=11, is_new=True).order_by('date_action')
            if not messages.exists():
                data = {'status': False, 'data': 'No message'}
            else:
                data = {'status': True, 'data': []}
                for each_message in messages:
                    try:
                        user_task = UserTaskRecord.objects.get(pk=each_message.action_id)
                        passed = True if user_task.score in ['S', 'A', 'B', 'C'] else False
                        time_consumption = (user_task.done_time - user_task.created).seconds - user_task.paused_seconds
                        time_excellent = True if time_consumption <= user_task.stage_task.task.excellent_time * 24 * 3600 \
                                                 and user_task.score == 'A' else False
                        data['data'].append(
                            render_to_string(
                                template,
                                {
                                    'task_name': user_task.stage_task.task.name,
                                    'class_id': user_task.class_id,
                                    'stage_task_id': user_task.stage_task.pk,
                                    'passed': passed, 'task_score': user_task.score,
                                    'time_excellent': time_excellent,
                                    'gift': user_task.stage_task.task.gift
                                },
                                context_instance=RequestContext(request)))

                    except Exception as msg:
                        log.error(msg)
                messages.update(is_new=False)  # update messages.
        except Exception as msg:
            log.error(msg)
            data = {'status': False, 'data': str(msg)}
    else:
        data = {'status': False, 'data': 'No enough parameters'}
    return JsonResponse(data)
