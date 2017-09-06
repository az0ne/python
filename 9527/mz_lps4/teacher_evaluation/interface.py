# -*- coding:utf-8 -*-
from django.http import Http404
import db.api.lps4.teacher_evaluation.warning_time
import db.api.lps4.teacher_evaluation.teacher_backlog
from utils.logger import logger as log
import datetime
from mz_common.common_interface import normal_excel_export

DONE_STATUS_DICT = {0: u'未处理', 1: u'事故', 2: u'严重预警', 3: u'预警', 4: u'正常'}


def add_not_done_status(backlog_list):
    if backlog_list:
        now_time = datetime.datetime.now()
        for backlog in backlog_list:
            is_done = backlog.get("is_done", None)
            if is_done == 0:
                warn_one_date = backlog.get("warn_one_date", None)
                warn_two_date = backlog.get("warn_two_date", None)
                warn_three_date = backlog.get("warn_three_date", None)
                type = backlog.get('type')
                if type == 5:
                    warn_three_date = warn_two_date
                if warn_three_date and now_time > warn_three_date:
                    backlog['done_status'] = 1
                elif warn_two_date and now_time > warn_two_date:
                    backlog['done_status'] = 2
                elif warn_one_date and now_time > warn_one_date:
                    backlog['done_status'] = 3
                else:
                    backlog['done_status'] = 4
    return backlog_list


def backlog_excel_export_format(backlog_list):
    title_tuple = (u'事项类型', u'事项内容', u'学员名称', u'老师名称', u'课程名称', u'创建时间', u'预警时间', u'严重预警时间', u'事故时间	', u'状态'
                   , u'是否处理', u'处理时间',)
    value_list = []
    if backlog_list:
        for backlog in backlog_list:
            if backlog.get('type') == 5:
                backlog['type_name'] = u"约课"
                backlog['warn_three_date'] = backlog.get('warn_two_date')
            backlog['teacher_name'] = backlog.get('teacher_real_name') if backlog.get(
                'teacher_real_name') else backlog.get('teacher_nick_name')
            values = [backlog.get('type_name'), backlog.get('content'), backlog.get('user_name'),
                      backlog.get('teacher_name'),
                      backlog.get('career_name'), backlog.get('create_date'), backlog.get('warn_one_date'),
                      backlog.get('warn_two_date'), backlog.get('warn_three_date'),
                      backlog.get('done_status'),
                      backlog.get('is_done_name'), backlog.get('done_date')]
            value_list.append(values)
    sheet_name = u'老师待办事项'
    excel_date = {sheet_name: value_list}
    excel_name = '待办事项'
    cols_width = dict()
    width = 310 * 15
    for col in xrange(len(title_tuple)):
        cols_width[col] = width
    return normal_excel_export(excel_title=title_tuple, excel_data=excel_date, excel_name=excel_name,
                               cols_width=cols_width)

def get_warning_time(_id):
    APIResult = db.api.lps4.teacher_evaluation.warning_time.get_warning_time_by_id(_id=_id)
    if APIResult.is_error():
        log.warn("get warning time by id failed. id=%d" % id)
        raise Http404
    result = APIResult.result()
    return result


def insert_warning_time(warn_dict):
    APIResult = db.api.lps4.teacher_evaluation.warning_time.insert_warning_time(warning_dict=warn_dict)
    if APIResult.is_error():
        log.warn("insert warning time failed.")
        raise Http404
    result = APIResult.result()
    return result


def update_warning_time(warn_dict):
    APIResult = db.api.lps4.teacher_evaluation.warning_time.update_warn_time(warn_dict=warn_dict)
    if APIResult.is_error():
        log.warn("update warning time failed.")
        raise Http404
    result = APIResult.result()
    return result


def delete_warning_time(warning_id):
    APIResult = db.api.lps4.teacher_evaluation.warning_time.delete_warning_time_by_id(warning_id=warning_id)
    if APIResult.is_error():
        log.warn("delete warning time failed.")
        raise Http404
    result = APIResult.result()
    return result
