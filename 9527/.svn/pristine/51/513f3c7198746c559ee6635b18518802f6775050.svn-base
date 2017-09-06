# -*- coding:utf-8 -*-
from django.conf import settings
from django.http import Http404
import db.api.lps4.common.student_health
from mz_common.common_interface import normal_excel_export

NORMAL_CLASS_DICT = {2: 411, 9: 412, 13: 413, 135: 414, 5: 415, 4: 416, 137: 417, 128: 418, 3: 419, 14: 420, 134: 421,
                     132: 440, 126: 443}


def get_lps4_student_info_for_health(page_index, keyword):
    APIResult = db.api.lps4.common.student_health.list_lps4_student(page_index=page_index,
                                                                    page_size=settings.PAGE_SIZE,
                                                                    keyword=keyword)
    if APIResult.is_error():
        raise Http404
    result = APIResult.result()
    return result


def export_lps4_student_info_for_health(keyword):
    APIResult = db.api.lps4.common.student_health.export_lps4_student_info(keyword=keyword)
    if APIResult.is_error():
        raise Http404
    result = APIResult.result()
    return result


def get_student_meeting_count_for_health(info):
    APIResult = db.api.lps4.common.student_health.get_lps_students_meeting_count(info)
    if APIResult.is_error():
        raise Http404
    result = APIResult.result()
    return result.get('result').get('num')


def get_student_video_count_for_health(info):
    APIResult = db.api.lps4.common.student_health.get_lps_students_video_count(info)
    if APIResult.is_error():
        raise Http404
    result = APIResult.result()
    return result.get('result').get('num')


def get_student_task_count_for_health(info):
    APIResult = db.api.lps4.common.student_health.get_lps_students_task_count(info)
    if APIResult.is_error():
        raise Http404
    result = APIResult.result()
    return result.get('result').get('num')


def get_upload_homework_reply_count(info):
    APIResult = db.api.lps4.common.student_health.get_teacher_project_coach_reply_count(info)
    if APIResult.is_error():
        raise Http404
    result = APIResult.result()
    return result.get('result').get('num')


def get_student_ask_reply_count(info):
    APIResult = db.api.lps4.common.student_health.get_student_coach_reply_count(info)
    if APIResult.is_error():
        raise Http404
    result = APIResult.result()
    return result.get('result').get('num')


def get_teacher_coach_count(info):
    APIResult = db.api.lps4.common.student_health.get_teacher_coach_count(info)
    if APIResult.is_error():
        raise Http404
    result = APIResult.result()
    return result.get('result').get('num')


def get_teacher_coach_reply_count(info):
    APIResult = db.api.lps4.common.student_health.get_teacher_coach_reply_count(info)
    if APIResult.is_error():
        raise Http404
    result = APIResult.result()
    return result.get('result').get('num')


def update_student_health_info(students, start_time, end_time):
    if students:
        for student in students:
            info = dict(user_id=student.get('user_id'), career_id=student.get('career_id'),
                        teacher_id=student.get('teacher_id'), class_id=NORMAL_CLASS_DICT.get(student.get('career_id')),
                        start_time=start_time, end_time=end_time)
            try:
                meeting_count = get_student_meeting_count_for_health(info)
                video_count = get_student_video_count_for_health(info)
                task_count = get_student_task_count_for_health(info)
                homework_count = get_upload_homework_reply_count(info)
                student_ask_count = get_student_ask_reply_count(info)
                teacher_coach_count = get_teacher_coach_count(info)
                teacher_coach_reply_count = get_teacher_coach_reply_count(info)
                student['meeting_count'] = meeting_count
                student['video_count'] = video_count
                student['task_count'] = task_count
                student['homework_count'] = homework_count
                student['student_ask_count'] = student_ask_count
                student['teacher_coach_count'] = teacher_coach_count
                student['teacher_coach_reply_count'] = teacher_coach_reply_count
                student['sum_make'] = meeting_count * 8 + video_count * 0.5 + task_count * 5 + homework_count * 3 \
                                      + student_ask_count * 3 + teacher_coach_count * 6 + teacher_coach_reply_count * 2
                student['student_name'] = student.get('student_real') if student.get('student_real') else student.get(
                    'student_nick')
                student['teacher_name'] = student.get('teacher_real') if student.get('teacher_real') else student.get(
                    'teacher_nick')
            except Exception as e:
                raise e
    return students


def student_health_excel_export_format(students, start_time, end_time, keyword):
    title_tuple = (u'序号', u'姓名', u'专业', u'就业类型', u'视频观看数', u'完成作业回复数', u'完成任务数', u'约课次数',
                   u'学生问答回复数', u'教师主动发起辅导数', u'教师主动发起辅导回复数', u'分数')
    value_list = []
    if students:
        number = 1
        for student in students:
            values = [number, student.get('student_name'), student.get('career_name'), student.get('student_type_name'),
                      student.get('video_count'), student.get('homework_count'), student.get('task_count'),
                      student.get('meeting_count'), student.get('student_ask_count'),
                      student.get('teacher_coach_count'), student.get('teacher_coach_reply_count'),
                      student.get('sum_make')
                      ]
            value_list.append(values)
            number += 1
    sheet_name = u'学生活跃度数据'
    excel_date = {sheet_name: value_list}
    if keyword:
        keyword = "_%s" % keyword
    excel_name = '学生活跃度数据(%s_%s%s)' % (start_time, end_time, keyword)
    cols_width = dict()
    width = 256 * 15
    for col in xrange(len(title_tuple)):
        cols_width[col] = width
    return normal_excel_export(excel_title=title_tuple, excel_data=excel_date, excel_name=excel_name,
                               cols_width=cols_width)
