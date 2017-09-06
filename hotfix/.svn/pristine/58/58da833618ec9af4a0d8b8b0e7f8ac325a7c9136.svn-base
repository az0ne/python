# -*- coding: utf-8 -*-
__author__ = 'zhangyunrui'
from tasks import djevn

djevn.load()

from mz_log.models import LogRecords
import os
import re
import datetime


def write_log2db(begin_date, end_date):
    """
    输入起始日期与截止日期,导出这段日期之间log到数据库LogRecords
    :param begin_date: 年月日之间以'-'分隔. eg. '2016-5-10'
    :param end_date: 同begin_date
    :return:
    """
    #todo: 解决乱码及中文不能写入的问题
    # 把字符串转换成datetime
    begin_date_ele = map(lambda x: int(x.lstrip('0')), begin_date.split('-'))
    end_date_ele = map(lambda x: int(x.lstrip('0')), end_date.split('-'))
    begin_datetime = datetime.date(*begin_date_ele)
    end_datetime = datetime.date(*end_date_ele)
    # 算出两个时间的差
    date_delta = end_datetime - begin_datetime
    # 如果结束日期比开始日期小,则把结束日期作为开始日期
    if date_delta.days < 0:
        begin_datetime = end_datetime
        date_delta = abs(date_delta)

    #todo: 探究有没有更方便生产日期list的方法
    for i in range(date_delta.days + 1):
        # 遍历日期list,靠strftime析出不合法日期
        try:
            date_time = begin_datetime + datetime.timedelta(i)
            file_name = date_time.strftime('%Y-%m-%d') + '.log'
        except Exception as e:
            print e

        # 如果LogRecords中file_name字段不等于filename,才写入
        #todo: 如果有记录,删除之
        if not LogRecords.objects.filter(file_name=file_name).exists():
            try:
                # 往上返两个目录层级找到logs文件夹
                logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(''))), 'logs')
                # 组合出日志文件所在目录
                file_path = os.path.join(logs_path, file_name[:7], file_name)
                file_txt = open(file_path).read()
                #todo: 解决读出log总是少一个的情况(研究log源码,从源头取数据,不用正则匹配)
                #todo: 单独读出最后一行的总结性错误信息
                pattern = re.compile(
                    'time: (?P<time>.*?)[\n]Internal Server Error: (?P<error>.*?)[\n].*?[\n](?P<traceback>.*?)[\n]{2}',
                    re.DOTALL)
                exception = pattern.findall(file_txt)

                # 把信息加入querysetlist,批量存储
                querysetlist = []
                for _v in exception:
                    querysetlist.append(
                        LogRecords(file_name=file_name, time=_v[0], internal_server_error=_v[1],
                                   traceback=_v[2].replace(' ', '').replace('\n', ' '))
                    )
                LogRecords.objects.bulk_create(querysetlist)
            except Exception as e:
                print e


if __name__ == '__main__':
    write_log2db('2016-05-19', '2016-05-12')
