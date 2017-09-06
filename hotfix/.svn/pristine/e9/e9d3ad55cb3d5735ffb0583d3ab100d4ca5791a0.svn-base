# -*- coding: utf-8 -*-

__author__ = 'Jackie'

import datetime

now = datetime.datetime.now()

import time

print long(time.mktime(now.timetuple()) * 1000 + now.microsecond / 1000)
print long(time.time() * 1000)
print now.timetuple()

import requests

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0",
           "Referer": "http://www.maiziedu.com/"
           }


def test():
    s = requests.session()
    form_data = {'account_l': 'nj1987@163.com', 'password_l': '123456789'}

    resp = s.post('http://127.0.0.1:8000/user/login/', data=form_data, headers=headers)
    print resp.status_code


def test2():
    tmp = [u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日']
    now = datetime.datetime.now()
    date = now.date()
    print date.weekday()
    print date.isoformat(), now.time().strftime('%H:%M')


def pretty_format(dt):
    tmp = (u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日')
    date = dt.date()
    return u"%s %s %s" % (date.isoformat(), tmp[date.weekday()], dt.time().strftime('%H:%M'))


def cal_age(birthday, today):
    assert isinstance(today, datetime.date)
    assert isinstance(birthday, datetime.date)
    age = today.year - birthday.year
    if today.isoformat()[-5:] < birthday.isoformat()[-5:]:
        age -= 1
    return age


print pretty_format(datetime.datetime.now())
