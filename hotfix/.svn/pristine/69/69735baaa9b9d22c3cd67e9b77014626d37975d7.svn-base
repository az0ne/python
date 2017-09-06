# -*- coding: utf-8 -*-

import os
import time

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
# import django
#
# django.setup()

import datetime
from django.conf import settings
from django.db import connections
from django.shortcuts import get_object_or_404, Http404

from utils.serializers import SimpleModelSerializer
from mz_user.models import UserUnlockStage, UserJobInfo
from mz_lps.models import Class, Project
from mz_course.models import Stage
from mz_lps3.models import UserTaskRecord, TaskKnowledgeRelation, StageTaskRelation, UserGiftRecord, \
    ClassRank, ClassMeetingRelation, Task
from mz_usercenter.student.interface_study import get_study_base, batch_get_study_base
from mz_usercenter.student.interface_job_info import get_study_goal

T_UNLOCK_ERR_NOT_PAID = u"该阶段课程未购买!"
T_UNLOCK_ERR_PREVIOUS_NOT_DONE = u"请先完成前面的任务!"
T_UNLOCK_ERR_LAST_CHECK_ALL = u"等前面所有任务都通过,再来开启最后一个任务!"


def exec_sql(sql, params=None, database="default"):
    cursor = connections[database].cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()


def calc_timeleft(dt, days, paused_seconds, is_pause=False, pause_datetime=None):
    """计算 倒计时
    :param dt: 起始时间
    :param days:限定天数
    :param paused_seconds
    :return:秒数
    """
    if is_pause and pause_datetime:  # 当前暂停状态
        delta = pause_datetime - dt
    else:
        delta = datetime.datetime.now() - dt
    assert isinstance(delta, datetime.timedelta)
    seconds_used = delta.days * 3600 * 24 + delta.seconds
    return days * 3600 * 24 - seconds_used + paused_seconds


def calc_done_type(start, end, expect, min, paused_seconds):
    """计算完成类型
    :param start: 起始时间
    :param end: 结束时间
    :param expect: 预期时长
    :return: "perfect","timeout"
    """
    assert isinstance(start, datetime.datetime)
    assert isinstance(end, datetime.datetime)
    delta = end - start
    if delta.days * 24 * 3600 + delta.seconds - paused_seconds > expect * 24 * 3600:
        return "timeout"
    elif delta.days * 24 * 3600 + delta.seconds - paused_seconds < min * 24 * 3600:
        return "quickly"
    else:
        return "normal"


def time_cost(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        print func.func_name, time.time() - start
        return ret

    return wrapper


def class_has_stage_task(class_id, stagetask_id):
    sql = """select _str.id
            from mz_lps3_stagetaskrelation as _str,
                 mz_course_stage as _stage,
                 mz_lps_class as _class
            where _str.id=%s
            and _class.id=%s
            and _stage.id = _str.stage_id
            and _class.career_course_id=_stage.career_course_id;
         """ % (stagetask_id, class_id)
    return bool(exec_sql(sql))


def user_has_paid_for_stage(student_id, stage_id):
    return UserUnlockStage.objects.filter(user_id=student_id, stage_id=stage_id).exists()


def user_can_unlock_task(class_id, student_id, stagetask_id):
    """
    判断用户是否可以解锁新的任务
    :param class_id:id of Class
    :param student_id: 学生id
    :param stagetask_id: id of StageTaskRelation
    :return: (True,'ok') or (False,reason)
    """
    iface = StageTaskInterface(class_id)
    iface.get_student_data(student_id)
    stagetask = iface.get_student_task(student_id, stagetask_id)  # 可能为None
    assert isinstance(stagetask, UserTaskInfo)

    if stagetask == iface.get_the_last_task(student_id):  # 最后一个任务,需要前面所有已经解锁
        flag = True
        for task in list(iface.iter_student_tasks(student_id))[:-1]:
            if task.is_pass:
                pass
            else:
                flag = False
        if not flag:
            return False, T_UNLOCK_ERR_LAST_CHECK_ALL

    if not stagetask.is_locked:
        return False, "repeat"
    if stagetask.can_be_unlocked():
        if iface.is_guide_task(stagetask.task_id):
            return True, u"新手引导任务,可以开启"
        return True, u"可以开启"
    else:
        if not stagetask.is_paid:
            return False, T_UNLOCK_ERR_NOT_PAID
        return False, T_UNLOCK_ERR_PREVIOUS_NOT_DONE


def get_student_doing_tasks_timeleft(class_id, student_id):
    """获取学生正在进行的任务及倒计时"""
    ret = list()
    objs = UserTaskRecord.objects \
        .filter(class_id=class_id, student_id=student_id, status="DOING") \
        .values("stage_task__task__id", "stage_task__task__expect_time", "stage_task__task__name",
                "created", "is_pause", "paused_seconds")
    for obj in objs:
        if obj.get('is_pause'):  # 暂停中的不算
            continue
        task_name = obj.get("stage_task__task__name")
        task_id = obj.get("stage_task__task__id")
        task_expect_time = obj.get("stage_task__task__expect_time")
        created = obj.get("created")
        paused_seconds = obj.get('paused_seconds')
        timeleft = calc_timeleft(created, task_expect_time, paused_seconds)
        ret.append(dict(task_id=task_id, task_name=task_name, timeleft=timeleft))
    return ret


def get_class_students_show_info(class_id, ccourse_id):
    """获取班级内学生展示信息
    :param class_id:班级id
    :param ccourse_id:职业课程id
    update：个人中心改版---lewis
    """
    sql = """
    SELECT
        student.id,
        student.real_name,
        student.email AS real_email,
        student.mobile AS real_mobile,
        cstudent.is_pause,
        cstudent.pause_datetime,
        cstudent.deadline,
        province.`name` AS province_name,
        city.`name` AS city_name,
        jobinfo.`degree` AS degree,
        cstudent.is_employment_contract AS is_employment_contract,
        _institute.name AS institute_name,
        cstudent.created,
        cstudent.status,
        cstudent.quit_datetime
    FROM
        mz_user_userprofile AS student
    INNER JOIN mz_lps_classstudents AS cstudent ON student.id = cstudent.user_id
    LEFT JOIN mz_user_citydict AS city ON student.city_id = city.id
    LEFT JOIN mz_user_provincedict AS province ON province.id = city.province_id
    INNER JOIN mz_lps_class AS _class ON cstudent.student_class_id = _class.id
    LEFT JOIN mz_course_careercourse AS _c_course ON _class.career_course_id = _c_course.id and _c_course.id = %s
    LEFT JOIN mz_course_institute AS _institute ON _c_course.institute_id = _institute.id
    LEFT JOIN mz_user_userjobinfo AS jobinfo ON jobinfo.user_id = student.id and jobinfo.career_course_id = _c_course.id
    WHERE
        cstudent.student_class_id = %s
    """ % (ccourse_id, class_id)
    result = dict()
    for student_id, real_name, real_email, real_mobile, is_pause, \
        pause_datetime, deadline, province_name, city_name, degree, is_employment_contract, \
        institute_name, created, status, quit_time in exec_sql(sql):
        result[student_id] = dict(
            real_name=real_name,  # 真实姓名
            real_email=real_email,  # 校验email
            real_mobile=real_mobile,  # 校验手机号
            is_pause=True if is_pause else False,  # 是否为暂停
            pause_datetime=pause_datetime,  # 暂停时间
            deadline=deadline,  # 试学到期时间
            province=province_name,
            city=city_name,  # 城市
            study_goal=get_study_goal(is_employment_contract),  # 学习目标
            study_base='',  # 学习基础,,,下面注入
            degree=UserJobInfo.DEGREES.get(degree, ''),  # 学历
            join_in_class_time=created,  # 加入班级时间
            student_status=status,  # 学生状态
            quit_time=quit_time,  # 退学时间
        )
    user_ids = result.keys()
    if user_ids:
        tmp = batch_get_study_base(user_ids, institute_name)
        for k, v in result.iteritems():
            result[k]['study_goal'] = ';'.join(tmp.get(k, []))
    return result


def _get_class_students_payment(class_id, student_id=None):
    """获取班级内学生支付信息,
    :param class_id:班级id
    :param student_id: None-->取班级全部学生的, int-->指定学生的
    """
    sql = """
    SELECT cstudents.user_id,stage.id,ustage.id,cstudents.deadline
    FROM (mz_lps_classstudents AS cstudents,
    mz_lps_class AS _class,
    mz_course_careercourse AS ccourse,
    mz_course_stage AS stage)
    LEFT JOIN mz_user_userunlockstage AS ustage ON ustage.user_id = cstudents.user_id AND ustage.stage_id = stage.id
    WHERE cstudents.student_class_id = %s
    %s
    AND _class.id = cstudents.student_class_id
    AND _class.lps_version = '3.0'
    AND ccourse.id = _class.career_course_id
    AND stage.career_course_id = ccourse.id
    AND stage.lps_version = '3.0'
    ORDER BY cstudents.user_id
    """ % (class_id, '' if student_id is None else 'AND cstudents.user_id=%s' % student_id)
    return exec_sql(sql)


def get_class_students_payment(class_id, student_id=None):
    """
    获取班级学生的支付信息
    """
    data = _get_class_students_payment(class_id, student_id)
    result = dict()
    for student_id, stage_id, unlock_id, deadline in data:
        result.setdefault(student_id, dict())
        result[student_id][stage_id] = (False if unlock_id is None else True) or not bool(deadline)
    return result


def get_class_students_full_payment(class_id, student_id=None):
    """获取班级内学生支付信息,全款或试学
    :param class_id: 班级id
    """
    result = dict()
    for info in _get_class_students_payment(class_id, student_id):
        student_id, stage_id, unlock_id, deadline = info
        result.setdefault(student_id, True)
        if unlock_id is None:
            result[student_id] = False or not bool(deadline)
    return result


def get_class_students_latest_rank(class_id):
    """获取最新排名"""
    # 先取出最后一次班会id
    the_last_meeting = ClassMeetingRelation.objects.filter(
        class_id=class_id, class_meeting__student_id=None, class_meeting__is_temp=False,
        class_meeting__status=1).order_by("-class_meeting__startline").first()
    if the_last_meeting is None:
        return {}
    result = dict()
    objs = ClassRank.objects.filter(class_id=class_id, classmeeting_id=the_last_meeting.class_meeting_id)
    for obj in objs:
        result[obj.student_id] = obj.rank
    return result


def get_class_student_stage_info_1(class_id, student_id, stage_id):
    """
    获取班级学生阶段面板信息(仅PROJECT,TEST)
    :param class_id:班级id
    :param student_id:学生id
    :param stage_id:阶段id
    """
    sql = """
    SELECT
        uitem.user_task_record_id AS utask_id,
        uitem.id AS uitem_id,
        item.id AS item_id,
        item.obj_type AS item_obj_type,
        item.obj_id AS item_obj_id,
        exam.title AS item_obj_name,
        uitem.`status` AS uitem_status,
        upaper.accuracy AS upaper_accuracy
    FROM
        (
            mz_lps3_stagetaskrelation AS str,
            mz_lps3_taskknowledgerelation AS tkr,
            mz_lps3_knowledgeitem AS item,
            mz_lps3_userknowledgeitemrecord AS uitem,
            mz_lps3_usertaskrecord AS utask
        )
    LEFT JOIN mz_lps_examine AS exam ON exam.id = item.obj_id
    LEFT JOIN mz_lps_examinerecord AS uexam ON uexam.student_id = %(student_id)s
    AND uexam.examine_id = exam.id
    LEFT JOIN mz_lps_paperrecord AS upaper ON upaper.paper_id = item.obj_id
    AND upaper.examinerecord_ptr_id = uexam.id
    WHERE
        str.stage_id = %(stage_id)s
    AND tkr.task_id = str.task_id
    AND item.parent_id = tkr.knowledge_id
    AND item.id = uitem.knowledge_item_id
    AND item.obj_type IN ("PROJECT", "TEST")
    AND uitem.knowledge_item_id = item.id
    AND uitem.user_task_record_id = utask.id
    AND utask.stage_task_id = str.id
    AND utask.class_id = %(class_id)s
    AND utask.student_id = %(student_id)s
    AND utask.is_in_sequence = 1
    ORDER BY
        str.`index`,
        tkr.`index`,
        item.`index`
    """ % dict(student_id=student_id, class_id=class_id, stage_id=stage_id)
    result = dict()
    for utask_id, uitem_id, item_id, item_obj_type, item_obj_id, \
        item_obj_name, uitem_status, upaper_accuracy in exec_sql(sql):
        if uitem_status != 'DONE':
            continue
        result.setdefault(utask_id, list())
        result[utask_id].append(
            dict(
                item_id=item_id,
                uitem_id=uitem_id,
                uitem_status=uitem_status,
                obj_type=item_obj_type,
                obj_id=item_obj_id,
                obj_name=item_obj_name,
                upaper_accuracy=int(round(upaper_accuracy, 2) * 100) if upaper_accuracy else 0
            )
        )
    return result


class UserStageInfo(object):
    """用户阶段信息"""

    def __init__(self, class_id, user_id, id, name, class_type=Class.CLASS_TYPE_NORMAL):
        self.class_id = class_id
        self.user_id = user_id  # id of UserProfile
        self.id = id  # id of Stage
        self.name = name  # name of Stage
        self.tasks = []
        self.class_type = class_type
        self._is_paid = None  # 是否已支付

    def set_paid(self, flag=True):
        self._is_paid = flag
        for task in self.tasks:
            task.set_paid(flag)

    @property
    def is_paid(self):
        if self._is_paid is None:
            self._is_paid = user_has_paid_for_stage(self.user_id, self.id)
        return self._is_paid

    def get_tasks(self):
        return self.tasks

    def count_task_finished(self):
        """获取用户任务已完成数量"""
        return sum(1 for task in self.tasks if task.is_done or task.is_pass)

    def count_task_done(self):
        """"""
        return sum(1 for task in self.tasks if task.is_done)

    def count_tasks(self):
        return len(self.tasks)

    def get_first_task(self):
        return self.tasks[0]

    def add_task_struct_data(self, data):
        usertaskinfo = UserTaskInfo(self.class_id, class_type=self.class_type)
        usertaskinfo.load_struct_data(data)
        usertaskinfo.set_paid(self._is_paid)
        self.tasks.append(usertaskinfo)

    def is_pass(self):
        """阶段最后一个任务通过,视为阶段通过"""
        if not self.tasks:  # 阶段无任务
            return True
        if self.tasks[-1].is_pass:
            return True
        return False

    def is_finished(self):
        """阶段内所有任务为DONE,PASS,视为阶段完成"""
        if not self.tasks:
            return True
        return not False in (task.is_done or task.is_pass for task in self.tasks)

    def had_finished(self):
        """DONE,PASS,FAILED"""
        if not self.tasks:
            return True
        return not False in (task.is_done or task.is_pass or task.is_fail for task in self.tasks)

    def is_going(self):
        """阶段正在进行中"""
        for task in self.tasks[::-1]:
            if not task.is_pass:  # 还未通过:包括(未解锁,正在做,已做完正等老师打分)
                return True
        return False

    def has_going(self):
        for task in self.tasks:
            if not task.is_locked:
                return True
        return False

    def is_undo(self):
        return False not in (task.is_locked for task in self.tasks)

    def has_failed_task(self):
        """有未通过任务"""
        for task in self.tasks:
            if task.is_fail:
                return True
        return False


class UserTaskInfo(object):
    """
    属性:
    task_('rid', 'rname', 'index', 'name', 'id', 'expect_time',
            'excellent_time')
    id,status,score,created,is_pause,pause_datetime,paused_seconds
    done_time,stage_task_id,student_id,class_id
    """

    def __init__(self, class_id, class_type=Class.CLASS_TYPE_NORMAL):
        self.class_id = class_id
        self.class_type = class_type
        self.id = None  # id of UserTaskRecord 当加载用户数据时会被覆盖
        self.status = None  # 状态,当加载用户数据时会被覆盖

        self._gift_flag = None  # 是获得有奖品
        self._can_be_unlocked = None  # 是否可开启,针对锁定的任务 True or False
        self._progress = None  # int
        self._timeleft = None  # int
        self._done_type = None  #
        self._focus = None  # 当前焦点
        self._is_paid = None  # 是否支付
        self._has_received_gift = None  # 是否收到礼物

    def load_struct_data(self, task_data):
        """加载任务的结构数据"""
        for k, v in task_data.iteritems():
            setattr(self, "task_%s" % k, v)

    def load_user_data(self, user_task_data):
        """加载用户记录数据"""
        for k, v in user_task_data.iteritems():
            setattr(self, k, v)

    def set_can_be_unlocked(self, flag):
        """设置可解锁状态"""
        assert flag in (True, False)
        self._can_be_unlocked = flag

    def can_be_unlocked(self):
        """是否可解锁"""
        return self._can_be_unlocked

    def get_timeleft(self):
        """获取剩余时长"""
        if self._timeleft is None:
            self._timeleft = calc_timeleft(self.created, self.task_expect_time, self.paused_seconds,
                                           self.is_pause, self.pause_datetime)
        return self._timeleft

    def has_received_gift(self):
        """是否收到礼物"""
        if self._has_received_gift is None:
            self._has_received_gift = UserGiftRecord.objects.filter(
                student_id=self.student_id, class_id=self.class_id, gift_id=self.task_gift_id).exists()
        return self._has_received_gift

    def set_progress(self, progress):
        """设置进度"""
        self._progress = progress

    def get_progress(self):
        """获取进度"""
        if self._progress is None:
            iface = TaskKnowledgeInterface(self.class_id, self.task_rid, self.task_id, class_type=self.class_type)
            assert isinstance(iface, TaskKnowledgeInterface)
            iface.load_student_data(self.student_id)
            self.set_progress(iface.get_utask_progress(self.student_id))
        return self._progress

    def set_focus(self, flag=True):
        """设置焦点"""
        self._focus = flag

    def set_paid(self, flag):
        self._is_paid = flag

    @property
    def is_paid(self):
        return self._is_paid

    @property
    def is_focus(self):
        return self._focus

    @property
    def is_locked(self):
        """判断是否为锁定状态,即无用户信息"""
        return self.id is None

    def get_done_type(self):
        """获取完成类型 提前完成;超时完成"""
        if self._done_type is None:
            self._done_type = calc_done_type(
                self.created, self.done_time, self.task_expect_time,
                self.task_excellent_time, self.paused_seconds)
        return self._done_type

    @property
    def _done_quickly(self):
        return self.get_done_type() == "quickly"

    @property
    def _done_timeout(self):
        return self.get_done_type() == "timeout"

    @property
    def task_show_status(self):
        """任务显示状态
        1.正在做(倒计时)
        2.正在做(已超时)
        3.已做完(待打分)
        4.已通过(已打分)
        5.已通过(perfect),,,获取了礼物
        6.已通过(超时完成)
        7.未通过
        8.重修中
        """
        if self.is_fail:
            return 7
        elif self.is_redoing:
            return 8
        elif self.is_doing and self.get_timeleft() > 0:
            return 1
        elif self.is_doing and self.get_timeleft() <= 0:
            return 2
        elif self.is_done:
            return 3
        # 获取了礼物
        elif not self.is_locked and self.has_received_gift():
            return 5
        elif self.is_pass and self._done_timeout:
            return 6
        elif self.is_pass:
            return 4
        else:
            return -1

    @property
    def is_doing(self):
        return self.status == "DOING"

    @property
    def is_done(self):
        return self.status == "DONE"

    @property
    def is_pass(self):
        return self.status == "PASS"

    @property
    def is_fail(self):
        return self.status == "FAIL"

    @property
    def is_redoing(self):
        return self.status == "REDOING"


class UserKnowledgeInfo(object):
    """
    rid,name,index,knowledge_id,task_id
    """

    def __init__(self):
        self.user_kid = None
        self.items = list()

    def load_struct_data(self, data):
        for k, v in data.iteritems():
            if k == "items":
                self.add_item_struct_data(v)
                continue
            setattr(self, k, v)

    def get_items(self):
        return self.items

    def add_item_struct_data(self, data):
        """
        添加知识点item结构数据
        :param data: list
        """
        for d in data:
            item = UserKnowledgeItemInfo()
            item.load_struct_data(d)
            self.items.append(item)
        self.items.sort(key=lambda x: x.index)

    @property
    def is_focus(self):
        return True in (item.is_focus for item in self.items)

    @property
    def is_done(self):
        """知识点开始"""
        return False not in (item.is_done2 for item in self.items)

    @property
    def is_undo(self):
        """知识点未开始"""
        return False not in (item.is_undo for item in self.items)


class UserKnowledgeItemInfo(object):
    """
    KnowledgeItem 所有 字段信息都打进来了
    u_id,u_created,u_status,u_done_time
    """

    def __init__(self):
        self.u_id = None
        self._can_be_unlocked = None
        self._is_focus = None

    def load_struct_data(self, data):
        for k, v in data.iteritems():
            setattr(self, k, v)

    def load_user_data(self, data):
        for k, v in data.iteritems():
            setattr(self, "u_%s" % k, v)

    def get_name(self):
        if self.obj_type == "LESSON":
            return self.lesson_name
        else:
            return self.exam_title

    def get_video_length(self):
        """视频长度"""
        try:
            length = int(self.lesson_video_length)
            return "%d:%02d" % (length / 60, length % 60)
        except:
            return "00:00"

    def get_quiz_count(self):
        """测试题目数"""
        if self.obj_type == "TEST":
            return self.quiz_count

    def get_expect_time(self):
        """测试时长"""
        if self.obj_type == "TEST":
            return self.expect_time

    def set_can_be_unlocked(self, flag):
        self._can_be_unlocked = flag

    def can_be_unlocked(self):
        return self._can_be_unlocked

    def set_focus(self, flag=True):
        self._is_focus = flag

    @property
    def is_focus(self):
        return self._is_focus

    @property
    def is_lesson(self):
        return getattr(self, "obj_type", None) == "LESSON"

    @property
    def is_project(self):
        return getattr(self, "obj_type", None) == "PROJECT"

    @property
    def is_undo(self):
        return self.u_id is None

    @property
    def is_done(self):
        return getattr(self, "u_status", None) == "DONE"

    @property
    def is_doing(self):
        if self.is_lock: return False
        return self.u_status == "DOING"

    @property
    def is_done2(self):
        if self.obj_type == "LESSON":
            return True
        return self.is_done

    @property
    def is_doing(self):
        return getattr(self, "u_status", None) == "DOING"


class StageTaskInterface(object):
    def __init__(self, class_id):
        self.class_id = class_id
        self._class = Class.objects.xall().get(id=class_id)
        self._class_type = self._class.class_type
        self._stage_tasks = self.get_stage_tasks_by_class_id(class_id)  # 结构字典数据
        self._students_data = {}  # student_id:data
        self._task_knowledge_interfaces = {}  # stagetask_id:interface

        self._graduated = []  # 毕业的学生,[student_id,student_id,...]

    def get_data_template(self):
        return self._stage_tasks

    @classmethod
    def get_stage_tasks_by_class_id(cls, class_id):
        """
        获取班级的所有任务 相当于模板
        :param class_id:班级id
        :return: [{name:xxx, id:xx,
                   tasks:[ {rid:xx, rname:xx, index:xx, id:x, name:xx, expect_time,excellent_time }, ...]
                   }, ...]
        """
        ret = list()
        # 先取出职业课程
        try:
            _class = Class.objects.xall().get(id=class_id)
        except Class.DoesNotExist:
            raise Http404
        career_course = _class.career_course
        # 取出职业课程下的阶段
        # 加过滤条件,区分lps3. stage中,如何区分是lps3的阶段
        stages = Stage.objects.xall().filter(lps_version='3.0', career_course=career_course).order_by('index')
        # 根据阶段找到任务
        stage_list = stages
        objs = StageTaskRelation.objects.filter(stage__in=stage_list).exclude(task__type=Task.TASK_TYPE_FREE_488)\
                .values('id', 'name', 'index', 'stage_id', 'task__name', 'task__id', 'task__expect_time',
                        'task__excellent_time', 'task__gift_id', 'task__project_id', 'task__desc', 'type') \
                .order_by('index')
        i = 0
        for stage in stage_list:
            info = dict(name=stage.name, id=stage.id)
            ts = list()
            for obj in objs:
                if obj.get('stage_id') == stage.id:
                    i += 1
                    ts.append(
                        dict(
                            real_index=i,
                            rid=obj.get('id'),  # relation id
                            rname=obj.get('name'),  # relation name
                            index=obj.get('index'),  # 排序索引
                            name=obj.get('task__name'),  # 任务名称
                            id=obj.get('task__id'),  # 任务id
                            expect_time=obj.get('task__expect_time'),  # 任务预期时长 天
                            excellent_time=obj.get('task__excellent_time'),  # 最短时长 天
                            gift_id=obj.get('task__gift_id'),
                            project_id=obj.get('task__project_id'),
                            desc=obj.get('task__desc'),
                            type=obj.get('type')
                        )
                    )
            info['tasks'] = ts
            ret.append(info)
        return ret

    @classmethod
    def get_real_stage_tasks_by_class_id(cls, class_id):
        """
        获取可以渲染的更简洁的任务数据
        :param class_id:
        :return:
        """
        ret = list()
        # 先取出职业课程
        try:
            _class = Class.objects.xall().get(id=class_id)
        except Class.DoesNotExist:
            raise Http404
        career_course = _class.career_course
        # 取出职业课程下的阶段
        # 加过滤条件,区分lps3. stage中,如何区分是lps3的阶段
        stages = Stage.objects.xall().filter(lps_version='3.0', career_course=career_course).order_by('index')
        # 根据阶段找到任务
        stage_list = stages
        objs = StageTaskRelation.objects.filter(stage__in=stage_list).exclude(task__type=Task.TASK_TYPE_FREE_488) \
                .values('id','stage_id', 'task__name', 'task__desc', 'type', 'task__id') \
                .order_by('index')
        i = 0
        for stage in stages:
            info = dict(name=stage.name, id=stage.id)
            ts = list()
            for obj in objs:
                if obj.get('stage_id') == stage.id:
                    i += 1
                    ts.append(
                        dict(
                            task_real_index=i,
                            task_rid=obj.get('id'),  # relation id
                            task_name=obj.get('task__name'),  # 任务名称
                            task_desc=obj.get('task__desc'),
                            task_type=obj.get('type'),
                            task_id=obj.get('task__id'),
                        )
                    )
            info['tasks'] = ts
            ret.append(info)
        return ret


    def get_stages(self):
        return list((stage.get('id'), stage.get('name')) for stage in self._stage_tasks)

    def count_all_tasks(self):
        """获取任务总数量"""
        return sum(len(stage['tasks']) for stage in self._stage_tasks)

    def get_task_knowledge_interface(self, stagetask_id, task_id=None):
        """获取(任务-知识点)接口实例"""
        if stagetask_id not in self._task_knowledge_interfaces:
            task_knowledge_interface = TaskKnowledgeInterface(self.class_id, stagetask_id, task_id=task_id,
                                                              class_type=self._class_type)
            self._task_knowledge_interfaces[stagetask_id] = task_knowledge_interface
        return self._task_knowledge_interfaces[stagetask_id]

    def is_guide_task(self, task_id):
        return task_id in (self._class.career_course.lps3_guide_task_id, settings.GUIDE_TASK_ID)

    def is_experience_3_1_task(self, stagetask_id):
        """
        判断是否是lps3.1免费任务
        """
        try:
            task = StageTaskRelation.objects.filter(id=stagetask_id)[0]
        except IndexError:
            return False
        return bool(task.type == 1)

    def _create_usertask_base(self, student_id):
        # 构造用户数据结构,,构建结构基础数据
        result = list()
        for stage in self._stage_tasks:
            user_stage_info = UserStageInfo(self.class_id, student_id, stage['id'], stage['name'],
                                            class_type=self._class_type)
            for task in stage['tasks']:
                user_stage_info.add_task_struct_data(task)
            result.append(user_stage_info)
        return result

    def _load_student_data(self, student_id):
        """
        获取学生的任务
        :param student_id: 学生id
        :note: 学生点击新的任务时,才会进行数据的插入
        不对外开放,
        """
        result = self._create_usertask_base(student_id)
        payment = get_class_students_payment(self.class_id, student_id)
        # 查询出学生在班级的已有任务
        uts = UserTaskRecord.objects.filter(class_id=self.class_id, student_id=student_id)
        tmp = dict()
        for ut in uts:
            user_data = SimpleModelSerializer(ut).data  # 序列化成字典
            tmp[ut.stage_task_id] = user_data

        for stage in result:
            assert isinstance(stage, UserStageInfo)
            # 如果是app免费班,视为所有stage都是paid
            if self._class_type == Class.CLASS_TYPE_FREE:
                # if True:
                paid_flag = True
            else:
                paid_flag = (payment.get(student_id, {}).get(stage.id, False)) & self._class.is_normal()
            stage.set_paid(paid_flag)
            for task in stage.get_tasks():
                assert isinstance(task, UserTaskInfo)
                user_data = tmp.get(task.task_rid, {})
                task.load_user_data(user_data)
        return result

    def _analyse_student_data(self, student_id):
        """分析学生数据,找到可解锁和焦点任务
        不对外开放,加载数据时会自动执行
        """
        total = 0
        last = None  # 上一个
        for task in self.iter_student_tasks(student_id):
            total += 1
            if total == 1 and task.is_locked \
                    and (task.is_paid
                         or self.is_guide_task(task.task_id)
                         or self.is_experience_3_1_task(task.task_rid)):
                task.set_can_be_unlocked(True)
                # 当前锁定,上一个已解锁,并且上一个[不是]正在进行 状态
            if total != 1 and task.is_locked \
                    and not last.is_locked \
                    and (task.is_paid
                         or self.is_free_task(task.task_rid)
                         or self.is_experience_3_1_task(task.task_rid)) \
                    and not last.is_doing:
                task.set_can_be_unlocked(True)
            last = task

        # 最后一个任务完成的 视为毕业
        if last and last.is_pass:
            self._graduated.append(student_id)


        # 找到当前焦点任务
        for task in list(self.iter_student_tasks(student_id))[::-1]:
            assert isinstance(task, UserTaskInfo)
            if task.can_be_unlocked() or not task.is_locked:  # 从后面找到第一个可解锁 或 已解锁 的
                task.set_focus()
                break

    def get_course_syllabus(self):
        """获取课程教学大纲"""
        nums = u"一二三四五六七八九十"
        stages = self.get_data_template()
        projects_ids = list()
        for i, stage in enumerate(stages):
            stage['number'] = nums[i % 10]
            for task in stage['tasks']:
                projects_ids.append(task['project_id'])
                task['knowledges'] = TaskKnowledgeInterface(self.class_id, task['rid'],
                                                            class_type=self._class_type).get_data_template()
        _tmp = Project.objects.filter(id__in=projects_ids).values('id', 'title')
        _tmp = list((obj['id'], obj['title']) for obj in _tmp)
        _tmp = dict(_tmp)
        for stage in stages:
            for task in stage['tasks']:
                task['project_name'] = _tmp.get(task['project_id'])
        return stages

    def load_student_data(self, student_id):
        """加载单个学生数据
        对外接口
        """
        self._students_data[student_id] = self._load_student_data(student_id)
        self._analyse_student_data(student_id)

    def load_students_data(self, students_id):
        """
        加载多学生数据
        :param students_id:list of student id
        """
        # todo:性能优化
        payments = get_class_students_payment(self.class_id)
        uts = UserTaskRecord.objects.filter(
            class_id=self.class_id, student_id__in=students_id)
        tmp = dict()  # (student_id,stage_task_id):dict()
        for ut in uts:
            user_data = SimpleModelSerializer(ut).data  # 序列化成字典
            tmp[(ut.student_id, ut.stage_task_id)] = user_data

        for student_id in students_id:
            result = self._create_usertask_base(student_id)
            for stage in result:
                paid_flag = payments.get(student_id, {}).get(stage.id, False)
                stage.set_paid(paid_flag)
                for task in stage.get_tasks():
                    assert isinstance(task, UserTaskInfo)
                    user_data = tmp.get((student_id, task.task_rid), {})
                    task.load_user_data(user_data)
            self._students_data[student_id] = result
            self._analyse_student_data(student_id)  # 分析数据

    def get_student_data(self, student_id):
        """获取用户数据"""
        if student_id not in self._students_data:
            self.load_student_data(student_id)
        return self._students_data[student_id]

    def get_student_graduate_time(self, student_id):
        """获取用户毕业时间
        暂时取最后一个任务的完成时间
        """
        last_task = self.get_the_last_task(student_id)
        if last_task.is_pass:
            return last_task.done_time
        return datetime.datetime.now()

    def count_student_tasks_finished(self, student_id):
        """获取学生任务完成数量"""
        assert student_id in self._students_data
        return sum(stage.count_task_finished() for stage in self._students_data[student_id])

    def iter_student_tasks(self, student_id):
        """迭代用户任务"""
        assert student_id in self._students_data
        for stage in self._students_data[student_id]:
            for task in stage.get_tasks():
                yield task

    def get_student_latest_task(self, student_id):
        """获取学生最近的一个任务(已解锁的)"""
        current = None
        for task in self.iter_student_tasks(student_id):
            if not task.is_locked:
                current = task
        return current

    def get_student_current_doing_tasks(self, student_id):
        """获取学生当前进行的任务"""
        result = list()
        for task in self.iter_student_tasks(student_id):
            if task.is_doing:
                result.append(task)
        return result

    def get_student_current_stage(self, student_id):
        """获取学生当前进行的阶段"""
        for task in list(self.iter_student_tasks(student_id))[::-1]:
            if not task.is_locked:
                break
        stage = self.get_student_stage_by_stagetask(student_id, task.task_rid)
        return stage

    def get_student_task(self, student_id, stagetask_id):
        """获取用户阶段任务"""
        for task in self.iter_student_tasks(student_id):
            if task.task_rid == stagetask_id:
                return task
        return None

    def get_student_stage(self, student_id, stage_id):
        """获取学生 阶段 状态"""
        for stage in self.get_student_data(student_id):
            if stage.id == stage_id:
                return stage
        return None

    def get_student_stage_by_stagetask(self, student_id, stagetask_id):
        """获取task所在的stage"""
        for stage in self.get_student_data(student_id):
            for task in stage.get_tasks():
                if task.task_rid == stagetask_id:
                    return stage
        return None

    def student_can_unlock_task(self, student_id, stagetask_id):
        """用户是否可以解锁任务"""
        stagetask = self.get_student_task(student_id, stagetask_id)
        if stagetask == self.get_the_last_task(student_id):  # 最后一个任务,需要前面所有已经解锁
            flag = True
            for task in list(self.iter_student_tasks(student_id))[:-1]:
                if task.is_pass:
                    pass
                else:
                    flag = False
            if not flag:
                return False, T_UNLOCK_ERR_LAST_CHECK_ALL

        if not stagetask.is_locked:
            return False, "repeat"
        if stagetask.can_be_unlocked():
            if self.is_guide_task(stagetask.task_id):
                return True, u"新手引导任务,可以开启"
            return True, u"可以开启"
        else:
            if not stagetask.is_paid:
                return False, T_UNLOCK_ERR_NOT_PAID
            return False, T_UNLOCK_ERR_PREVIOUS_NOT_DONE

    def is_just_beginning(self, student_id):
        """判断刚开始学习,还未解锁任何任务"""
        for task in self.iter_student_tasks(student_id):
            if not task.is_locked:
                return False
        return True

    def student_has_finished(self, student_id):
        """学生学完"""
        last_task = self.get_the_last_task(student_id)
        if last_task.is_pass:
            return True
        return False

    def student_fall_behind(self, student_id):
        """学习进度落后"""
        pass

    def get_the_first_task(self, student_id):
        """学生第一个任务"""
        for task in self.iter_student_tasks(student_id):
            return task
        return None

    def get_the_last_task(self, student_id):
        """学生最后一个任务"""
        the_last_one = None
        for task in self.iter_student_tasks(student_id):
            the_last_one = task
        return the_last_one

    def is_free_task(self, stagetask_id):
        """是否为免费任务"""

        def _get_free_list():
            i = 0
            if self._class_type == Class.CLASS_TYPE_FREE:
                # if True:
                free_prex = 999
            else:
                free_prex = 2  # 前两个为免费
            free_tasks = list()
            for stage in self.get_data_template():
                for task in stage.get('tasks', []):
                    if i >= free_prex:
                        break
                    free_tasks.append(task.get('rid'))
                    i += 1
            return free_tasks

        if getattr(self, 'free_tasks', None) is None:
            self.free_tasks = _get_free_list()

        return stagetask_id in self.free_tasks

    def get_class_total_progress(self):
        """获取班级总进度"""
        total_task_count = self.count_all_tasks()
        total = total_task_count * len(self._students_data)
        if total == 0:
            return 0
        done = 0
        for student_id in self._students_data:
            if student_id in self._graduated:  # 毕业的学生
                done += total_task_count
                continue
            for stage in self.get_student_data(student_id):
                for task in stage.get_tasks():
                    if task.is_done or task.is_pass:
                        done += 1
        return int(round(done * 100.0 / total))

    def get_class_total_done_tasks(self):
        """获取班级新增未批改task(作业)"""
        done = 0
        for student_id in self._students_data:
            for stage in self.get_student_data(student_id):
                for task in stage.get_tasks():
                    if task.is_done:
                        done += 1
        return done

    def count_knowledges(self, student_id='NULL'):
        """
        获取总的和已完成的知识点数和测试项数
        """
        # 免费班project不计入考核
        knowledgeitem_type = ''
        if self._class_type == Class.CLASS_TYPE_FREE and student_id != 'NULL':
            knowledgeitem_type = 'PROJECT'
        sql = """
        SELECT
            tkr.id,
            ukir.id,
            ki.id,
            ki.obj_type
        FROM
            mz_lps3_taskknowledgerelation AS tkr
        JOIN mz_lps3_stagetaskrelation AS str ON str.task_id = tkr.task_id
        JOIN mz_course_stage AS s ON s.id = str.stage_id
        JOIN mz_lps_class AS c ON c.career_course_id = s.career_course_id
        JOIN mz_lps3_knowledgeitem AS ki ON (
            ki.parent_id = tkr.knowledge_id
            AND ki.obj_type != '%s'
        )
        LEFT JOIN mz_lps3_usertaskrecord AS utr ON (
            utr.stage_task_id = str.id
            AND utr.class_id = c.id
            AND utr.student_id = %s
            AND utr.is_in_sequence = 1
        )
        LEFT JOIN mz_lps3_userknowledgeitemrecord AS ukir ON (
            ukir.user_task_record_id = utr.id
            AND ukir.knowledge_item_id = ki.id
            AND ukir.`status` = 'DONE'
        )
        WHERE
            c.id = %s
        """ % (knowledgeitem_type, student_id, self.class_id)
        knowledge_dict = {}
        total_knowledge = 0
        done_knowledge = 0
        total_test_item = 0
        done_test_item = 0
        # 循环出: task_knowledge_relation_id, 知识点项纪录id, 知识点项id, 知识点项type
        for tkr_id, item_record_id, item_id, item_type in exec_sql(sql):
            # 'TEST', 'PROJECT'计入'测试项'
            if item_type in ('TEST', 'PROJECT'):
                total_test_item += 1
                # 知识点项纪录有数据则计入'完成的测试项'
                if item_record_id:
                    done_test_item += 1
            # 构造以知识点为key的dict
            knowledge_dict.setdefault(tkr_id, {'item_count': 0, 'item_record_count': 0})
            # dict的value为'知识点项'计数(包括'LESSON')和'知识点项纪录'计数
            knowledge_dict[tkr_id]['item_count'] += 1
            if item_record_id:
                knowledge_dict[tkr_id]['item_record_count'] += 1

        # 如果知识点内'知识点项'计数 == '知识点项纪录'计数
        for knowledge in knowledge_dict.itervalues():
            total_knowledge += 1
            if knowledge['item_count'] == knowledge['item_record_count']:
                done_knowledge += 1

        return total_knowledge, done_knowledge, total_test_item, done_test_item


class TaskKnowledgeInterface(object):
    def __init__(self, class_id, stagetask_id, task_id=None, class_type=Class.CLASS_TYPE_NORMAL):
        """
        :param stagetask_id: id of StageTaskRelation
        :param task_id:id of Task
        """
        self.class_id = class_id
        self.stagetask_id = stagetask_id
        self.task_id = task_id
        self.class_type = class_type
        self._struct = None
        self._items_map = dict()
        self._student_data = {}

    @classmethod
    def get_task_knowledge_struct(cls, task_id):
        """获取一个任务 知识点结构
        :param task_id: 任务id  ==> id of Task
        :return: [{rid:xx,name:xx,index:xx,task_id:xx,knowledge_id:xx,items:[{},]}]
        """
        ret = list()
        objs = TaskKnowledgeRelation.objects \
            .filter(task_id=task_id) \
            .values('id', 'index', 'task_id', 'task__name',
                    'knowledge_id', 'knowledge__name') \
            .order_by('index')
        temp = dict()
        for obj in objs:
            info = dict(
                rid=obj.get('id'),
                name=obj.get('knowledge__name'),
                index=obj.get('index'),
                knowledge_id=obj.get('knowledge_id'),
                task_id=obj.get('task_id'),
                items=list()
            )
            temp[obj['knowledge_id']] = info
            ret.append(info)
        sql = """
        SELECT
            item.id,
            item.obj_type,
            item.obj_id,
            item.expect_time,
            item.`index`,
            item.created,
            item.parent_id,
            lesson.`name` AS lesson_name,
            lesson.video_length AS lesson_video_length,
            exam.title AS exam_title,
            COUNT(q.id)
        FROM
            mz_lps3_knowledgeitem AS item
        LEFT JOIN mz_course_lesson AS lesson ON lesson.id = item.obj_id
        AND item.obj_type = 'LESSON'
        LEFT JOIN mz_lps_examine AS exam ON exam.id = item.obj_id
        AND item.obj_type IN ('PROJECT', 'TEST')
        LEFT JOIN mz_lps_quiz AS q ON q.paper_id = exam.id
        WHERE
            item.parent_id IN (
                SELECT
                    mz_lps3_taskknowledgerelation.knowledge_id
                FROM
                    mz_lps3_taskknowledgerelation
                WHERE
                    mz_lps3_taskknowledgerelation.task_id = %s
            )
        GROUP BY
            item.id
        """ % task_id
        for id, obj_type, obj_id, expect_time, index, created, parent_id, \
            lesson_name, lesson_video_length, exam_title, quiz_count in exec_sql(sql):
            _data = dict(
                id=id, obj_type=obj_type, obj_id=obj_id, index=index, parent_id=parent_id,
                lesson_name=lesson_name, lesson_video_length=lesson_video_length,
                exam_title=exam_title, quiz_count=quiz_count, expect_time=expect_time,
            )
            items = temp[parent_id]['items']
            items.append(_data)

        return ret

    def get_data_template(self):
        if self._struct is None:
            if self.task_id is None:
                self.task_id = get_object_or_404(StageTaskRelation, id=self.stagetask_id).task_id
            self._struct = self.get_task_knowledge_struct(self.task_id)
        return self._struct

    def _load_student_data(self, student_id):
        """
        获取用户任务详情
        1.获取任务的总 知识点item 数量
        2.获取用户的完成量
        :param student_id: student user id
        """
        knowledge_strut = self.get_data_template()

        usertask = UserTaskRecord.objects.not_in_sequence_all().get(
            stage_task_id=self.stagetask_id, student_id=student_id, class_id=self.class_id)

        uis = usertask.userknowledgeitemrecord_set.all()
        tmp2 = dict()  # knowledegitem_id:info
        for ui in uis:
            info = SimpleModelSerializer(ui, ['created', 'id', 'status', 'done_time']).data
            tmp2[ui.knowledge_item_id] = info

        result = list()

        for knowledge in knowledge_strut:
            # 用户知识点信息
            uk = UserKnowledgeInfo()
            uk.load_struct_data(knowledge)
            # [{id:xx,name:xx,index:xx,task_id:xx,knowledge_id:xx,items:[{},]}]
            for item in uk.get_items():
                item_id = item.id
                user_item = tmp2.get(item_id, {})
                item.load_user_data(user_item)
            result.append(uk)
        return (usertask, result)

    def _analyse_student_data(self, student_id):
        """分析用户当前焦点item"""
        # 如果是app免费班,所有item不用按序做
        if self.class_type in (Class.CLASS_TYPE_FREE, Class.CLASS_TYPE_FREE_488):
            # if True:
            for item in self.iter_student_items(student_id):
                assert isinstance(item, UserKnowledgeItemInfo)
                item.set_can_be_unlocked(True)

        else:
            last = None
            i = 0
            for item in self.iter_student_items(student_id):
                assert isinstance(item, UserKnowledgeItemInfo)
                if item.is_lesson:
                    continue
                i += 1
                if i == 1 and item.is_undo:
                    item.set_can_be_unlocked(True)
                elif i > 1 and item.is_undo and last.is_done:
                    item.set_can_be_unlocked(True)
                last = item

            the_next = None
            for item in list(self.iter_student_items(student_id))[::-1]:
                assert isinstance(item, UserKnowledgeItemInfo)
                if item.is_doing:  # 最后一个正在进行中的item
                    item.set_focus()
                    break
                if item.is_done and the_next and the_next.is_undo:  # 这个已完成,后面的还未开始,后面的那个聚焦
                    the_next.set_focus()
                    break
                the_next = item

    def load_student_data(self, student_id):
        self._student_data[student_id] = self._load_student_data(student_id)
        self._analyse_student_data(student_id)

    def get_student_data(self, student_id):
        if student_id not in self._student_data:
            self.load_student_data(student_id)
        return self._student_data[student_id][1]

    def get_student_usertask_model(self, student_id):
        if student_id not in self._student_data:
            self.load_student_data(student_id)
        return self._student_data[student_id][0]

    def get_knowledge_id_by_item(self, item_id):
        for knowledge in self._struct:
            for item in knowledge['items']:
                if item.get('id') == item_id:
                    return knowledge.get('knowledge_id')

    def get_utask_progress(self, student_id):
        """
        获取用户任务的进度,针对未完成的任务
        1.获取任务的总 知识点item 数量
        """
        usertask = self.get_student_usertask_model(student_id)
        if usertask.status in ("DONE", "PASS"):
            return 100
        total = 0
        done = 0

        # 如果是app免费班,计算进度不包括PROJECT
        if self.class_type == Class.CLASS_TYPE_FREE:
            # if True:
            for item in self.iter_student_items(student_id):
                if not item.is_project:
                    total += 1
                    if item.is_done:
                        done += 1
            # 规避item数目为0的情况
            if total == 0:
                progress = 100
            else:
                progress = int(round(done * 100.0 / total))
            return progress

        else:
            for item in self.iter_student_items(student_id):
                total += 1
                if item.is_done:
                    done += 1
            return int(round(done * 100.0 / (total + 1)))

    def iter_student_items(self, student_id):
        for k in self.get_student_data(student_id):
            for item in k.get_items():
                yield item

    def student_has_done_task(self, student_id):
        assert student_id in self._student_data
        usertask = self._student_data[student_id][0]
        return usertask.status in ("DONE", "PASS")

    def get_student_latest_item(self, student_id):
        current = None
        for task in self.iter_student_items(student_id):
            if not task.is_undo:
                current = task
        return current

    def get_student_current_doing_items(self, student_id):
        """获取用户当前进行中的item"""
        pass

    def get_student_item(self, student_id, item_id):
        """"""
        for item in self.iter_student_items(student_id):
            if item.id == item_id:
                return item
        return None

    def all_items_have_done(self, student_id):
        """判断所有item是否都已完成"""
        flag = True

        if self.class_type == Class.CLASS_TYPE_FREE_488:
            return True
        # 如果是app免费班,计算是否都完成时不算PROJECT
        elif self.class_type == Class.CLASS_TYPE_FREE:
            # if True:
            for item in self.iter_student_items(student_id):
                if item.is_project:
                    continue
                if not item.is_done:
                    flag = False
                    break
            return flag

        else:
            for item in self.iter_student_items(student_id):
                if item.is_lesson:
                    continue
                if not item.is_done:
                    flag = False
                    break
            return flag

    def done_item_count(self, student_id):
        """对完成的item计数"""
        count = 0
        for item in self.iter_student_items(student_id):
            if item.is_done:
                count += 1
        return count

    def is_just_beginning(self, student_id):
        """判断是否刚开始"""
        for item in self.iter_student_items(student_id):
            if not item.is_undo:
                return False
        return True

    def get_the_first_item(self, student_id):
        """取得第一个item"""
        for item in self.iter_student_items(student_id):
            return item
        return None


if __name__ == "__main__":
    pass
    # print get_class_students_show_info(180,13)
    # print get_student_classes(50238)
    # struct = get_stage_tasks_by_class_id(106)
    # for stage in struct:
    #     for task in stage['tasks']:
    #         print task['task__name']
    # # print get_task_knowledge_struct(30)
    # print get_student_tasks_by_class_id(106, 69736)
    # print class_has_stage_task(106, 12)
    # print get_user_paid_stages(69736)
    # print user_has_paid_for_stage(69736, 101)
    # print get_student_doing_tasks_timeleft(111, 34000)
    # print get_class_students_latest_rank(111)
    # print get_class_student_stage_info_1(111, 34000, 101)
    # print get_class_students_payment(111, 34000)
    # iface = StageTaskInterface(111)
    # iface.load_student_data(34000)
    # print get_class_students_latest_rank(111)
