# -*- coding: utf-8 -*-

__author__ = 'guotao'
import json
import requests
from django.conf import settings
from datetime import date, timedelta, datetime
from functions import create_liveroom, write_class_rank_change_message
from mz_lps3.models import UserTaskRecord, ClassRank, ClassMeeting, ClassMeetingRelation, ClassMeetingMobileRecord
from mz_course.models import Stage
from mz_common.mz_log2mongo import MzL2M, LPS3_ClassOpType
from mz_lps.models import ClassStudents
from mz_lps3.models import ClassRankRecord
from mz_lps3.functions import StageTaskInterface, CustomJsonEncode
from mz_lps3.functions_gt import get_attendance_info
from mz_lps3.functions import write_absent_user_message, write_class_meeting_open_message
from utils.sms_manager import send_sms, get_templates_id

LOGGER_TORNADO = ['1m_lps3']  # 指定loger位置,目的是为了解决tornado多进程时log日志文件句柄被占用的问题
logger = MzL2M.getLogger("mongodb_logger")


def create_classmeeting(user_class, pre_startline=None):
    """
    创建下周直播班会
    """
    # 如果是新建的班级并且没有学生则不创建班会,如果班会没有开启也不创建班会
    if user_class.students.count() < 1 or user_class.meeting_enabled == False:
        return
    if pre_startline:
        # 依据上次直播班会时间创建下周班会
        startline = pre_startline + timedelta(7)
    else:
        today = date.today()
        startline = today + timedelta(7 - today.isoweekday())
        startline = datetime.strptime(str(startline) + ' 20:00:00', '%Y-%m-%d %H:%M:%S')
    try:
        classmeeting = ClassMeeting.objects.create(startline=startline, status=0, content='周直播班会', is_temp=False,
                                                   create_id=user_class.teacher.id)
        classmeeting_relation = ClassMeetingRelation.objects.create(class_meeting=classmeeting, class_id=user_class.id)
        flags, log = create_liveroom(user_class.teacher, classmeeting, [user_class])  # 创建班会后，创建直播室
        if flags:
            infodict = dict(task_type=LOGGER_TORNADO[0], class_id=user_class.id,
                            user_oper_type=LPS3_ClassOpType.LIVEROOM_CREATED,
                            classmeeting_id=classmeeting.id)
            logger.cache(infodict)
            # 创建班会后,计算班级排名(不需要再计算周排名)
            # calc_classrank=CalcClassRank(user_class)
            # calc_classrank.calc_classrank(classmeeting.id)

            infodict = dict(task_type=LOGGER_TORNADO[0], class_id=user_class.id,
                            user_oper_type=LPS3_ClassOpType.MEETING_CREATED,
                            classmeeting_id=classmeeting.id)
            logger.cache(infodict)
        else:
            classmeeting_relation.delete()
            classmeeting.delete()
            infodict = dict(task_type=LOGGER_TORNADO[0], class_id=user_class.id,
                            user_oper_type=LPS3_ClassOpType.LIVEROOM_CREATED_LOG,
                            classmeeting_id=classmeeting.id, log=log)
            logger.cache(infodict)
    except Exception, e:
        logger.error(e, task_type=LOGGER_TORNADO[0], calss_id=user_class.id)


class CalcClassRank(object):
    """
    计算班级排名
    """

    def __init__(self, user_class):
        self.user_class = user_class
        self.stage_taskrel = self._get_stage_taskrel_by_class_id(user_class)

    def _get_stage_taskrel_by_class_id(self, user_class):
        """
        获取班级的所有阶段——任务关联表的ID
        :param class_id:班级id
        """
        stage_taskrel = list()
        # 取出职业课程下的阶段
        # 加过滤条件,区分lps3. stage中,如何区分是lps3的阶段
        stages = Stage.objects.xall().filter(lps_version='3.0', career_course=user_class.career_course).order_by(
            'index')
        # 根据阶段找到任务
        for stage in stages:
            ts = stage.stagetaskrelation_set \
                .values('id', 'name', 'index', 'task__name', 'task__id', 'task__expect_time', 'task__excellent_time')
            for item in ts:
                stage_taskrel.append(item.get('id'))
        return stage_taskrel

    def get_stu_score(self, user_class):
        """
        获取制定班级下用户的成绩列表
        """
        dict_score = {'A': 3, 'B': 2, 'C': 1}
        stu_score_lst = []
        class_stu_set = ClassStudents.objects.filter(student_class=user_class,
                                                     status=ClassStudents.STATUS_NORMAL).exclude(is_pause=True)
        for class_stu in class_stu_set:
            total_a = 0
            uts = UserTaskRecord.objects.filter(class_id=user_class.id, student_id=class_stu.user.id, status='PASS')
            for ut in uts:
                if ut.stage_task.id in self.stage_taskrel:
                    total_a += dict_score.get(ut.score, 0)
            user_name = class_stu.user.real_name if class_stu.user.real_name else class_stu.user.nick_name  # 优先使用真名,然后才是昵称
            stu_score_lst.append([class_stu.user.id, total_a, user_name, class_stu.user.avatar_url])

        return stu_score_lst

    def calc_classrank(self, classmeeting_task_id):
        """
        计算特定班级本周排名（从0开始）
        :param user_class:班级对象
        """
        try:
            # 进行排名排序
            stu_score_lst = self.get_stu_score(self.user_class)
            sorted_stu_score_lst = sorted(stu_score_lst, key=lambda e: e[1], reverse=True)
        except Exception, e:
            # print e
            logger.error(e, task_type=LOGGER_TORNADO[0], calss_id=self.user_class.id)
            return
        # 获取上周的班会ID
        classmeeting_lst = ClassMeeting.objects.filter(classmeetingrelation__class_id=self.user_class.id,
                                                       is_temp=False, status=1).order_by('-id')[:1]
        # 将排名写入数据库
        for i in xrange(len(sorted_stu_score_lst)):
            try:
                class_rank = ClassRank()
                class_rank.class_id = self.user_class.id
                class_rank.classmeeting_id = classmeeting_task_id
                class_rank.student_id = sorted_stu_score_lst[i][0]
                class_rank.rank = i + 1
                class_rank.total_score = sorted_stu_score_lst[i][1]
                class_rank.rank_change = 0
                if classmeeting_lst:
                    pre_classrank = ClassRank.objects.filter(class_id=self.user_class.id,
                                                             classmeeting_id=classmeeting_lst[0].id,
                                                             student_id=sorted_stu_score_lst[i][0])[:1]
                    if pre_classrank:
                        class_rank.rank_change = pre_classrank[0].rank - class_rank.rank
                class_rank.save()
                # 计算排名后，写入消息系统
                write_class_rank_change_message(class_rank.student_id, class_rank.class_id, class_rank.rank_change)
                # 积分计算
                _url = settings.FPS_HOST + 'service/ticket/'
                if class_rank.rank <= 3:  # 进入前3名次
                    requests.put(url=_url, data={'user_id': class_rank.student_id, 'op_type': 'first_third_rank'},
                                 timeout=2)
                if len(sorted_stu_score_lst) - class_rank.rank <= 3:
                    requests.put(url=_url, data={'user_id': class_rank.student_id, 'op_type': 'last_third_rank'},
                                 timeout=2)
            except Exception, e:
                logger.error(e, task_type=LOGGER_TORNADO[0], calss_id=self.user_class.id)

    def calc_classrank_score(self):
        """
        计算班级同学的成绩排名，与函数calc_classrank的作用类似，但不写数据
        :return:
        """
        ranks = sorted(self.get_stu_score(self.user_class), key=lambda e: e[1], reverse=True)  # 进行排名排序
        for k, v in enumerate(ranks):
            v.insert(0, k + 1)  # 插入排名
        pattern = ['rank', 'student_id', 'score', 'nick_name', 'avatar_url']
        return dict(class_id=self.user_class.id, rank_type='1', rank_detail=map(lambda x: dict(zip(pattern, x)), ranks))

    def calc_classrank_progress(self):
        """
        计算班级进度排名
        """
        total = StageTaskInterface(self.user_class.id).count_all_tasks()  # 班级全部任务
        student_progress_list = []
        # 获取全部同学
        class_students = ClassStudents.objects.filter(student_class=self.user_class,
                                                      status=ClassStudents.STATUS_NORMAL).exclude(is_pause=True)
        for student in class_students:
            finished = UserTaskRecord.objects.filter(class_id=self.user_class.id, student_id=student.user.id,
                                                     status__in=['DONE', 'PASS']).count()
            progress = float(finished) / total
            user_name = student.user.real_name if student.user.real_name else student.user.nick_name  # 优先使用真名,然后才是昵称
            student_progress_list.append([student.user.id, progress, user_name, student.user.avatar_url])
        ranks = sorted(student_progress_list, key=lambda x: x[1], reverse=True)
        for k, v in enumerate(ranks):
            v.insert(0, k + 1)
        pattern = ['rank', 'student_id', 'progress', 'nick_name', 'avatar_url']
        return dict(class_id=self.user_class.id, rank_type='2', rank_detail=map(lambda x: dict(zip(pattern, x)), ranks))


def calc_rank_change(new_ranks, old_ranks):
    """
    批量计算排名变化，new_ranks为新的排名，　old_ranks为旧排名，　详细定义如下：
    :param new_ranks:   新排名的列表，格式为
                        [{  class_id: 5,
                            rank_type: '1',
                            rank_details = [{   rank: 8,
                                                student_id: 8,
                                                score: 30 or progress 0.68,
                                                nick_name: qlp,
                                                avatar_url: /uploads/avatar_url/photo.img
                                            },
                                            ...,
                                            {}]
                         },
                        ...,
                        {},]
            注意，该例子中的 rank_details 是以　班级成绩每天排名　的业务逻辑进行举例，其格式可以由不同的业务逻辑决定
    :param old_ranks:   旧排名的列表，格式为
                        [{  class_id: 5,
                            rank_type: '1',
                            rank_details = [{   rank: 8,
                                                student_id: 8,
                                                score: 30 or progress 0.68,
                                                nick_name: qlp,
                                                avatar_url: /uploads/avatar_url/photo.img
                                                rank_change: -5
                                            },
                                            ...,
                                            {}]
                         },
                        ...,
                        {},]
            注意，该例子中的 rank_details 是以　班级成绩每天排名　的业务逻辑进行举例，其格式可以由不同的业务逻辑决定
    :return:
    计算步骤如下：
    1. 循环new_ranks中的每个班级排名，临时命名为every_rank, 并做如下处理：
        2.  判断old_ranks中，改班级排名是否存在
            若存在：　（说明有该班级的旧排名）
                循环every_rank.rank_details中每条记录（即，遍历改班级排名中，每位同学的排名记录），并作如下处理：
                    判断该同学在该班级的旧的排名记录中，是否有排名记录
                    若有：
                        则用该同学的新排名减去就排名，作为rank_change
                    若为：
                        则该同学可能为新的同学，rank_change 设置为０
            如不存在：
                将every_rank中的每位同学的班级排名变化（rank_change）全部设为０
    """
    for new_rank in new_ranks:
        # 过滤昨天的对应班级的排名，班级有可能为新班级
        old_rank = filter(lambda x: True if x['class_id'] == new_rank['class_id'] else False, old_ranks)
        if old_rank:  # 该班级昨天的排名存在
            for student_rank in new_rank['rank_detail']:  # 判断每个同学的排名变化
                old_student_rank = filter(lambda x: True if x['student_id'] == student_rank['student_id'] else False,
                                          old_rank[0]['rank_detail'])
                if old_student_rank:  # 如果某位同学之前的排名记录存在
                    # 如果排名记录存在，但昨天的排名字段却不存在，防御性处理
                    _old_student_rank = old_student_rank[0].get('rank')
                    student_rank['rank_change'] = _old_student_rank - student_rank['rank'] if _old_student_rank else 0
                else:  # # 如果某位同学之前的排名记录不存在, 那么认为该同学可能为新同学，认为成绩没有变化
                    student_rank['rank_change'] = 0
        else:  # 该班级昨天的排名并不存在, 将改该班级每位同学的排名变化设置为０
            for student_rank in new_rank['rank_detail']:
                student_rank['rank_change'] = 0
    return new_ranks


def write_class_rank_record(records):
    """
    批量将班级排名数据记录进入数据库
    :param records: 班级排名的数据，类型为列表，元素为字典
    :return: true if success else false
    """
    assert isinstance(records, list)
    for record in records:  # 序列化
        record['rank_detail'] = json.dumps(record['rank_detail'], cls=CustomJsonEncode)
    record_entries = [ClassRankRecord(**record) for record in records]
    ClassRankRecord.objects.bulk_create(record_entries)


def get_class_rank_record(class_id, rank_type, rank_number='all'):
    """
    :param class_id: 课程Id
    :param rank_type: 排名类型
    :param rank_number: 默认为'all',返回全部, 若为'top3'则返回前三名
    :return:
    """
    record = ClassRankRecord.objects.filter(class_id=class_id, rank_type=rank_type).order_by('-rank_date').first()
    if rank_number == 'all':
        ranks = json.loads(record.rank_detail)
        if rank_type == '1':
            for rank in ranks:
                rank['score'] = rank['score'] * 10
        return ranks
    elif rank_number == 'top3':
        ranks = json.load(record.rank_detail)[:3]
        if rank_type == '1':
            for rank in ranks:
                rank['score'] = rank['score'] * 10
        return ranks


def send_sms_start_class_meeting(each_class, class_meeting):
    """
    班会开始前15分钟提醒
    :param each_class:
    :param class_meeting:
    :return:
    """
    try:
        class_id_lst = ClassMeetingRelation.objects.filter(class_meeting=class_meeting).values_list(
            "class_id", flat=True)
        class_students_lst = ClassStudents.objects.filter(student_class_id__in=class_id_lst, is_pause=False,
                                                          status=ClassStudents.STATUS_NORMAL)
        for class_students in class_students_lst:
            if not class_students.is_active:
                continue
            # student_infos=StudentInfo.objects.filter(student_id=class_students.user.id)
            # if student_infos:
            #     mobile=student_infos[0].mobile
            # 班会开始前将用户信息写入消息提醒
            write_class_meeting_open_message(class_students.user.id, class_meeting.id)
            # 班会开始前给用户发送短信提醒
            if class_students.user.mobile and class_students.user.valid_mobile == 1:
                mobile = class_students.user.mobile

                delta_time = class_meeting.startline - datetime.now()
                if delta_time.total_seconds() >= 0 and delta_time <= timedelta(minutes=15):
                    send_sms(settings.SMS_APIKEY, get_templates_id('classmeeting_notify'),
                             mobile.encode('utf-8'), class_meeting.content.encode('utf-8'),
                             class_meeting.startline.strftime('%Y年%m月%d日%H时%M分'))
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e, task_type=LOGGER_TORNADO[0], class_id=each_class.id, method=send_sms.__name__,
                         class_meeting_id=class_meeting.id, info='classmeeting_notify')
    else:
        logger.cache(dict(task_type=LOGGER_TORNADO[0], class_id=each_class.id, method=send_sms.__name__,
                          class_meeting_id=class_meeting.id, info='classmeeting_notify'))


def send_sms_attendance(each_class, class_meeting):
    """
    考勤以及缺勤短信
    :param each_class:
    :param class_meeting:
    :return:
    """
    try:
        get_attendance_info(class_meeting)
        # _, _, _, absent_class_student_lst = get_attendance_info(class_meeting)
        # for class_student in absent_class_student_lst:
        #     if not class_student.is_active:
        #         continue
        #     absent_user = class_student.user
        #     # 缺勤班会的用户写入消息提醒
        #     write_absent_user_message(absent_user.id, class_meeting.id)
        #     # 给缺勤的用户发送短信
        #     if absent_user.mobile and absent_user.valid_mobile == 1:
        #         mobile = absent_user.mobile
        #         send_sms(settings.SMS_APIKEY, get_templates_id('classmeeting_absence'),
        #                  mobile.encode('utf-8'), class_meeting.content.encode('utf-8'),
        #                  class_meeting.startline.strftime('%Y年%m月%d日%H时%M分'))
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e, task_type=LOGGER_TORNADO[0], class_id=each_class.id, method=send_sms.__name__,
                         class_meeting_id=class_meeting.id, info='classmeeting_absence')
    else:
        logger.cache(dict(task_type=LOGGER_TORNADO[0], class_id=each_class.id, method=send_sms.__name__,
                          class_meeting_id=class_meeting.id, info='classmeeting_absence'))


def send_sms_start_class_meeting_free(each_class, class_meeting):
    """
    免费试学班会开始前3个小时提醒
    :param each_class:
    :param class_meeting:
    :return:
    """
    try:
        class_record = ClassMeetingMobileRecord.objects.get(class_meeting=class_meeting)
        if class_record.start_3hour_ago:
            return
    except ClassMeetingMobileRecord.DoesNotExist:
        pass
    try:
        class_id_lst = ClassMeetingRelation.objects.filter(class_meeting=class_meeting).values_list(
            "class_id", flat=True)
        class_students_lst = ClassStudents.objects.filter(student_class_id__in=class_id_lst, is_pause=False,
                                                          status=ClassStudents.STATUS_NORMAL)
        for class_students in class_students_lst:
            if class_students.status == 2:  # 退学
                continue
            # 班会开始前给用户发送短信提醒
            if class_students.user.mobile and class_students.user.valid_mobile == 1:
                mobile = class_students.user.mobile
                send_sms(settings.SMS_APIKEY, get_templates_id('start_free_class_meeting_3hour'),
                         mobile, each_class.career_course.name,
                         class_meeting.startline.strftime('%Y年%m月%d日%H时%M分'))
        ClassMeetingMobileRecord.objects.create(start_3hour_ago=True, class_meeting=class_meeting)
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e, task_type=LOGGER_TORNADO[0], class_id=each_class.id, method=send_sms.__name__,
                         class_meeting_id=class_meeting.id, info='start_free_class_meeting_3hour')
    else:
        logger.cache(dict(task_type=LOGGER_TORNADO[0], class_id=each_class.id, method=send_sms.__name__,
                          class_meeting_id=class_meeting.id, info='start_free_class_meeting_3hour'))
