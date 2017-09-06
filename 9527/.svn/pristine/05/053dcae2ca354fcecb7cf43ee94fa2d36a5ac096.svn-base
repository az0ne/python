# -*- coding: utf8 -*-

import db.api
from utils.tool import convert_01
from utils.excel_tool import BaseExcelExportTool
from utils.logger import logger as log


# 获取学生试学详情
def get_try_learn_detail(class_id, student_id):
    # 是否参加会议
    in_meeting = db.api.is_in_meeting(class_id, student_id)
    if in_meeting.is_error():
        log.warn('get is in meeting failed. '
                 'class_id: {}, student_id: {}'.format(class_id, student_id))
    in_first_meeting = in_meeting.result().get('in_first_meeting', 0)
    in_qa_meeting = in_meeting.result().get('in_QA_meeting', 0)

    # 是否提交作业
    is_submit_task = db.api.is_submit_task(class_id, student_id)
    if is_submit_task.is_error():
        log.warn('get is submit task failed. '
                 'class_id: {}, student_id: {}'.format(class_id, student_id))
    is_submit_task = is_submit_task.result().get('is_submit_task', 0)

    # 是否提交满意度调查表
    is_submit_questionnaire = db.api.is_submit_questionnaire(class_id, student_id)
    if is_submit_questionnaire.is_error():
        log.warn('get is submit questionnaire failed. '
                 'class_id: {}, student_id: {}'.format(class_id, student_id))
    is_submit_questionnaire = is_submit_questionnaire.result().get(
        'is_submit_questionnaire', 0)

    if is_submit_questionnaire:
        # 提交满意度调查表详情
        questionnaire_records = db.api.get_questionnaire_records(class_id, student_id)
        if questionnaire_records.is_error():
            log.warn('get questionnaire records failed. '
                     'class_id: {}, student_id: {}'.format(class_id, student_id))
            questionnaire_records = []
        questionnaire_records = questionnaire_records.result()
    else:
        questionnaire_records = []

    return dict(in_first_meeting=in_first_meeting,
                in_QA_meeting=in_qa_meeting,
                is_submit_task=is_submit_task,
                is_submit_questionnaire=is_submit_questionnaire,
                questionnaire_records=questionnaire_records)


class ExportTryLearnData(BaseExcelExportTool):

    titles = (
        u'ID', u'姓名（昵称）', u'手机', u'麦子账号', u'试学课程',
        u'试学班老师', u'试学时间', u'加班时间', u'首次班会开始时间',
        u'答疑班会开始时间', u'是否参加首次班会', u'是否参加答疑班会',
        u'是否提交作业', u'是否提交满意度调查表', u'题干', u'学生选择')

    def __init__(self, untreated_values):
        super(ExportTryLearnData, self).__init__(self.titles, untreated_values)

    def process(self, try_learn_list):
        rows = list()

        for learn in try_learn_list:
            detail_list = (
                [learn['id'], learn['nick_name'], learn['mobile'],
                 learn['username'], learn['try_learn_name'],
                 learn['teacher_name'], learn['try_learn_time'],
                 learn['join_class_date'], learn['first_startline'],
                 learn['QA_startline']]
            )

            other = get_try_learn_detail(learn['class_id'], learn['id'])
            detail_list.extend(
                [convert_01(other['in_first_meeting']), convert_01(other['in_QA_meeting']),
                 convert_01(other['is_submit_task']), convert_01(other['is_submit_questionnaire'])]
            )

            for qd in other['questionnaire_records']:
                detail_list.extend([qd['stem'], qd['record']])

            rows.append(detail_list)

        return rows
