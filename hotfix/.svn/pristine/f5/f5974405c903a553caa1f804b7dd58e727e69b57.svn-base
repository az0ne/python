# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect

from django.template.context import RequestContext
from django.template.loader import get_template

from mz_common.decorators import teacher_or_eduadmin_required
from mz_eduadmin.students.interface import ClassStudentsInterface

from mz_lps3.functions_nj import UserTaskInfo
from mz_lps4.class_dict import LPS4_DICT
from mz_user.models import UserProfile
from mz_lps3.functions_zy import ExportStudentInfo

from views_teacher_gt import *
import db.api.coach.coach


def teacher_classmeeting(request, class_id):
    class_meeting_dict = functions.get_teacher_classmeetings_by_class_id(class_id)
    datetime.datetime.now().weekday()
    content = {"class_meeting_dict": class_meeting_dict, 'now_month': datetime.datetime.now().month,
               'now_year': datetime.datetime.now().year, 'class_id': class_id}
    return render(request, 'mz_lps3/teacher/live_meeting.html', content)


def teacher_attendance(request, class_id, classmeeting_id):
    try:
        class_meeting = ClassMeeting.objects.get(id=classmeeting_id)
    except:
        raise Http404
    setattr(class_meeting, 'd_week', functions.get_weekday(class_meeting.startline.weekday()))
    setattr(class_meeting, 'd_date', class_meeting.startline.strftime("%m-%d"))
    setattr(class_meeting, 'd_time', class_meeting.startline.strftime("%H:%M"))

    punctual_user_lst, late_user_lst, absent_user_lst, _ = functions.get_attendance_info(class_meeting, class_id=class_id,
                                                                                      is_update=False)
    punctual_user_count = len(punctual_user_lst)
    late_user_count = len(late_user_lst)
    absent_user_count = len(absent_user_lst)
    return render(request, 'mz_lps3/teacher/div_attendance.html', locals())


class CmpMethod:
    """学生排序方法"""

    @staticmethod
    def cmp_join(x, y):
        """入班时间排序"""
        x_join_in_class_time = x['join_in_class_timestamp']
        y_join_in_class_time = y['join_in_class_timestamp']
        if not x_join_in_class_time:
            return -1
        if not y_join_in_class_time:
            return 1
        if x_join_in_class_time < y_join_in_class_time:
            return -1
        elif x_join_in_class_time > y_join_in_class_time:
            return 1
        else:
            return 0

    @staticmethod
    def cmp_rank(x, y):
        """排名排序"""
        x_rank = x['class_rank']
        y_rank = y['class_rank']
        if x_rank is None:
            return 1
        if y_rank is None:
            return -1
        if x_rank < y_rank:
            return -1
        elif x_rank > y_rank:
            return 1
        else:
            return 0

    @staticmethod
    def cmp_pay(x, y):
        """支付情况排序"""
        x_pay = x['is_full_payment']
        y_pay = y['is_full_payment']
        if x_pay < y_pay:
            return 1
        elif x_pay > y_pay:
            return -1
        else:
            return CmpMethod.cmp_rank(x, y)


@teacher_required
def teacher_class(request, class_id):
    teacher_id = request.user.id
    class_id = int(class_id)  # 测试班级请用111
    try:
        tclass = Class.objects.xall().get(id=class_id, teachers=request.user, lps_version='3.0')
        csi = ClassStudentsInterface(class_id)
        data = csi.data
    except:
        raise Http404
    # 班级关闭倒计时
    if tclass.meeting_enabled:
        now = datetime.datetime.now()
        end_time = (tclass.meeting_start or now) + datetime.timedelta(days=tclass.meeting_duration or 90)
        class_time_left = (end_time - now).days + 1
    class_meeting_enabled = tclass.meeting_enabled

    # 学生总数,,jackie-20160517  改为只算非退学学生人数
    # students_count = tclass.current_student_count
    students_count = len(list(s for s in data if not s.get('status_is_quit')))


    iface = functions.StageTaskInterface(class_id)
    stages = iface.get_stages()

    _students = tclass.students.all()
    iface.load_students_data(list(student.id for student in _students))
    total_progress = iface.get_class_total_progress()

    s_order = request.GET.get('s_order', 'pay')
    if s_order == 'join':  # 入学时间
        data.sort(cmp=CmpMethod.cmp_join)
    elif s_order == 'rank':  # 排名
        data.sort(cmp=CmpMethod.cmp_rank)
    else:  # 缴费
        data.sort(CmpMethod.cmp_pay)

    html_class_meeting = render_class_meeting(request, class_id, teacher_id)
    classcodings = json.dumps(functions.get_classcoding_lst(class_id))


    return render(request, "mz_lps3/teacher/class_index.html", locals())


@teacher_required
def start_class(request, class_id):
    """开启班级"""
    teacher = request.user
    class_id = int(class_id)  # 测试班级请用111
    try:
        tclass = Class.objects.xall().get(id=class_id, teachers=teacher, lps_version='3.0')
    except:
        raise Http404
    assert isinstance(tclass, Class)
    if not tclass.meeting_enabled:
        @transaction.atomic
        def _batch():
            now = datetime.datetime.now()
            tclass.meeting_enabled = True
            tclass.meeting_start = now
            tclass.save()
            for cstudent in ClassStudents.objects.filter(student_class_id=class_id):
                if cstudent.deadline:
                    if cstudent.created > datetime.datetime(2016, 04, 01):
                        cstudent.deadline = now + datetime.timedelta(days=15)
                    else:
                        cstudent.deadline = now + datetime.timedelta(days=30)
                    cstudent.save()

        _batch()
    return redirect(reverse("lps3:teacher_class", kwargs=dict(class_id=class_id)))


@teacher_required
def course_syllabus(request, class_id):
    """查看教学大纲"""
    try:
        tclass = Class.objects.xall().get(id=class_id)
    except Class.DoesNotExist:
        raise Http404
    iface = functions.StageTaskInterface(class_id)
    stages = iface.get_course_syllabus()
    return render(request, "mz_lps3/teacher/syllabus.html", locals())


@teacher_or_eduadmin_required
def student_info(request, class_id, student_id):
    info = ExportStudentInfo(class_id=class_id, student_id=student_id).student_info()
    return render(request, "mz_lps3/teacher/student_info.html", locals())


@teacher_or_eduadmin_required
def export_student_info(request, class_id, student_id):
    return ExportStudentInfo(class_id=class_id, student_id=student_id).export_excel_for_studentinfo()


def student_stage_div(request, class_id, student_id, stage_id):
    """学生阶段信息"""
    class_id = int(class_id)
    student_id = int(student_id)
    stage_id = int(stage_id)

    user = get_object_or_404(UserProfile, id=student_id)
    student_name = user.real_name if user.real_name else user.username

    st_interface = functions.StageTaskInterface(class_id)
    st_interface.load_student_data(student_id)
    stage = st_interface.get_student_stage(student_id, stage_id)
    tasks = stage.get_tasks()
    # 获取学生知识点item记录
    student_stage_info = functions.get_class_student_stage_info_1(class_id, student_id, stage_id)
    for task in stage.get_tasks():
        assert isinstance(task, UserTaskInfo)
        setattr(task, 'extra_info', student_stage_info.get(task.id, []))
        stage_task_id = task.task_rid
        if LPS4_DICT.get(class_id):
            source_location = json.dumps(dict(
                project=dict(
                    class_id=int(class_id),
                    stage_task_id=int(stage_task_id),
                    item_id=0,
                    student_id=int(student_id)
                )
            ))
            result = db.api.coach.coach.get_project_coach(LPS4_DICT.get(class_id), student_id, request.user.id,
                                                          source_location, False)
            if result.result():
                setattr(task, 'is_coach', True)
                setattr(task, 'coach_id', result.result()['id'])

            # 小项目制作
            for extra_info_v in task.extra_info:
                if extra_info_v.get("obj_type") == "PROJECT":
                    source_location = json.dumps(dict(
                            project=dict(
                                class_id=int(class_id),
                                stage_task_id=int(stage_task_id),
                                item_id=extra_info_v.get("item_id"),
                                student_id=int(student_id)
                            )
                    ))
                    result = db.api.coach.coach.get_project_coach(LPS4_DICT.get(class_id), student_id, request.user.id,
                                                                  source_location, False)
                    if result.result():
                        extra_info_v["is_coach"] = True
                        extra_info_v["coach_id"] = result.result()['id']

    return render(request, "mz_lps3/teacher/div_student_stage.html", locals())


# 20160331老师端优化去掉休学入口
# @teacher_required
# def pause_student_studying(request, class_id, student_id, to_status):
#     """暂停学生学习"""
#     cstudent = get_object_or_404(ClassStudents, student_class_id=class_id, user_id=student_id)
#     if cstudent.is_pause:  # 暂停状态
#         assert to_status == 'resume'
#     else:
#         assert to_status == 'pause'
#     now = datetime.datetime.now()
#
#     @transaction.atomic()
#     def _pause_studying():
#         cstudent.is_pause = True
#         cstudent.pause_datetime = now
#         cstudent.pause_reason = u"老师触发暂停,teacherID:%s" % request.user.id
#         cstudent.save()
#         for utask in UserTaskRecord.objects.filter(
#                 class_id=class_id, student_id=student_id, status__in=('DOING', 'REDOING')):
#             utask.is_pause = True
#             utask.pause_datetime = now
#             utask.save()
#
#     @transaction.atomic()
#     def _resume_studying():
#         cstudent.is_pause = False
#         cstudent.restore_datetime = now
#         cstudent.save()
#         for utask in UserTaskRecord.objects.filter(
#                 class_id=class_id, student_id=student_id, is_pause=True):
#             utask.is_pause = False
#             delta = now - utask.pause_datetime
#             utask.paused_seconds = delta.days * 24 * 3600 + delta.seconds + (utask.paused_seconds or 0)
#             utask.pause_datetime = now
#             utask.save()
#
#     def send_message(mobile, course_name):
#         import datetime
#         from django.conf import settings
#         from mz_common.models import MobileVerifyRecord
#         from utils.sms_manager import send_sms, get_templates_id
#         start = datetime.datetime.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         if MobileVerifyRecord.objects.filter(created__gt=start, mobile=mobile).count() < settings.SMS_MAX_COUNT_MOBILE:
#             try:
#                 send_sms.delay(settings.SMS_APIKEY, get_templates_id('studying_paused'),
#                          mobile.encode('utf-8'), course_name.encode('utf-8'))
#             except Exception, e:
#                 print e
#
#     if to_status == 'pause':  # 暂停
#         _pause_studying()
#         if cstudent.user.mobile:
#             course_name = cstudent.student_class.career_course.name
#     else:  # 恢复学习
#         _resume_studying()
#     return redirect(reverse("lps3:teacher_class", kwargs=dict(class_id=class_id)))


def render_class_meeting(request, class_id, teacher_id):
    """渲染班会列表div"""
    classmeeting_lst = functions.get_classmeeting_list(class_id, teacher_id)
    is_classmeeting_video = True if ClassMeeting.objects.filter(classmeetingrelation__class_id=class_id,
                                                                status=1).exists() else False
    template = get_template("mz_lps3/teacher/div_class_meeting.html")
    html = template.render(RequestContext(request, locals()))
    return html
