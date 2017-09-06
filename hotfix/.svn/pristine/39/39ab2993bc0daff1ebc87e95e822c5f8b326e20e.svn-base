# -*- coding:utf-8 -*-
"""
学生任务超时提醒
"""
import djevn
djevn.load()
import datetime
from mz_lps.models import Class
from mz_lps3.functions import get_student_doing_tasks_timeleft
from mz_common.views import sys_send_message


def main():
    objs = Class.objects.xall().filter(
        lps_version='3.0', class_type=Class.CLASS_TYPE_NORMAL,
        is_active=True, status=1, meeting_enabled=True)
    classes = list()
    for cls in objs:
        meeting_finish = cls.meeting_start + datetime.timedelta(days=(cls.meeting_duration or 1))
        if meeting_finish > datetime.datetime.now():  # 班会未结束
            classes.append(cls)
    for cls in classes:
        assert isinstance(cls, Class)
        for cstudent in cls.classstudents_set.all().filter(is_pause=False):
            if not cstudent.is_active:
                continue
            results = get_student_doing_tasks_timeleft(cls.id, cstudent.user_id)
            for result in results:
                if -3600*25 < result['timeleft'] <= 0:  # task not expired and left time no more than 24h
                    content = '您的职业课程名中的任务%s已经超时，请赶快完成哟~' % result['task_name']
                    sys_send_message(0, cstudent.user_id, 14, content, result['task_id'], cls.career_course_id)

            if cstudent.need_pay():
                content = '你报名的课程%s试学期限已结束，请在5天之内续费哦~' % cls.course_name
                sys_send_message(0, cstudent.user_id, 16, content, cls.id)


# 每天晚8点执行
def main_at():
    if datetime.datetime.now().hour == 20:
        main()

if __name__ == '__main__':
    main()
