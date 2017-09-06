#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six

from HTMLParser import HTMLParser
from datetime import datetime


def html_content_brief(content, length=120):
    """
    @brief 对带html标签的内容提取摘要

    @param content : 内容
    @param length : 摘要默认长度
    @retval : 返回长度最多为120个字符
    """
    html = content.strip()
    result = []
    parse = HTMLParser()
    parse.handle_data = result.append
    parse.feed(html)
    parse.close()
    result = list(filter(lambda x: x[:1] != '\n', result))
    result = ''.join(result)
    return result[:length]+'...' if len(result) > length else result


def second2duration(second):
    """
    @brief 秒数到时长的转换，例：492 ——> '08:12'

    @param second : 多少秒
    @retval : 返回'08:12'格式的时长
    """
    return '{:0>2}:{:0>2}'.format(second / 60, second % 60)


def datetime_convert(times):
    """
    @brief 计算时间过去了多久

    @param times : 时间，支持字符串格式、datetime.datetime类型
    @retval : xx前
    """
    if isinstance(times, six.string_types):
        try:
            times = datetime.strptime(times, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return ''
    tt = datetime.now() - times
    if int(tt.days / 365 > 0):
        return str(int(tt.days / 365)) + '年前'
    elif int(tt.days / 30) > 0:
        return str(int(tt.days / 30)) + '个月前'
    elif int(tt.total_seconds() / 60 / 60 / 24) > 0:
        return str(int(tt.total_seconds() / 60 / 60 / 24)) + '天前'
    elif int(tt.total_seconds() / 60 / 60) > 0:
        return str(int(tt.total_seconds() / 60 / 60)) + '小时前'
    elif int(tt.total_seconds() / 60) > 0:
        return str(int(tt.total_seconds() / 60)) + '分钟前'
    elif int(tt.total_seconds()) < 60:
        return '刚刚'
