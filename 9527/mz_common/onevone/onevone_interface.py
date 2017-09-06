# -*-coding:utf8-*-
from utils.excel_tool import ExcelExport
import db.api.common.onevone.onevone_ops
from django.conf import settings
from utils.logger import logger as log
from django.shortcuts import render
from mz_common.common_interface import get_city_name


def draw_onevone_ops_data(ops_list):
    '''
    填充onevone ops 的数据
    :param ops_list:
    :return:
    '''
    data = list()
    if ops_list:
        for ops in ops_list:
            row = [ops.get('id'), ops.get('real_name'), ops.get('name'), ops.get('type_name'), ops.get('nick_name'),
                   ops.get('username'),
                   ops.get('mobile'), ops.get('ops_mobile'),
                   ops.get('qq'), ops.get('city_name'), ops.get('source_name'),
                   ops.get('datetime').strftime("%Y-%m-%d %H:%M:%S"), ops.get('time_interval_name'),
                   ops.get('is_done_name')]

            data.append(row)
    return data


def excle_export(ops_list):
    '''
    设置excel的标题和内容，并保存为字节流的方式
    :param ops_list:
    :return:
    '''
    ex = ExcelExport()
    title = (
        u'ID', u'真实姓名', u'意向专业', u'工作情况', u'昵称', u'账户名', u'账户电话', u'预约电话', u'QQ', u'所在城市', u'数据来源', u'预约时间', u'预约时段',
        u'是否处理')
    ex.set_excel(titles=title, values=draw_onevone_ops_data(ops_list))
    return ex.write_bio()


def get_onevone_data(request, data_type, page_index):
    if data_type == '1':  # 当前页数据
        APIResult = db.api.common.onevone.onevone_ops.list_onevone_ops(page_index=page_index,
                                                                       page_size=settings.PAGE_SIZE)
    elif data_type == '2':  # 所有数据
        APIResult = db.api.common.onevone.onevone_ops.get_all_onevone_ops()

    if APIResult.is_error():
        log.warn("list onevone ops failed.")
        return render(request, "404.html", {"message": "list onevone ops failed."})
    result = APIResult.result()
    # # 获取城市信息
    ops_result = result.get('result', None) if data_type == '1' else result
    for res in ops_result:
        city = get_city_name(request, res.get('city_id', 0))
        if city:
            res["city_name"] = "%s-%s" % (city.get('province_name'), city.get('city_name'))
        else:
            res["city_name"] = None
    return ops_result


def change_onevone_ops_is_done(request, ops_id):
    if ops_id:
        APIResult = db.api.common.onevone.onevone_ops.change_ops_is_done(ops_id)
        if APIResult.is_error():
            log.warn("change onevone ops is_done failed.")
            return render(request, "404.html", {"message": "change onevone ops is_done failed."})


def change_onevone_ops_is_done_to_1(request, ops_id):
    if ops_id:
        APIResult = db.api.common.onevone.onevone_ops.change_ops_is_done_to_1(ops_id)
        if APIResult.is_error():
            log.warn("change onevone ops is_done to true failed.")
            return render(request, "404.html", {"message": "change onevone ops is_done to true failed."})
