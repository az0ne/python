# -*- coding: utf-8 -*-

"""
@version: 2016/3/28
@author: Jackie
@contact: jackie@maiziedu.com
@file: interface.py
@time: 2016/3/28 17:19
@note:  ??
"""

from common.async.decorators import async


def send_sms(mobile, content, ip, tpl):
    """
    发送短消息
    :param mobile:手机号
    :param content: 内容
    :param ip: ip地址
    :param tpl: 模板id
    :return:
    """
    pass


@async
def _async_send_sms():
    pass
