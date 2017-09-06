# -*- coding:utf-8 -*-
from django.http import Http404
import db.api.coach.coach_api
from utils.logger import logger as log
from mz_common.common_interface import normal_excel_export
from mz_lps4.teacher_evaluation.interface import DONE_STATUS_DICT


def get_coach_status_by_id(coach_id):
    APIResult = db.api.coach.coach_api.get_coach_status_by_id(coach_id)
    if APIResult.is_error():
        log.warn("get done_status from mz_lps4_teacher_warning_backlog by coach_id failed.")
        raise Http404
    status = APIResult.result()
    get_status = DONE_STATUS_DICT.get(0)  # 获取默认完成状态
    if status:
        status_list = []
        for sta in status:
            done_status = sta.get('done_status', None)
            if done_status:
                status_list.append(done_status)
        if status_list:
            get_status = DONE_STATUS_DICT.get(min(status_list))
    else:  # Don't have backlog
        get_status = DONE_STATUS_DICT.get(4)
    return get_status


def coach_excel_export_format(coach_list):
    title_tuple = (u'辅导类型', u'职业课程', u'发贴人', u'学生姓名', u'老师姓名', u'帖子摘要', u'创建时间', u'学生回复数', u'老师回复数', u'最后回复时间'
                   , u'老师最后回复时间', u'学生最后回复时间', u'老师未读回复数', u'学生未读回复数', u'完成状态',)
    value_list = []
    if coach_list:
        for coach in coach_list:
            values = [coach.get('source_type_name'), coach.get('career_name'), coach.get('nick_name'),
                      coach.get('student_name'),
                      coach.get('teacher_name'), coach.get('abstract'), coach.get('create_date'),
                      coach.get('student_comment_count'), coach.get('teacher_comment_count'),
                      coach.get('last_comment_date'),
                      coach.get('last_teacher_comment_date'), coach.get('last_student_comment_date'),
                      coach.get('teacher_replay_count'),
                      coach.get('student_replay_count'), coach.get('done_status')]
            value_list.append(values)
    sheet_name = u'辅导信息'
    excel_date = {sheet_name: value_list}
    excel_name = '辅导信息'
    cols_width = dict()
    width = 256 * 15
    for col in xrange(len(title_tuple)):
        cols_width[col] = width
    return normal_excel_export(excel_title=title_tuple, excel_data=excel_date, excel_name=excel_name,
                               cols_width=cols_width)
