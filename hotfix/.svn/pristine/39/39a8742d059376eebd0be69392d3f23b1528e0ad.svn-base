# -*- coding: utf-8 -*-

"""
@version: 2016/3/28
@author: Jackie
@contact: jackie@maiziedu.com
@file: validators.py
@time: 2016/3/28 11:51
@note:  一些常用的校验方法
"""

import re


class VerifyError(Exception):
    pass


def v_len(s, min_l, max_l, name=''):
    if min_l <= len(s) <= max_l:
        return
    raise VerifyError, u"%s长度超过范围(%s,%s)" % (name, min_l, max_l)


def v_email(value, min_len=3, max_len=50):
    re_str = ur"^[-_A-Za-z0-9\.]+@([_A-Za-z0-9]+\.)+[A-Za-z0-9]{2,32}$"
    v_len(value, min_len, max_len)
    if not re.match(re_str, value):
        raise VerifyError, u"邮箱格式不正确"


def v_mobile(value):
    re_str = ur"^1[3578]\d{9}$|^14[57]\d{8}$"
    if not re.match(re_str, value):
        raise VerifyError, u"手机号码格式错误!"


def v_nick(value, min_len=2, max_len=12, check_ban=True):
    """
    :attention: 验证昵称
    """
    if check_ban:
        ban_keywords = (u'测试', u'test', u'教师', u'教务', u'老师')
        for key in ban_keywords:
            if key in value:
                raise VerifyError, u"昵称不能含有关键字 %s ！" % key

    re_str = u'^[\w\-\_\u4e00-\u9fa5]{%s,%s}$' % (min_len, max_len)
    if not re.match(re_str, value):
        raise VerifyError, u"昵称只能是%s~%s位中文、字母、数字、下划线或减号！" % (min_len, max_len)


def v_password(value):
    '''
    :note: 判断是否是弱密码
    '''
    weak_password = (
        '000000', '111111', '11111111', '112233', '123123', '123321', '123456', '12345678',
        '654321', '666666', '888888', 'abcdef', 'abcabc', 'abc123', 'a1b2c3',
        'aaa111', '123qwe', 'qwerty', 'qweasd', 'password',
        'p@ssword', 'passwd', 'iloveyou', '5201314',)
    if value in weak_password:
        raise VerifyError, u"你的密码太过简单！请重新设置"
    use_char = set(list(value))
    if len(use_char) > 2:
        return
    raise VerifyError, u"你的密码太过简单！请重新设置"
