# -*- coding: utf-8 -*-

"""
@version: 2016/3/31
@author: Jackie
@contact: jackie@maiziedu.com
@file: util
@time: 2016/3/31 0:16
@note:  ??
"""

from django.db import connections


def exec_sql(sql, params=None, database="default"):
    cursor = connections[database].cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()