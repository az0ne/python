# -*- coding: utf-8 -*
from mz_lps4.models import OnevoneMeeting
from utils.send_sms_and_message import SendSmsAndMessage
from utils.tool import strip_tags

import datetime
import urllib

from django.utils.functional import cached_property
from django.conf import settings

import db.api.onevone.meeting
import db.api.lps.student
import db.api.user.user
from core.common.http.response import failed_json
from mz_lps.models import ClassStudents
from mz_lps3.functions_nj import StageTaskInterface

from mz_lps4 import class_dict
from mz_lps4.class_dict import week_day_dict
from db.api.onevone.study_service import get_student_unread, get_teacher_unread, get_teacher_by_lps4, get_user_name, \
    create_new_service
from mz_platform.objects.sql_result_wrapper import SqlResultWrapper
from mz_user.models import UserJobInfo
from mz_usercenter.student.interface_job_info import get_study_goal
from utils.logger import logger as log
from mz_usercenter.student.interface_study import get_study_base
import db.api.course.career_course
from utils.message_queue import mq_service


def update_join_url(meeting, is_teacher=False, is_video=False):
    """
    更新meeting的join_url
    :param meeting:
    :param is_teacher:
    :param is_video:
    :return:
    """
    if is_teacher:
        nick_name = meeting.get('teacher_real_name', '') or meeting.get('teacher_nick_name', '')
    else:
        nick_name = meeting.get('user_name', '') or meeting.get('user_real_name', '') \
                    or meeting.get('user_nick_name', '')
    # 录播
    if meeting['video_url']:
        url = meeting['video_url']
        token = meeting['video_token']
    else:
        if is_video:
            return ''
        # 客户端加入地址(学生以助教的身份加入)
        url = meeting['teacher_url']
        token = meeting['teacher_token'] if is_teacher else meeting['assistant_token']
    values = {'nickname': nick_name, 'token': token}
    join_url = url + '?' + urllib.urlencode(values)

    return join_url


def get_onevone_meeting_info(user_id, career_id):
    """
    lps4首页 获取1V1直播的数据信息
    :param user_id:
    :param career_id:
    :return:
    """
    to_begin_meeting = {}
    now = datetime.datetime.now()
    now_after_30_min = now + datetime.timedelta(minutes=30)

    # 获取半小时内可以进入的直播（显示直到已开始）
    result = db.api.onevone.meeting.get_to_begin_meeting(user_id, career_id, now_after_30_min)
    if result.is_error():
        log.warn('is_ended_onevone_meeting is error career_id:%s user_id"%s' % (career_id, user_id))
    else:
        to_begin_meeting = result.result()

    # 更新meeting的join_url
    try:
        join_url = update_join_url(to_begin_meeting)
    except Exception as e:
        log.warn(str(e))
    else:
        to_begin_meeting.update({'join_url': join_url})
    return dict(to_begin_meeting=to_begin_meeting)


def cmp_type(x, y):
    # 就业类型排序
    x = x['type']
    if x == 1:
        return -1
    elif x == 0:
        return -1
    elif x == 2:
        return 1
    else:
        return 0


def cmp_count(x, y):
    x_c = (x['onevone_count'].get('new_service_count', 0) +
           x['onevone_count'].get('new_comment_count', 0))
    y_c = (y['onevone_count'].get('new_service_count', 0) +
           y['onevone_count'].get('new_comment_count', 0))
    if x_c < y_c:
        return 1
    else:
        return -1


def get_student_type_by_students(students, career_id):
    """
    根据user id列表获取用户购买的服务类型 保就业还是棉就业还是试学
    :param students:
    :param career_id:
    :return:
    """

    types = dict()
    for student in students:
        result = db.api.lps.student.get_lps4_student_info_by_user_id(
            student.id, career_id, ['type'])
        if result.is_error():
            log.warn('get_lps4_student_info_by_user_id failed. '
                        'student_id: {0}, career_id: {1}'.format(student.id, career_id))
            result = {'type': 99}
        else:
            result = result.result() or {'type': 99}
        types.update({student.id: result['type']})
    return types


def student_unread_num(career_id, student_id, teacher_id):
    """
    学生端 未读老师回复数
    :param student_id:
    :param teacher_id:
    :param career_id:
    :return:
    """
    result = get_student_unread(career_id=career_id, teacher_id=teacher_id, student_id=student_id)
    if result.is_error():
        return 0
    return result.result()


def _teacher_unread_num(career_id, student_list, teacher_id):
    """
    老师端每个学生的未读数
    :param student_list:
    :param career_id:
    :return:
    """
    result = get_teacher_unread(career_id=career_id, student_list=student_list, teacher_id=teacher_id)
    if result.is_error():
        return {}
    result = {res['user_id']: res for res in result.result()}
    return result


def teacher_unread_num(students, class_id, teacher_id):
    try_class_dict = {v: k for k, v in class_dict.NORMAL_CLASS_DICT.items()}

    return _teacher_unread_num(
        try_class_dict[class_id], [student.id for student in students], teacher_id)


def get_students(teacher_id, career_id):
    res = db.api.lps.student.get_students_by_lps4(
        teacher_id, career_id).result()
    for r in res:
        r['id'] = r['user_id']
    return [SqlResultWrapper(r) for r in res]


def students_show_info(career_id, students):
    res = db.api.lps.student.get_students_info(
        career_id, [s.user_id for s in students]).result()

    result = dict()
    for r in res:
        result[r['id']] = dict(
            id=r['id'],
            real_name=r['real_name'],  # 真实姓名
            real_email=r['real_email'],  # 校验email
            real_mobile=r['real_mobile'],  # 校验手机号
            is_pause=True if r['is_pause'] else False,  # 是否为暂停
            pause_datetime=r['pause_datetime'],  # 暂停时间
            deadline=r['deadline'],  # 试学到期时间
            province=r['province_name'],
            city=r['city_name'],  # 城市
            study_goal=get_study_goal(r['is_employment_contract']),  # 学习目标
            degree=UserJobInfo.DEGREES.get(r['degree'], ''),  # 学历
            join_in_class_time=r['created'],  # 加入班级时间
            student_status=r['status'],  # 学生状态
            quit_time=r['quit_datetime'],  # 退学时间
            nick_name=r['nick_name'],
            qq=r['qq'],
            avatar_small_thumbnall=r['avatar_small_thumbnall']
        )

    return result


class LPS4StudentsInterface(object):
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

    def __init__(self, teacher_id, career_id, class_id):
        self.teacher_id = teacher_id
        self.career_id = career_id
        self.class_id = class_id
        self._load()

    def _load(self):
        # 只接受LPS3的班级 或 LPS4
        self._status = {'graduate': [], 'finish': [], 'normal': [], 'paused': [], 'quit': [], 'behind': []}

        self.students = get_students(self.teacher_id, self.career_id)
        self.students_show_info = students_show_info(self.career_id, self.students)
        self.iface = StageTaskInterface(self.class_id)
        self.iface.load_students_data(list(student.id for student in self.students))

        self.students_type = get_student_type_by_students(self.students, self.career_id)
        self.onevone_counts = teacher_unread_num(self.students, self.class_id, self.teacher_id)  # 一对一服务 未读信息

        for student in self.students:
            student_id = student.id
            show_info = self.students_show_info.get(student_id)
            if student.end_time < datetime.datetime.now():  # 班级一毕业
                self._status['graduate'].append(student_id)
                continue
            if show_info['student_status'] == ClassStudents.STATUS_QUIT:  # 退学
                self._status['quit'].append(student_id)
                continue
            if student.is_stop:  # 休学的
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

    @cached_property
    def data(self):
        ret = list()
        for student in self.students:
            student_id = student.id
            show_info = self.students_show_info.get(student_id)
            student_status = self.get_student_status(student_id)
            data = dict()

            data.update(self._status_attrs(student_status))

            data['class_id'] = self.class_id
            data['career_id'] = self.career_id
            data['model'] = student
            data['show_info'] = show_info

            data['is_full_payment'] = self.students_type.get(student_id) in (0, 1)
            data['student_status'] = student_status
            data['show_student_status'] = self.STUDENT_STATUS.get(student_status)
            data['show_name'] = data['show_info']['real_name'] or student.nick_name

            if student_status == self.STUDENT_GRADUATE:
                # 毕业时间
                data['graduate_date'] = student.end_time
            if student_status == self.STUDENT_QUIT:
                quit_time = show_info['quit_time']
                # 退学时间
                data['quit_date'] = quit_time.date().isoformat() if quit_time else ''

            data['show_status_gray'] = student_status in (self.STUDENT_QUIT, self.STUDENT_GRADUATE, self.STUDENT_PAUSED)

            data['stages'] = self.iface.get_student_data(student_id)
            data['can_be_operated'] = not (student_status in (self.STUDENT_QUIT, self.STUDENT_GRADUATE))
            data['type'] = self.students_type.get(student_id)   # 用户是保就业还是免就业
            data['onevone_count'] = self.onevone_counts.get(student_id, {})
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


def student_create_service(user, source, career_id):
    """
    学生端新建学习建议接口
    :param user:
    :param source:
    :param career_id:
    :return:
    """
    result = get_teacher_by_lps4(career_id=career_id, student_id=user.id)
    if result.is_error():
        return False
    teacher_id = result.result()['teacher_id']
    result = get_user_name(user_id=teacher_id)
    if result.is_error():
        return False
    teacher_name = result.result()['real_name'] or result.result()['nick_name']

    content = '我正在学习 %s ，请老师给我一点建议吧~' % source.split('-')[-1]
    data = {'career_id': career_id, 'student_id': user.id, 'teacher_id': teacher_id,
            'teacher_nick_name': teacher_name,
            'teacher_avatar_url': str(result.result()['avatar_url']),
            'now': datetime.datetime.now(), 'source_type': 0, 'source': source,
            'content': content, 'user_id': user.id,
            'user_nick_name': user.real_name or user.nick_name,
            'user_avatar_url': str(user.avatar_url), 'teacher_unread': 1,
            'student_unread': 0, 'is_student': True}
    result = create_new_service(**data)
    if result.is_error():
        log.error(
            'when create_onevone_service in student_create_service raise a error')
        return False
    return True


def student_join_class_create_service(user, career_id, career_name):
    """
    学生端新建学习建议接口(新学员入班)
    :param user:
    :param career_id:
    :param career_name:
    :return:
    """

    result = get_teacher_by_lps4(career_id=career_id, student_id=user.id)
    if result.is_error():
        return False
    teacher_id = result.result()['teacher_id']

    # 加入消息队列
    result = db.api.course.career_course.get_institute_by_career_id(career_id)
    institute = {}
    if not result.is_error():
        institute = result.result()
    mq_data = mq_service.publish({
        "event": "user_study_info_perfect_sync",
        "data": {
            "user_id": str(user.id),
            "domain": institute.get('name')
        }
    })
    log.info('mq_data_user_study_info_perfect_sync: %s' % str(mq_data))
    mq_data = mq_service.publish({
        "event": "notify_teacher_time_sync",
        "data": {
            "user_id": str(user.id),
            "career_id": career_id,
            "notify_teacher_time": datetime.datetime.now().strftime("%F %T")
        }
    })
    log.info('mq_data_notify_teacher_time_sync: %s' % str(mq_data))

    # 学习目标
    study_goal_str = '其他'
    result = db.api.lps.student.student_study_goal(user_id=int(user.id), career_id=int(career_id))
    if result.is_error():
        log.warn('db.api.lps.student.student_study_goal failed : user_id=%s, career_id=%s' % (user.id, career_id))
    else:
        if result.result():
            study_goal_str = result.result()['name']

    # 学习基础
    study_base_str = ""
    result = db.api.lps.student.get_lps_3_institute_name_by_career_id(career_id)
    if result.is_error():
        log.warn('')
    if result.result():
        institute_name = result.result()['name']
        study_base_list = get_study_base(user.id, institute_name)
        if study_base_list:
            study_base_str_begin = '<p>&nbsp;&nbsp;&nbsp;&nbsp;我的学习基础情况：</p>' \
                                   '<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            study_base_str_middle = '</p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'.join(
                                [study_base['name']+'，'+study_base['level']+';' for study_base in study_base_list])
            study_base_str_end = '</p>'
            study_base_str = study_base_str_begin+study_base_str_middle+study_base_str_end
        else:
            study_base_str = ''

    result = get_user_name(user_id=teacher_id)
    if result.is_error():
        return False
    teacher_name = result.result()['real_name'] or result.result()['nick_name']
    str_mobile = '我的电话是：%s，' % user.mobile if user.mobile else ''
    str_email = '我的邮箱是：%s，' % user.email if user.email else ''
    str_qq = '我的QQ号是：%s。' % user.qq if user.qq else ''
    str_wechat = '我的微信号是：%s。' % user.wechat if user.wechat else ''
    content = '<p>老师您好：</p>' \
              '<p>&nbsp;&nbsp;&nbsp;&nbsp;我刚加入您的%s课程进行1V1学习。%s%s%s%s</p>' \
              '<p>&nbsp;&nbsp;&nbsp;&nbsp;我的学习目标：%s</p>%s' \
              '<p>麻烦老师帮我制定下符合我个人情况的学习建议吧！</p>' % (
                  career_name, str_mobile, str_email, str_qq, str_wechat,
                  study_goal_str, study_base_str)

    data = {'career_id': career_id, 'student_id': user.id, 'teacher_id': teacher_id,
            'teacher_nick_name': teacher_name,
            'teacher_avatar_url': str(result.result()['avatar_url']),
            'now': datetime.datetime.now(), 'source_type': 0, 'source': None,
            'content': content, 'user_id': user.id,
            'user_nick_name': user.real_name or user.nick_name,
            'user_avatar_url': str(user.avatar_url), 'teacher_unread': 1,
            'student_unread': 0, 'is_student': True}

    result = create_new_service(**data)
    if result.is_error():
        log.error(
            'when create_onevone_service in student_join_class_create_service raise a error')
        return False
    return True


# 判断该班级是否是lps4的班级
def is_lps_class(class_id):
    result = class_dict.LPS4_DICT.get(int(class_id))
    if result:
        return result
    return None


def generate_oneveone_meeting(teacher_id):
    """
    根据老师生成一个假的一对一直播
    :param teacher_id:
    :return:
    """
    teacher = db.api.user.user.get_user_by_id(teacher_id).result()
    _date = datetime.datetime.now() + datetime.timedelta(days=1)

    if teacher:
        oneveone_meeting = dict(
            id=0,
            status='CREATE',
            teacher_head=teacher.get('avatar_url'),
            teacher_nick_name=teacher.get('nick_name'),
            teacher_real_name=teacher.get('real_name'),
            start_time=datetime.datetime(_date.year, _date.month, _date.day, 20),
            end_time=datetime.datetime(_date.year, _date.month, _date.day, 20, 30)
        )
    else:
        oneveone_meeting = None

    return oneveone_meeting


def serialize_onevone_meeting_date(teacher_id):
    """
    组织班会日期
    :param teacher_id:
    :return:
    """
    meetings = []
    now_after_3 = datetime.datetime.now() + datetime.timedelta(hours=3)
    _meetings = db.api.onevone.meeting.get_onevone_meeting_can_be_date(teacher_id, now_after_3)

    if _meetings.is_error():
        log.warn('get_onevone_meeting_can_be_date is error teacher_id is %s' % teacher_id)
    else:
        meetings = list(_meetings.result())

    s_meetings = []
    for m in meetings:
        week_key = int(m['start_time'].strftime('%w'))
        week_dict = {1: u'一', 2: u'二', 3: u'三', 4: u'四', 5: u'五', 6: u'六', 0: u'日'}
        weekday = week_dict[week_key]
        data = dict(
            m_id=m['id'],
            m_time='%s-%s' % (m['start_time'].strftime('%H:%M'), m['end_time'].strftime('%H:%M')),
            m_day=weekday,
            m_date=m['start_time'].strftime('%Y-%m-%d')
        )
        s_meetings.append(data)

    return s_meetings


def get_onevone_meeting(meeting_id):
    """
    1v1直播详情
    :param meeting_id:
    :return:
    """

    result = db.api.onevone.meeting.get_onevone_meeting_by_id(meeting_id)
    if result.is_error():
        log.warn('get_onevone_meeting_by_id is error meeting_id:%s' % meeting_id)
        return failed_json()
    onevone_meeting = result.result()

    try:
        is_video = onevone_meeting.get('status', 'CREATE') == 'ENDED'
        join_url = update_join_url(onevone_meeting, is_video=is_video)
    except Exception as e:
        log.warn(str(e))
    else:
        onevone_meeting.update({'join_url': join_url})

    return onevone_meeting


def get_onevone_meeting_range_by_user_id_interface(teacher_id, user_id=0):
    """
    获取用户的班会范围
    :param teacher_id:
    :param user_id:
    :return:
    """
    now = datetime.datetime.now()
    now_after_3 = now + datetime.timedelta(hours=3)
    _result = db.api.onevone.meeting.get_onevone_created_meeting_range_by_teacher_id(teacher_id, now_after_3)
    if user_id:
        _result = db.api.onevone.meeting.get_onevone_meeting_range_by_user_id(teacher_id, now_after_3, user_id)
    if _result.is_error():
        log.warn('get_onevone_meeting_range_by_user_id is error teacher_id:%s user_id:%s' % (teacher_id, user_id))
        return failed_json()
    result = _result.result()
    if result:
        start_time = result['start_time']
        end_time = result['end_time']
    else:
        start_time = now
        end_time = now + datetime.timedelta(600)

    if end_time is None:
        end_time = start_time = now
        if end_time < now:
            end_time = now

    return start_time.strftime('%Y-%m-%d'), end_time.strftime('%Y-%m-%d')


def serialize_onevone_meeting_time_list(career_id, user_id):
    now = datetime.datetime.now()
    end_date = (now + datetime.timedelta(8)).date()
    today = datetime.date.today()
    today_0 = datetime.datetime(today.year, today.month, today.day)

    result = db.api.onevone.meeting.get_created_onevone_meeting(career_id, user_id, end_date)
    if result.is_error():
        log.warn('get_created_onevone_meeting is error career_id:%s user_id:%s' % (career_id, user_id))
        return False
    meeting_tuple = result.result()

    try:
        meeting_list = [m['start_time'] for m in meeting_tuple]
        date_list = []
        for d in map(lambda x: today_0 + datetime.timedelta(x), range(0, 8)):
            hour_list = []
            for h in range(9, 23):
                if d + datetime.timedelta(hours=h) > now:
                    minutes_list = []
                    for m in (0, 30):
                        _time = d + datetime.timedelta(hours=h, minutes=m)
                        if _time > now + datetime.timedelta(minutes=30):
                            if _time in meeting_list:
                                available = False
                            else:
                                available = True
                            minutes_list.append(dict(
                                minute=str(m),
                                available=available
                            ))
                    hour_list.append(dict(
                        hour=str(h),
                        minutes_list=minutes_list
                    ))

            if hour_list:
                date_list.append(dict(
                    date=d.strftime('%F'),
                    hour_list=hour_list
                ))
    except Exception as e:
        log.warn(str(e))
        return False

    result = db.api.onevone.meeting.get_onevone_meeting_user_count(user_id, career_id)
    if result.is_error():
        log.warn('get_onevone_meeting_user_count is error career_id:%s user_id:%s' % (career_id, user_id))
        return False
    max_num = result.result()

    return dict(max_num=max_num, date_list=date_list)


def get_student_meeting_list_interface(career_id, user, is_web=False):
    """
    获取学生班会列表接口
    :param career_id:
    :param user:
    :param is_web: 是否是web端调用
    :return:
    """
    try:
        # 未开始直播
        onevone_meeting_list = get_student_meeting_list(career_id, user, is_web)
        # 往期直播
        onevone_old_meeting_list = get_student_meeting_list(career_id, user, is_web, is_old=True)
    except Exception as e:
        log.warn(str(e))
        raise Exception(str(e))

    return {'onevone_meeting_list': onevone_meeting_list,
            'onevone_old_meeting_list': onevone_old_meeting_list,
            'status': 1}


def get_student_meeting_list(career_id, user, is_web, is_old=False):
    """
    获取学生端约课列表
    :return:
    """
    status_dict = OnevoneMeeting.STATUS_DICT
    # 未开始直播
    result = db.api.onevone.meeting.app_get_ordered_onevone_meeting(career_id, user.id, is_old=is_old)
    if result.is_error():
        log.warn('app_get_ordered_onevone_meeting error.career_id %s, user_id %s' % (career_id, user.id))
        raise Exception(u'服务器开小差了,稍后再试吧')
    onevone_meeting_list = []
    for meeting in result.result():
        meeting_dict = {
            "status": status_dict.get(meeting['status'], '0'),
            "avatar": settings.SITE_URL + settings.MEDIA_URL + meeting['teacher_head'],
            "teacher_name": meeting['teacher_real_name'] or meeting['teacher_nick_name'],
            "start_time": meeting['start_time'].strftime('%H:%M'),
            "end_time": meeting['end_time'].strftime('%H:%M'),
            "datetime": meeting['start_time'].strftime('%Y/%m/%d'),
            "week_time": week_day_dict[meeting['start_time'].weekday()],
            "nick_name": user.real_name or user.nick_name,
            "token": meeting['student_client_token'],
            "room_number": meeting['live_code'],
            "id": str(meeting['id']),
        }
        # web端特有需要的参数
        if is_web:
            meeting_dict.update({
                "create_time": meeting['create_date_time'].strftime('%Y年%m月%d日 %R'),
                "start_year": meeting['start_time'].strftime('%Y年%m月%d日'),
                "question": strip_tags(meeting['question']) if meeting['question'] else '',
                "teacher_id": meeting['teacher_id']
            })
            try:
                join_url = update_join_url(meeting, is_video=is_old)
            except Exception as e:
                log.warn(str(e))
            else:
                meeting_dict.update({'join_url': join_url})

        onevone_meeting_list.append(meeting_dict)

    return onevone_meeting_list


