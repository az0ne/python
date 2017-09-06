# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='second2duration')
def second2duration(second):
    """
    @brief 模板过滤器：秒数到时长的转换，例：492 ——> '08:12'

    @param second : 多少秒
    @retval : 返回'08:12'格式的时长
    """
    return '{:0>2}:{:0>2}'.format(second / 60, second % 60)
