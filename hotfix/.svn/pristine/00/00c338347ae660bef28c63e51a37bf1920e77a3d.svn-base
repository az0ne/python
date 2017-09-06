# -*- coding: utf-8 -*-
import datetime
import time
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from mz_lps3 import functions as lps3_functions
from mz_lps.models import Class, ClassStudents
from mz_lps3.models import UserTaskRecord, UserKnowledgeItemRecord, UserGiftRecord, StudyHistory, ClassMeetingRelation, \
    ClassMeetingAttendance
from mz_pay.models import UserPurchase
from mz_user.models import UserProfile, MyCourse
from mz_eduadmin.models import OptLog
import xlwt

__author__ = 'Jackie'


def time_cost(func):
    import time
    def _wrapper(*args, **kwargs):
        begin = time.time()
        ret = func(*args, **kwargs)
        print time.time() - begin
        return ret

    return _wrapper


def datetime2timestamp(dt):
    """datetime转时间戳(毫秒级)"""
    return long(time.mktime(dt.timetuple()) * 1000 + dt.microsecond / 1000)


def log_opt(class_id, student_id, operator_id, opt_type, remark='', **kwargs):
    """教务操作日志
    暂时不加
    """
    ol = OptLog()
    ol.class_id = class_id
    ol.student_id = student_id
    ol.operator_id = operator_id
    ol.opt_type = opt_type
    ol.remark = remark
    if opt_type == ol.OPT_TYPE_STUDENT_CHANGE_CLASS:  # 学生转班操作
        to_class_id = kwargs.pop('to_class_id')
        assert to_class_id
        ol.ext_obj_type = ol.EXT_OBJ_TYPE_CLASS
        ol.ext_obj_id = to_class_id
    ol.save()


def change_student_class(class_id, student_id, operator_id, to_class, remark):
    """
    学生转班
    :param to_class: class coding
    """
    cstudent = get_object_or_404(ClassStudents, user_id=student_id, student_class_id=class_id)
    old_class = Class.objects.xall().get(id=class_id)
    new_class = Class.objects.xall().filter(lps_version=3.0, coding=to_class, class_type=Class.CLASS_TYPE_NORMAL)
    if not new_class:
        return False, u'未找到指定班级'
    new_class = new_class[0]
    assert isinstance(new_class, Class)
    if str(new_class.id) == str(class_id):
        return False, u'转入当前班级???'
    if old_class.career_course_id != new_class.career_course_id:
        return False, u'只能同专业转班'
    if not new_class.is_active:
        return False, u'班级无效'
    if new_class.status == 2:
        return False, u'班级已结束'
    if new_class.is_closed:
        return False, u'班级已关闭了报名'
    if not new_class.current_student_count < new_class.student_limit:
        return False, u'班级已达人数上限'

    @transaction.atomic
    def _sub():
        cstudent.student_class_id = new_class.id
        old_class.current_student_count = old_class.current_student_count - 1
        new_class.current_student_count = new_class.current_student_count + 1
        cstudent.save()
        old_class.save()
        new_class.save()
        # 乱序解锁任务球，加not_in_sequence_all
        UserTaskRecord.objects.not_in_sequence_all().filter(class_id=class_id, student_id=student_id).update(class_id=new_class.id)
        UserKnowledgeItemRecord.objects.filter(class_id=class_id, student_id=student_id).update(class_id=new_class.id)
        UserGiftRecord.objects.filter(class_id=class_id, student_id=student_id).update(class_id=new_class.id)
        StudyHistory.objects.filter(class_id=class_id, student_id=student_id).update(class_id=new_class.id)
        UserPurchase.objects.filter(pay_class_id=class_id, user_id=student_id).update(pay_class_id=new_class.id)

        log_opt(class_id, student_id, operator_id,
                OptLog.OPT_TYPE_STUDENT_CHANGE_CLASS, remark=remark, to_class_id=new_class.id)

    try:
        _sub()
    except Exception, e:
        return False, e.message
    return True, u'成功转入新的班级'


def student_quit_class(class_id, student_id, operator_id, remark):
    """
    学生退班
    """
    cstudent = get_object_or_404(ClassStudents, user_id=student_id, student_class_id=class_id)
    career_course_id = cstudent.student_class.career_course_id

    @transaction.atomic
    def _sub():
        assert cstudent.status == ClassStudents.STATUS_NORMAL
        cstudent.status = cstudent.STATUS_QUIT
        cstudent.quit_datetime = datetime.datetime.now()
        cstudent.save()
        MyCourse.objects.filter(user_id=student_id, course_type=2, course=career_course_id).delete()
        log_opt(class_id, student_id, operator_id, OptLog.OPT_TYPE_STUDENT_QUIT, remark=remark)

    try:
        _sub()
    except Exception, e:
        return False, e.message

    return True, u'已成功办理退学'


def student_pause_studying(class_id, student_id, operator_id, remark, type='pause'):
    """
    学生休学
    """
    cstudent = get_object_or_404(ClassStudents, student_class_id=class_id, user_id=student_id)
    if cstudent.is_pause:  # 暂停状态
        assert type == 'resume'
    else:
        assert type == 'pause'
    now = datetime.datetime.now()

    @transaction.atomic()
    def _pause_studying():
        cstudent.is_pause = True
        cstudent.pause_datetime = now
        cstudent.pause_reason = u"老师触发暂停,teacherID:%s" % operator_id
        cstudent.save()
        for utask in UserTaskRecord.objects.filter(
                class_id=class_id, student_id=student_id, status__in=('DOING', 'REDOING')):
            utask.is_pause = True
            utask.pause_datetime = now
            utask.save()
        log_opt(class_id, student_id, operator_id, OptLog.OPT_TYPE_STUDENT_PAUSE, remark=remark)

    @transaction.atomic()
    def _resume_studying():
        cstudent.is_pause = False
        cstudent.restore_datetime = now
        cstudent.save()
        for utask in UserTaskRecord.objects.filter(
                class_id=class_id, student_id=student_id, is_pause=True):
            utask.is_pause = False
            delta = now - utask.pause_datetime
            utask.paused_seconds = delta.days * 24 * 3600 + delta.seconds + (utask.paused_seconds or 0)
            utask.pause_datetime = now
            utask.save()
        log_opt(class_id, student_id, operator_id, OptLog.OPT_TYPE_STUDENT_RESUME, remark=remark)

    try:
        if type == 'pause':  # 暂停
            _pause_studying()
            if cstudent.user.mobile:
                course_name = cstudent.student_class.career_course.name
        else:  # 恢复学习
            _resume_studying()
    except Exception, e:
        return False, e.message
    return True, u'已成功办理休学' if type == 'pause' else u'已成功办理复学'


class ClassStudentsInterface(object):
    STUDENT_FINISH = 0
    STUDENT_GRADUATE = 1
    STUDENT_NORMAL = 2
    STUDENT_PAUSED = 3
    STUDENT_QUIT = 4
    STUDENT_BEHIND = 5
    STUDENT_STATUS = {
        STUDENT_FINISH: u'已学完',
        STUDENT_GRADUATE: u'已毕业',
        STUDENT_NORMAL: u'正常',
        STUDENT_PAUSED: u'休学',
        STUDENT_QUIT: u'已退学',
        STUDENT_BEHIND: u'落后',
    }

    def __init__(self, class_id, students_objs=None):
        self.class_id = class_id
        self.students = students_objs
        self._load()

    def _load(self):
        # 只接受LPS3的班级
        self._status = {'graduate': [], 'finish': [], 'normal': [], 'paused': [], 'quit': [], 'behind': []}
        self._class = Class.objects.xall().get(
            id=self.class_id, lps_version='3.0', class_type=Class.CLASS_TYPE_NORMAL)
        self.students = self.students or list(self._class.students.all())
        self.students_show_info = lps3_functions.get_class_students_show_info(
            self.class_id, self._class.career_course_id
        )
        self.iface = lps3_functions.StageTaskInterface(self.class_id)
        self.iface.load_students_data(list(student.id for student in self.students))
        self.students_rank_info = lps3_functions.get_class_students_latest_rank(self.class_id)

        for student in self.students:
            student_id = student.id
            info = self.students_show_info[student_id]
            if self._class.status == 2 and info['student_status'] == ClassStudents.STATUS_NORMAL:  # 班级一毕业
                self._status['graduate'].append(student_id)
                continue
            if info['student_status'] == ClassStudents.STATUS_QUIT:  # 退学
                self._status['quit'].append(student_id)
                continue
            if info['is_pause']:  # 休学的
                self._status['paused'].append(student_id)
                continue
            if self.iface.student_has_finished(student_id):  # 学完
                self._status['finish'].append(student_id)
                continue
            current_tasks = self.iface.get_student_current_doing_tasks(student_id)
            behind = False
            for t in current_tasks:
                if t.get_timeleft() < 3600 * 24:
                    behind = True
                    break
            if behind:
                self._status['behind'].append(student_id)
                continue
            self._status['normal'].append(student_id)

    @property
    def class_name(self):
        return self._class.coding

    @cached_property
    def course_name(self):
        return self._class.career_course.name

    @cached_property
    def teacher_name(self):
        return self._class.teacher_name

    @cached_property
    def eduadmin_name(self):
        return self._class.edu_admin.staff_name

    def get_student_status(self, student_id):
        if student_id in self._status['finish']:
            return self.STUDENT_FINISH
        if student_id in self._status['graduate']:
            return self.STUDENT_GRADUATE
        if student_id in self._status['normal']:
            return self.STUDENT_NORMAL
        if student_id in self._status['paused']:
            return self.STUDENT_PAUSED
        if student_id in self._status['behind']:
            return self.STUDENT_BEHIND
        if student_id in self._status['quit']:
            return self.STUDENT_QUIT

    def _status_attrs(self, status):
        return {
            'status_is_normal': True if status == self.STUDENT_NORMAL else False,
            'status_is_behind': True if status == self.STUDENT_BEHIND else False,
            'status_is_paused': True if status == self.STUDENT_PAUSED else False,
            'status_is_quit': True if status == self.STUDENT_QUIT else False,
            'status_is_finish': True if status == self.STUDENT_FINISH else False,
            'status_is_graduate': True if status == self.STUDENT_GRADUATE else False,
        }

    def _cal_expiring_date(self, deadline):
        """计算试学学员的到期时间
        :param deadline: 试学到期时间
        """
        if not self._class.meeting_enabled:
            return ''
        if not deadline:
            return ''
        return deadline.date().isoformat()

    @cached_property
    def data(self):
        ret = list()
        for student in self.students:
            show_info = self.students_show_info.get(student.id)
            deadline = show_info.get('deadline')
            join_in_class_datetime = show_info['join_in_class_time'] or datetime.datetime.now()
            student_status = self.get_student_status(student.id)
            data = dict()

            data.update(self._status_attrs(student_status))

            data['class_id'] = self.class_id
            data['class_eduadmin_id'] = self._class.edu_admin_id
            data['model'] = student
            data['show_info'] = show_info

            data['is_full_payment'] = not bool(deadline)
            data['student_status'] = student_status
            data['show_student_status'] = self.STUDENT_STATUS.get(student_status)
            data['show_name'] = data['show_info']['real_name'] or student.nick_name
            data['join_in_class_timestamp'] = datetime2timestamp(join_in_class_datetime)
            data['join_in_class_date'] = join_in_class_datetime.date().isoformat()

            # data['study_goal'] = ''
            # career_course_id = Class.objects.xall().get(id=self.class_id).career_course.id
            # user_goals = UserStudyGoal.objects.filter(user_id=student.id,
            #                                           career_course_id=career_course_id)
            # if user_goals:
            # data['study_goal'] = UserStudyGoal.GOAL_CHOICES.get(show_info['study_goal'], '')

            if not data['is_full_payment']:  # 试学学员
                # 试学到期时间
                data['expiring_date'] = self._cal_expiring_date(deadline)
            if student_status == self.STUDENT_GRADUATE:
                # 毕业时间
                data['graduate_date'] = self.iface.get_student_graduate_time(student.id).date().isoformat()
            if student_status == self.STUDENT_QUIT:
                quit_time = show_info['quit_time']
                # 退学时间
                data['quit_date'] = quit_time.date().isoformat() if quit_time else ''

            data['show_status_gray'] = student_status in (self.STUDENT_QUIT, self.STUDENT_GRADUATE, self.STUDENT_PAUSED)

            data['stages'] = self.iface.get_student_data(student.id)
            data['can_be_operated'] = not (student_status in (self.STUDENT_QUIT, self.STUDENT_GRADUATE))
            data['class_rank'] = self.students_rank_info.get(student.id)
            ret.append(data)
        return ret

    @cached_property
    def dashboard(self):
        ret = {'total': len(self.students),
               'finish': len(self._status['finish']),
               'graduate': len(self._status['graduate']),
               'normal': len(self._status['normal']),
               'paused': len(self._status['paused']),
               'quit': len(self._status['quit']),
               'behind': len(self._status['behind'])
               }
        return ret


class QueryStudentsInterface:
    def __init__(self, eduadmin_id, query):
        self.eduadmin_id = eduadmin_id
        self.query = query
        self._load()

    def _load(self):
        objs = ClassStudents.objects.filter(
            student_class__edu_admin_id=self.eduadmin_id, user__real_name__contains=self.query,
            student_class__lps_version='3.0', student_class__class_type=Class.CLASS_TYPE_NORMAL
        ).values('student_class_id', 'user_id').order_by('-created')
        tmp = dict()  # {class:[students]}
        objs2 = UserProfile.objects.filter(id__in=[obj['user_id'] for obj in objs])
        objs2 = dict((obj.id, obj) for obj in objs2)
        for obj in objs:
            class_id, student_id = obj['student_class_id'], obj['user_id']
            tmp.setdefault(class_id, [])
            student = objs2.get(student_id)
            if student:
                tmp[class_id].append(objs2[student_id])
        self.ifaces = list()
        for class_id, students in tmp.iteritems():
            iface = ClassStudentsInterface(class_id, students)
            self.ifaces.append(iface)

    @cached_property
    def data(self):
        ret = list()
        for iface in self.ifaces:
            ret.extend(iface.data)
        return ret

    @cached_property
    def dashboard(self):
        ret = {'total': 0, 'graduate': 0, 'finish': 0, 'normal': 0, 'paused': 0, 'quit': 0, 'behind': 0}
        for iface in self.ifaces:
            ret['total'] += iface.dashboard['total']
            ret['finish'] += iface.dashboard['finish']
            ret['graduate'] += iface.dashboard['graduate']
            ret['normal'] += iface.dashboard['normal']
            ret['paused'] += iface.dashboard['paused']
            ret['quit'] += iface.dashboard['quit']
            ret['behind'] += iface.dashboard['behind']
        return ret


class ClassStudentsExportInterface(ClassStudentsInterface):
    def __init__(self, class_id):
        super(ClassStudentsExportInterface, self).__init__(class_id)
        self._orders = None  # dict() 记录班内所有学生的订单
        self._attendances = None  # 记录班内所有学生的考勤

    @cached_property
    def data_plus(self):
        ret = list()
        for i, d in enumerate(self.data):
            student = d['model']
            student_address = u'%s %s %s' % (
                d['show_info']['province'] or '', d['show_info']['city'] or '', student.address or '')
            row = (
                str(i + 1),  # 序号
                student.real_name or student.nick_name,  # 姓名
                student.username,  # 账号
                d['join_in_class_date'] or '',  # 入班时间
                u'全款' if d['is_full_payment'] else u'试学',  # 缴费情况
                self.get_student_order_info(student.id),  # 支付方式/交易号
                self.iface.get_student_current_stage(student.id).name,  # 学习阶段
                self.STUDENT_STATUS.get(d['student_status'], ''),  # 学习状态
                self.get_student_attendance_info(student.id),  # 考勤状况
                student.gender_text,  # 性别
                student.age or '',  # 年龄
                student.qq,  # qq
                student.email or '',  # email
                student.mobile or '',  # mobile
                student_address,
                student.description or '',  # 自我评价
                d['show_info']['degree'],  # 学历
                d['show_info']['study_goal'],  # 学习目的
                d['show_info']['study_base'],  # 学习基础
            )
            ret.append(row)

        return ret

    def get_student_order_info(self, student_id):
        """批处理订单信息"""
        if self._orders is None:
            self._orders = dict()
            objs = UserPurchase.objects.filter(
                pay_careercourse_id=self._class.career_course_id, user_id__in=list(u.id for u in self.students),
                pay_status=1,
            ).order_by('-id')
            for obj in objs:
                self._orders.setdefault(obj.user_id, list())
                self._orders[obj.user_id].append((obj.pay_way_text, obj.trade_no))
        ret = self._orders.get(student_id)
        if ret:
            return u'/'.join(ret[0])
        else:
            return ''

    def get_student_attendance_info(self, student_id):
        """批处理考勤信息"""
        if self._attendances is None:
            self._attendances = dict()
            objs = ClassMeetingRelation.objects.filter(
                class_id=self.class_id,
                class_meeting__status=1,  # 已结束
            ).values('class_meeting__id').order_by('class_meeting__id')
            tmp1 = list(obj['class_meeting__id'] for obj in objs)
            objs = ClassMeetingAttendance.objects.filter(
                student_id__in=list(u.id for u in self.students),
                class_meeting_id__in=tmp1
            )
            tmp2 = dict(((obj.class_meeting_id, obj.student_id), obj) for obj in objs)
            for student in self.students:
                self._attendances.setdefault(student.id, [])
                for mid in tmp1:
                    att = tmp2.get((mid, student.id))
                    self._attendances[student.id].append(att.status_text if att else u"缺勤")

        return u','.join(self._attendances.get(student_id))

    def export(self):
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet(u"内部资料".encode('utf-8'))
        self._write_title(sheet)

        for i, row in enumerate(self.data_plus):
            for j, cell in enumerate(row):
                sheet.write(3 + i, j, cell)

        return book

    def _write_title(self, sheet):
        font_bold = xlwt.Font()
        font_bold.bold = True

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER

        style_title = xlwt.XFStyle()
        style_title.font = font_bold
        style_title.alignment = alignment

        sheet.write_merge(
            0, 0, 0, 18, u'专业:%s  老师:%s  教务:%s' % (self.course_name, self.teacher_name, self.eduadmin_name),
            style_title
        )
        sheet.write_merge(
            1, 1, 0, 18,
            u"班级:%s 总人数:%s 正常学习:%s 落后:%s 已学完:%s 已毕业:%s 休学:%s 退学:%s" % \
            (self.class_name, self.dashboard['total'], self.dashboard['normal'], self.dashboard['behind'],
             self.dashboard['finish'],
             self.dashboard['graduate'], self.dashboard['paused'], self.dashboard['quit']),
            style_title
        )
        heads = [u'序号', u'学生', u'麦子账号', u'入学时间', u'缴费情况', u'支付方式/交易号', u'学习阶段', u'学习状态',
                 u'考勤记录', u'性别', u'年龄', u'QQ', u'邮箱', u'手机号码', u'地址', u'自我评价', u'学历', u'学习目的', u'学习基础']
        for i, h in enumerate(heads):
            sheet.write(2, i, h, style_title)


if __name__ == "__main__":
    # print get_class_students_list(134)
    # print get_teachers()
    # interface = ClassStudentsInterface(134)
    # print interface.dashboard
    # print interface.data
    # print get_edu_admins()
    # print get_classes_by_eduadmin(20276)
    # iface = QueryStudentsInterface(20276, u'李')
    iface = ClassStudentsExportInterface(134)
    # print iface.data_plus
    print iface.get_student_attendance_info(11)
    # excel = iface.export()
    # excel.save(open('d:/ddd.xls', 'wb'))
