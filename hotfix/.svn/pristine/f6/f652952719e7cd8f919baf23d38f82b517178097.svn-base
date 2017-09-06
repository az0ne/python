# -*- coding: utf-8 -*-
"""
@version: 2016/6/6 0006
@author: lewis
@contact: lewis@maiziedu.com
@file: employ_teacher.py
@time: 2016/6/6 0006 16:55
@note:  ??
"""
from utils.logger import logger as log
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_make_conn_cursor
def insert_employ_teacher(conn, cursor, data_dict):
    """
    插入讲师招聘数据
    :param conn:
    :param cursor:
    :param data_dict:插入招聘讲师录入的数据
    :return:
    """
    sql = """
             INSERT INTO mz_employ_teacher(
             teacher_type,
             teacher_catagory,
             name,
             career,
             work_time,
             resume,
             mobile,
             qq,
             create_time,
             is_send_email)VALUES
             (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    import datetime

    insert_list = list()
    insert_list.append(data_dict.get('teacher_type', 'Null'))
    insert_list.append(data_dict.get('teacher_catagory', 'Null'))
    insert_list.append(data_dict.get('name', 'Null'))
    insert_list.append(data_dict.get('career', 'Null'))
    insert_list.append(data_dict.get('work_time', 'Null'))
    insert_list.append(data_dict.get('resume', 'Null'))
    insert_list.append(data_dict.get('mobile', 'Null'))
    insert_list.append(data_dict.get('qq', 'Null'))
    insert_list.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    insert_list.append(0)
    try:
        cursor.execute(sql, insert_list)
        conn.commit()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(code=True)
