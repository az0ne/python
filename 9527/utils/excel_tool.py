# -*- coding: utf8 -*-
import string
from datetime import datetime

import xlrd
import xlwt
from io import BytesIO

from utils.tool import is_phone_or_telephone, ip_check


class ExcelExport(object):
    """
    excel导出
    """

    def __init__(self):
        self.work_book = xlwt.Workbook()
        self.sheet = self.work_book.add_sheet('sheet1', cell_overwrite_ok=True)

    def set_col_width(self, table_widths):
        """
        :param table_widths: {列号: 列宽, 列号: 列宽, ...}
        :return:
        """
        if not isinstance(table_widths, dict):
            raise ValueError('table_widths must be dict')
        for k, v in table_widths.items():
            self.sheet.col(k).width = v

    def set_excel(self, titles, values):
        """
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

        for y in xrange(len(values)):
            for x in range(len(values[y])):
                value = values[y][x]
                value = self._convert_value(value)

                if value is None:
                    self.sheet.write(y + 1, x, '')
                else:
                    self.sheet.write(y + 1, x, value)

    @staticmethod
    def _convert_value(val):
        if isinstance(val, datetime):
            return val.strftime('%Y-%m-%d %H:%M:%S')
        return val

    def write_bio(self):
        bio = BytesIO()
        self.work_book.save(bio)
        return bio


class BaseExcelExportTool(object):

    def __init__(self, titles, untreated_values):
        self.et = ExcelExport()

        if not isinstance(titles, (list, tuple)):
            raise TypeError('titles must be list or tuple')

        if not isinstance(untreated_values, (list, tuple)):
            raise TypeError('untreated_values must be list or tuple')

        self.titles = titles
        self.untreated_values = untreated_values

    def process(self, untreated_values):
        """
        用来处理untreated_values，必须根据自己的数据需求重写
        :param untreated_values: 未处理的数据
        :return: 处理过的数据
                values: [
                            ['数据0', '数据1', '数据2'],
                            ['数据0', '数据1', '数据2']
                            ...
                        ]
        """
        raise NotImplementedError()

    def export_bio(self):
        """
        导出到io流
        :return:
        """
        self.et.set_excel(
            self.titles, self.process(self.untreated_values))

        return self.et.write_bio()  # 返回一个BytesIO流


class ExcelImport(object):
    """
    excel导入
    """

    def __init__(self, file_data, sheets_count=1):
        self.file_data = file_data
        try:
            self.excel = xlrd.open_workbook(file_contents=self.file_data)
        except AssertionError:
            raise ExcelDataError(0, message=u'可能由Excel版本问题引起！请下载系统\
                                             提供的Excel模板！并严格按照格式填写数据！')
        if len(self.excel.sheets()) < sheets_count:
            raise ExcelDataError(0, message=u'Excel中不能少于{0}个工作表！'.format(sheets_count))
        self.sheet_name = self.excel.sheet_names()[0]
        self.row = 2    # 记录当前读取到第几行

    def set_sheet(self, sheet):
        self.sheet_name = self.excel.sheet_names()[sheet]

    def set_row(self, sheet):
        self.sheet_name = self.excel.sheet_names()[sheet]

    def get_values(self, verify_col, sheets=0):
        """
        获取数据
        :param sheets: 第几个工作表
        :param verify_col: 提供当前模板的列数，以此初步验证模板是否为系统提供
        :return:
        """

        result = []
        sheet = self.excel.sheets()[sheets]

        if sheet.nrows == 0 or len(sheet.row_values(0)) != verify_col:
            raise ExcelDataError(0, message=u'请下载系统提供的Excel模板！')

        self.sheet_name = self.excel.sheet_names()[sheets]

        for row_num in range(sheet.nrows - 1):
            line = self._strips(sheet.row_values(row_num + 1))
            if line:
                result.append(self._strips(sheet.row_values(row_num + 1)))

        if len(result) == 0:
            raise ExcelDataError(0, message=u'Excel数据为空！', sheet_name=self.sheet_name)
        return result

    @staticmethod
    def _strips(values):
        """
        剔除空行
        :param values:
        :return:
        """
        for i, value in enumerate(values):
            if isinstance(value, (str, unicode)):
                values[i] = value.strip()
        if [v for v in values if v]:
            return values
        return None

    def xldate_as_datetime(self, value, row, err_msg=u'请检查时间格式！'):
        try:
            time = xlrd.xldate.xldate_as_datetime(value, False)
            return time
        except Exception as e:
            raise ExcelDataError(row, message=err_msg, sheet_name=self.sheet_name)

    def verify_telephone(self, phone, row):
        telephone = self.verify_value_is_num(phone, row, u'电话号码只能是数字组成！')
        if not is_phone_or_telephone(telephone):
            raise ExcelDataError(row, message=u'请检查电话号码格式以及长度！', sheet_name=self.sheet_name)
        return telephone

    def verify_value_is_num(self, value, row, err_msg, convert=True):
        try:
            if isinstance(value, float):
                result = str(int(value)) if convert else value
            else:
                if isinstance(value, (str, unicode)):
                    float(value) if '.' in value else int(value)
                result = str(value) if convert else value
        except Exception:
            raise ExcelDataError(row, message=err_msg, sheet_name=self.sheet_name)
        return result

    @staticmethod
    def verify_value_is_empty(value, row, err_msg):
        if not value:
            raise ExcelDataError(row, message=err_msg)

    @staticmethod
    def verify_values_is_empty(values, row):
        if not values:
            raise ExcelDataError(row, message=u'Excel每列都为必填项，请完善Excel重新上传！')
        for value in values:
            if not value:
                raise ExcelDataError(row, message=u'Excel每列都为必填项，请完善Excel重新上传！')

    def verify_value_is_float(self, value, row, err_msg, precise=True):
        if not isinstance(value, float):
            try:
                value = float(value)
            except Exception:
                raise ExcelDataError(row, message=err_msg, sheet_name=self.sheet_name)
        return round(value, 3) if precise else value

    def check_telephone(self, phone, row):
        digits = string.digits.decode('ascii')

        if isinstance(phone, (str, unicode)):
            flag_i = None
            for i in range(len(phone)):
                if phone[i] in digits:
                    flag_i = i
                    break
            if flag_i is None:
                raise ExcelDataError(row, message=u'请确认输入了手机号。', sheet_name=self.sheet_name)
            return self.verify_telephone(phone[flag_i:], row)
        else:
            return self.verify_telephone(phone, row)

    def verify_ip(self, ip, row):
        if '(' in ip:
            ip = ip.split('(')[-1].replace(')', '')
        if ip_check(ip):
            return ip
        raise ExcelDataError(row, message=u'ip格式有误。', sheet_name=self.sheet_name)


class ExcelDataError(Exception):
    """
    上传Excel数据异常
    """

    def __init__(self, row, message=None, sheet_name=None):
        super(Exception, self).__init__()
        self.row = u' 行号：{0}。'.format(row) if row != 0 else ''
        self.sheet_name = u' 工作表：{0}。'.format(sheet_name) if sheet_name else ''
        if message:
            self.message = message
        else:
            self.message = u'请检查Excel文件！'

    def __str__(self, *args, **kwargs):
        return u'Excel数据有误, 信息：{msg}{sheet}{row}'\
            .format(msg=self.message, sheet=self.sheet_name, row=self.row)
