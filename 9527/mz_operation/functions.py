# -*- coding: utf8 -*-

from datetime import datetime
import requests
from utils import tool
from utils.excel_tool import ExcelImport
from django.conf import settings


def get_7_days_ago():
    return tool.other_day(7).strftime('%Y-%m-%d')


def get_a_day_later():
    return tool.other_day(-1).strftime('%Y-%m-%d')


def get_now():
    return datetime.now().strftime('%Y-%m-%d')


def shortcut_date(shortcut):
    if shortcut == 'same_day':
        start_date = datetime.now().strftime('%Y-%m-%d')
    elif shortcut == 'this_week':
        start_date = tool.get_week_1().strftime('%Y-%m-%d')
    elif shortcut == 'this_month':
        start_date = tool.get_month_1().strftime('%Y-%m-%d')
    elif shortcut == '7day_ago':
        start_date = tool.other_day(6).strftime('%Y-%m-%d')
    elif shortcut == '30day_ago':
        start_date = tool.other_day(29).strftime('%Y-%m-%d')
    else:
        start_date = datetime.now().strftime('%Y-%m-%d')

    end_date = tool.other_day(-1).strftime('%Y-%m-%d')

    return start_date, end_date


recommend_data = {
    u'转介绍': True,
    u'非转介绍': False
}
patron_data = {
    u'首次购买': True,
    u'重复购买': False
}


def build_volume_info(file_data):
    """
    构造销售数据
    :param file_data: excel数据(io流)
    :return:
    """
    ei = ExcelImport(file_data)
    data = ei.get_values(5)

    json_data = list()

    for i in range(len(data)):
        line = data[i]
        row = i + 2  # 从excel第二行开始读数据
        mobile = ei.verify_telephone(line[0], row)
        date = tool.fill_datetime(ei.xldate_as_datetime(line[1], row))
        price = ei.verify_value_is_num(line[2], row, u'价钱必须为数字！')
        recommend = recommend_data.get(line[3], False)
        patron = patron_data.get(line[4], False)

        json_data.append(dict(
            day=date.strftime('%Y-%m-%d'),
            mobile=mobile,
            datetime=date,
            price=price,
            recommended=recommend,
            patron=patron
        ))

    return json_data


def build_customer_info(file_data):
    """
    构造客户数据
    :param file_data: excel数据(io流)
    :return:
    """
    ei = ExcelImport(file_data, 2)

    data = dict()
    sheet2 = ei.get_values(1, 1)
    count = sheet2[0][0]
    data.update(count=count)

    sheet1 = ei.get_values(3, 0)
    json_data = list()

    for i in range(len(sheet1)):
        line = sheet1[i]
        row = i + 2  # 从excel第二行开始读数据
        mobile = ei.check_telephone(line[0], row)
        date = ei.xldate_as_datetime(line[1], row)
        ip = line[2] if line[2] == '' else ei.verify_ip(line[2], row)

        json_data.append(dict(
            day=date.strftime('%Y-%m-%d'),
            mobile=mobile,
            datetime=date,
            ip=ip
        ))
    data.update(result=json_data)

    return data


def build_sem_info(file_data):
    """
    构造sem数据
    :param file_data: excel数据(io流)
    :return:
    """
    ei = ExcelImport(file_data)
    data = ei.get_values(5)

    json_data = list()

    for i in range(len(data)):
        line = data[i]
        row = i + 2  # 从excel第二行开始读数据
        date = tool.fill_datetime(ei.xldate_as_datetime(line[0], row))
        channel = line[1]
        display = ei.verify_value_is_num(line[2], row, u'查看次数必须为数字！')
        click = ei.verify_value_is_num(line[3], row, u'点击次数必须为数字！')
        money = ei.verify_value_is_float(line[4], row, u'投入金额必须为数字！')

        json_data.append(dict(
            day=date.strftime('%Y-%m-%d'),
            datetime=date,
            channel_name=channel,
            display=display,
            click=click,
            money=money
        ))

    return json_data


def get_new_students_list(page_index):
    url = settings.OPERATION_NEW_STUDENT_API_HOST + '/new_students/'
    para = dict(page_index=page_index)
    data = requests.get(url=url, params=para, timeout=5).json()
    student_info = dict()
    if data and data.get('code') == 200:
        result = data.get('result', dict())
        if result:
            page = dict(page_index=result.get('page_index', 1), page_size=result.get('page_size', 10),
                        rows_count=result.get('rows_count'), page_count=result.get('page_count'))
            student_info = dict(student_info=result.get('data'), page=page)
    return student_info


def get_student_info(student_id, career_id):
    url = settings.OPERATION_NEW_STUDENT_API_HOST + '/one_student/'
    para = dict(student_id=student_id, career_id=career_id)
    data = requests.get(url=url, params=para, timeout=5).json()
    student = dict()
    if data and data.get('code') == 200:
        student = data.get('result', dict())
    return student
