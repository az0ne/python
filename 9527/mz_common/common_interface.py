# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render
import db.api.common.city
from utils.logger import logger as log
from utils.excel_tool import ExcelExport
import xlwt
from django.conf import settings
import requests


def get_city_name(request, city_id):
    APIResult = db.api.common.city.get_city_name_by_city_id(city_id)
    if APIResult.is_error():
        log.warn("get city info failed.")
        return render(request, "404.html", {'message': 'get city info failed.'})
    city = APIResult.result()
    return city


def get_api_data(start_date, end_date, action_id):
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    data_url = "%s%s" % (settings.OPERATION_API_HOST, '/action/data/')
    data = {'from': start_date, 'to': end_date, 'action_id': action_id}
    try:
        result = requests.get(url=data_url, params=data, timeout=5)
        json_result = result.json()
    except Exception as e:
        log.warn('get url api failed.'
                 'url:%s.'
                 'error:%s') % (result.url, e)
        json_result = dict()

    return json_result


def excel_export(excel_name, excel_title, excel_data):
    '''
    设置excel的标题和内容，并返回xls格式表格
    :param excel_name: str, the name of excel;
    :param excel_title: tuple, （u'name',u'age',u'address',……）
    :param excel_data: dict, excel 中的数据
    :return:HttpResponse
    '''
    try:
        ex = ExcelExportForLPS()
        for key in excel_data:
            ex.sheet = ex.work_book.add_sheet(key, cell_overwrite_ok=True)
            ex.set_excel(titles=excel_title, values=excel_data.get(key))
        bio = ex.write_bio()
        response = HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % excel_name
        response['Content-Length'] = len(bio.getvalue())

    except Exception as e:
        log.error("excle_export is error.info:%s" % e)
        response = HttpResponse(u"生成excle数据过程中发生了错误。error:%s" % e)
    return response


def normal_excel_export(excel_name, excel_title, excel_data, cols_width=dict()):
    '''
    标准的Excel导出，无任何格式，可通用
    设置excel的标题和内容，并返回xls格式表格
    :param cols_width: 列宽， dict()
    :param excel_name: str, the name of excel;
    :param excel_title: tuple, （u'name',u'age',u'address',……）
    :param excel_data: dict, excel 中的数据，{sheet_name:[[],[].……]}
    :return:HttpResponse
    '''
    try:
        ex = ExcelExportForLPS()
        for key in excel_data:
            ex.sheet = ex.work_book.add_sheet(key, cell_overwrite_ok=True)
            ex.set_col_width(cols_width)
            ex.normal_set_excel(titles=excel_title, values=excel_data.get(key))
        bio = ex.write_bio()
        response = HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % excel_name
        response['Content-Length'] = len(bio.getvalue())

    except Exception as e:
        log.error("excle_export is error.info:%s" % e)
        response = HttpResponse(u"生成excle数据过程中发生了错误。error:%s" % e)
    return response


class ExcelExportForLPS(ExcelExport):
    def __init__(self):
        self.work_book = xlwt.Workbook()

    def set_excel(self, titles, values):
        """
        写入LPS数据，设置有相关格式
        将title，values插入excel
        :param titles: ('行名0', '行名1', '行名2')
        :param values: [
                            ['数据0', '数据1', '数据2'],
                            ['数据0', '数据1', '数据2']
                            ...
                        ]
        :return:
        """
        if not isinstance(titles, (tuple, list)):
            raise ValueError('titles must be tuple or list')
        if not isinstance(values, (tuple, list)):
            raise ValueError('values must be tuple or list')

        for i in range(len(titles)):
            self.sheet.write(0, i, titles[i])
        bold_row = -1
        for y in xrange(len(values)):
            for x in range(len(values[y])):
                if not isinstance(values[y][1], int):
                    bold_row = y
                value = values[y][x]
                value = self._convert_value(value)
                if value is None:
                    self.sheet.write(y + 1, x, '')
                elif y == bold_row:
                    self.sheet.write(y + 1, x, value, self.set_bold())
                else:
                    self.sheet.write(y + 1, x, value)

    def normal_set_excel(self, titles, values):
        """
        通用的写入excel数据，无格式设置
        :param titles: tuple,行名
        :param values: 二维列表，每行的数据
        :return:
        """
        return super(ExcelExportForLPS, self).set_excel(titles=titles, values=values)

    @staticmethod
    def set_bold():
        style = xlwt.XFStyle()
        font = xlwt.Font()  # 为样式创建字体
        font.bold = True
        style.font = font
        return style
