# -*- coding: utf-8 -*-


__author__ = 'changfu'

import json
import datetime
import djevn
djevn.load()

from mz_lps.models import Class
from mz_lps3.calc_functions import CalcClassRank, calc_rank_change, write_class_rank_record
from mz_lps3.models import ClassRankRecord

def calc_class_rank(class_objs, type):
    """
    批量计算班级每天排名，步骤如下
    1. 取得每个班级当前成绩排名
    2. 取得每个班级昨天成绩排名, 并反序列化
    3. 计算名字变化
    4. 记录排名进入数据库
    :return:
    """
    if type == '1':
        new_ranks = [CalcClassRank(class_obj).calc_classrank_score() for class_obj in class_objs]   # 计算新成绩排名
    elif type == '2':
        new_ranks = [CalcClassRank(class_obj).calc_classrank_progress() for class_obj in class_objs]   # 计算新进度排名
    class_ids = [class_obj.id for class_obj in class_objs]
    old_ranks = ClassRankRecord.objects.\
                filter(rank_type=type, class_id__in=class_ids).order_by('-rank_date')[:len(class_objs)]
    old_ranks = [dict(class_id=old_rank.class_id,
                      rank_detail=json.loads(old_rank.rank_detail))
                 for old_rank in old_ranks]    # 获取旧排名
    new_ranks = calc_rank_change(new_ranks, old_ranks)  # 计算排名变化
    write_class_rank_record(new_ranks)  # 存入数据库

def calc_class_rank_day():
    """
    计算班级成绩排名
    :return:
    """
    class_objs = Class.objects.xall().filter(lps_version='3.0', is_active=True, status=1, class_type=Class.CLASS_TYPE_NORMAL)
    # class_objs = Class.objects.xall().filter(id=135)
    calc_class_rank(class_objs, type='1')
    calc_class_rank(class_objs, type='2')


def main():
    # 每天上午4点执行
    if datetime.datetime.now().hour == 4:
        calc_class_rank_day()

if __name__ == '__main__':
    calc_class_rank_day()

    # 测试班级消息生成
    # from mz_lps3.functions import ClassDyMsgQueue
    # import datetime, time
    # message = dict(user_id=555,
    #                nick_name='test',
    #                avatar_url='uploads/avatar_url/a.jpg',
    #                message='haha, this is a test',
    #                time=datetime.datetime.now()
    #                )
    # set_class_dynamic_message(135, format_class_dynamic_message(message))

    #测试批量班级消息生成及获取
    # msgs = []
    # for x in range(31):
    #     msgs.append(dict(user_id=x,
    #                      nick_name='test%s' % x,
    #                      avatar_url='uploads/avatar_url/a.jpg',
    #                      message='haha, this is a test',
    #                      time=datetime.datetime.now()))
    #
    # format_msgs = [ClassDyMsgQueue.format_message(msg) for msg in msgs]
    # for msg in format_msgs:
    #     ClassDyMsgQueue.push(135, msg)
    #
    # print ClassDyMsgQueue.get(135)
    #
    # msgs2 = []
    # for x in range(31, 61):
    #     time.sleep(2)
    #     msgs2.append(dict(user_id=x,
    #                      nick_name='test%s' % x,
    #                      avatar_url='uploads/avatar_url/a.jpg',
    #                      message='haha, this is a test',
    #                      time=datetime.datetime.now()))
    # format_msgs = [ClassDyMsgQueue.format_message(msg) for msg in msgs2]
    # for msg in format_msgs:
    #     ClassDyMsgQueue.push(135, msg)
    # print ClassDyMsgQueue.get(135)