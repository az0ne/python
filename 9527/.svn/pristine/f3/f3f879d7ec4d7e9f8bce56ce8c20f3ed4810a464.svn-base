# -*- coding: utf8 -*-

from django import template

register = template.Library()


@register.filter(name='right_or_wrong')
def right_or_wrong(num):
    """
    将0或正整数转换为 前端 勾 叉
    :param num: 0 or 正整数
    :return: html标签
    """
    if num > 0:
        return ('<span class="glyphicon glyphicon-ok" '
                'aria-hidden="true" style="color: red;"></span>')
    else:
        return ('<span class="glyphicon glyphicon-remove" '
                'aria-hidden="true" style="color: red;"></span>')
