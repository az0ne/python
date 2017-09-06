# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404

from mz_lps.models import Class, ClassStudents
from mz_lps3 import functions
from mz_lps3.models import ClassRank, ClassRankRecord
from mz_user.models import UserProfile


def get_rank_record(class_id, rank_type):
    """ author: feng
    获取班级排名记录
    :param class_id: 班级id
    :param rank_type: 排名类型 '1': '班级成绩每天排名', '2': '班级进度每天排名'
    :return: 排行榜
    """
    rank = ClassRankRecord.objects.filter(
        class_id=class_id, rank_type=rank_type).order_by('-rank_date').first()
    if rank:
        rank = json.loads(rank.rank_detail)
        return sorted(rank, key=lambda x: x['rank'])    # 按排名正序排序
    return []


def get_grade_rank_of_class(class_id, num=-1):
    """ author: feng
    获取班级学生成绩排名
    :param class_id: 班级id
    :param num: 取前几名 -1表示所有
    :return: 排行榜
    """
    grade_rank = get_rank_record(class_id, '1')

    if len(grade_rank) < num or num == -1:
        return grade_rank
    return grade_rank[:num]


def get_progress_rank_of_class(class_id, num=-1):
    """ author: feng
    获取班级学生进度排名
    :param class_id: 班级id
    :param num: 取前几名 -1表示所有
    :return: 排行榜
    """
    progress_rank = get_rank_record(class_id, '2')

    if len(progress_rank) < num or num == -1:
        return progress_rank
    return progress_rank[:num]


def _filter_rank_by_student_id(rank, student_id):
    """ author: feng
    根据学生id获取排名
    :param rank: 班级总排行
    :param student_id: 学生id
    :return: 个人排行
    """
    info = [r for r in rank if r['student_id'] == int(student_id)]
    return info[0] if info else {}


def get_rank_of_class_student(class_id, student_id):
    """ author: feng
    根据班级id跟学生id，获取成绩排名详情
    :param class_id: 班级id
    :param student_id: 学生id
    :return: 个人排名详情
    """
    grade_rank = get_rank_record(class_id, '1')
    # progress_rank = get_rank_record(class_id, '2')
    grade_info = _filter_rank_by_student_id(grade_rank, student_id)
    # progress_info = _filter_rank_by_student_id(progress_rank, student_id)
    return grade_info


def format_date(time):
    """ author: feng
    格式化时间
    :param time: 时间
    :return: 格式化时间
    """
    assert isinstance(time, datetime), 'date type must be datetime'
    return time.strftime("%Y%m%d")


def add_date(time, days):
    """ author: feng
    格式化时间
    :param time: 时间
    :param days: 加多少天
    :return: 格式化时间
    """
    return time + timedelta(days=days)


def count_down(time):
    """ author: feng
    根据时间计算倒计时
    :param time: 时间
    :return: 剩余时间
    """
    time = datetime(time.year, time.month, time.day)
    now = datetime.now()
    now = datetime(now.year, now.month, now.day)
    return time - now


def count_down_days(time):
    """ author: feng
    根据时间计算倒计时
    :param time: 时间
    :return: 剩余天数
    """
    return count_down(time).days


def get_top_data(student, sclass):
    """ author: feng
    获取顶部公用数据
    :param student: 学生
    :param sclass: 班级
    :return: 顶部公用数据
    """
    # 应对传的id过来
    if isinstance(student, (int, str, unicode)):
        student = UserProfile.objects.get(pk=student)
    if isinstance(sclass, (int, str, unicode)):
        class_student = get_object_or_404(
            ClassStudents, student_class_id=sclass, user_id=student)
        sclass = class_student.student_class

    if sclass.meeting_enabled:
        end_time = add_date(sclass.meeting_start or datetime.now(),
                            sclass.meeting_duration or 90)
        class_time_left = count_down_days(end_time)     # 毕业倒计时
    else:
        class_time_left = u'未开始'

    class_students_count = sclass.current_student_count     # 班级总人数

    # 班级排名
    class_rank = get_rank_of_class_student(sclass.id, student.id)
    # 排名
    rank_number = class_rank['rank'] if class_rank else 0
    # 排名浮动
    rank_change_num = class_rank['rank_change'] if class_rank else 0
    if rank_change_num and rank_change_num > 0:
        rank_change_status = 'up'
    elif rank_change_num and rank_change_num < 0:
        rank_change_status = 'down'
    else:
        rank_change_status = 'up'
    rank_change_num = abs(rank_change_num)

    # 计算学习进度
    st_interface = functions.StageTaskInterface(sclass.id)
    total = st_interface.count_all_tasks()
    st_interface.load_student_data(student.id)
    done = st_interface.count_student_tasks_finished(student.id)  # 完成数量
    total_progress = int(round(done * 100.0 / total)) if total else 100

    return {
        'userinfo': student,     # 当前学生
        'sclass': sclass,      # 当前班级
        'is_unlockstage': student.is_unlockstage,   # 是否是企业直通班学员
        'student_count': class_students_count,  # 班级总人数
        'rank_number': rank_number,     # 当前学生排名
        'rank_change_status': rank_change_status,   # 排名上升还是下降
        'rank_change_num': rank_change_num,     # 改变的名次
        'class_time_left': class_time_left,      # 离毕业还有多少天
        'total_progress': total_progress        # 学习总进度
    }
