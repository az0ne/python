# -*- coding: utf8 -*-
from utils.excel_tool import BaseExcelExportTool


class ExportUserCareer(BaseExcelExportTool):

    titles = (u'姓名（昵称）', u'电话号码', u'email', u'职业课程名', u'时间')

    def __init__(self, untreated_values):
        super(ExportUserCareer, self).__init__(self.titles, untreated_values)

    def process(self, user_career_list):
        rows = list()

        for uc in user_career_list:
            detail_list = [
                uc['nick_name'], uc['mobile'], uc['email'],
                uc['career_name'], uc['create_date']
            ]
            rows.append(detail_list)

        return rows
