# -*- coding: utf-8 -*-

__author__ = 'lewis'
import os
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django

django.setup()
# from django.conf import settings
from django.db import connections
from collections import OrderedDict

def exec_sql(sql, params=None, database="default"):
    cursor = connections[database].cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()

#当前直播日期
class LivingSchedule(object):

    def __init__(self,edu_admin_id,start_date,end_date):
        self.edu_admin_id = edu_admin_id
        self.start_date = start_date + ' 00:00'
        self.end_date = end_date+ ' 23:59'

    def get_living_data(self):
        living_info=self._get_living_info(self.edu_admin_id, self.start_date, self.end_date)
        #对数据进行整理统计
        living_data = OrderedDict()
        for week in xrange(0,7):
            data_lst=living_info.get(week,[])
            times = len(data_lst)
            numbers = sum([data['current_student_count'] for data in data_lst])
            data_lst.sort(key=lambda x:x['create_datetime'])
            living_data[get_week_value(week)] = dict(times=times, numbers=numbers, data_lst=data_lst)
        if living_info == {}:
            is_data = False
        else:
            is_data = True
        return living_data,is_data

    def _get_living_info(self,edu_admin_id,start_date,end_date):
        """
        @:param edu_admin_id 教务老师ID
        @:param start_date  周开始时间
        @:param end_date  周结束时间
        """
        if edu_admin_id == 0:
            #查询全部教务
            edu_admin_sql = """
            edu_admin.id in
            (SELECT
                mz_user_userprofile.id
            FROM
                mz_user_userprofile
            INNER JOIN mz_user_userprofile_groups ON mz_user_userprofile_groups.userprofile_id = mz_user_userprofile.id
            INNER JOIN auth_group ON mz_user_userprofile_groups.group_id = auth_group.id
            WHERE
                auth_group.`name` = '教务')
            """
        else:
            edu_admin_sql = "edu_admin.id = %s" % edu_admin_id

        sql = """
        SELECT
            classmeeting.id AS class_meeting_id,
            class.id AS class_id,
            classmeeting.startline AS startline,
            classmeeting.startline AS create_datetime,
            class.current_student_count AS current_student_count,
            classmeeting.content AS content,
            class.coding AS coding,
            teacher.nick_name AS teacher_nick_name,
            edu_admin.nick_name AS edu_admin_nick_name,
            teacher.real_name AS teacher_real_name,
            edu_admin.real_name AS edu_admin_real_name,
            classmeeting.status AS status,
            liveroom.teacher_join_url AS join_url,
            liveroom.assistant_token AS token
        FROM
          mz_lps3_classmeeting as classmeeting
        INNER JOIN mz_lps3_classmeetingrelation ON mz_lps3_classmeetingrelation.class_meeting_id = classmeeting.id
        INNER JOIN mz_lps_class as class ON mz_lps3_classmeetingrelation.class_id=class.id
        INNER JOIN mz_user_userprofile as teacher ON classmeeting.create_id = teacher.id
        INNER JOIN mz_user_userprofile as edu_admin ON class.edu_admin_id = edu_admin.id
        INNER JOIN mz_lps3_liveroom as liveroom ON liveroom.class_meeting_id = classmeeting.id
        WHERE
           %s
        AND '%s' <= classmeeting.startline
        AND classmeeting.startline <= '%s'
        AND class.is_active = True
        AND class.lps_version = '3.0'
        AND class.class_type = 0
        """ % (edu_admin_sql,start_date,end_date)
        result = dict()
        for class_meeting_id,class_id,startline,create_datetime,current_student_count,content,coding,\
            teacher_nick_name,edu_admin_nick_name,teacher_real_name,edu_admin_real_name,status,join_url,token  in exec_sql(sql):
            week=startline.weekday()
            data=dict(
                class_meeting_id=class_meeting_id,
                class_id=class_id,
                startline=startline,
                create_datetime=create_datetime,
                current_student_count=current_student_count,
                content=content,
                coding=coding,
                teacher_name=teacher_real_name or teacher_nick_name,
                edu_admin_name=edu_admin_real_name or edu_admin_nick_name,
                status=status,
                join_url=join_url,
                token=token
            )
            if result.has_key(week):
                result[week].append(data)
            else:
                result[week] = [data]
        return result

def get_week_time(step=0):
    #时间范围计算
    now_datetime = datetime.datetime.now()
    real_datetime = now_datetime+datetime.timedelta(days=step*7)
    week = real_datetime.weekday()
    day_diff = -1 * week
    day_add = 6 - week
    start_date = (real_datetime+datetime.timedelta(days=day_diff)).strftime('%Y-%m-%d')
    end_date = (real_datetime+datetime.timedelta(days=day_add)).strftime('%Y-%m-%d')
    step_prev=step-1
    step_next=step+1
    return start_date,end_date,step_prev,step_next

def get_week_value(week):
    week_dict = {0:'星期一',
                 1:'星期二',
                 2:'星期三',
                 3:'星期四',
                 4:'星期五',
                 5:'星期六',
                 6:'星期日',}

    return week_dict.get(week,'')

if __name__ == "__main__":
    # living = LivingSchedule(20276,'2016-02-21','2016-03-23')
    print datetime.datetime.now().weekday()