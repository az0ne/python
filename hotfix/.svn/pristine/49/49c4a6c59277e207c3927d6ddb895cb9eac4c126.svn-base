#!/usr/bin/env python
# -*- coding: utf8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_get_cache("get_career_course_links")
@dec_make_conn_cursor
def get_career_course_links(conn, cursor, career_id, link_type=''):
    """
    @brief 获取老的职业课程大纲页的友情链接 /course/ios/
    :param conn:
    :param cursor:
    :return:
    """
    map = dict(FRIEND=' AND type = "FRIEND" ',
               RELATION=' AND type = "RELATION" ')
    sql = '''SELECT title, url FROM mz_career2_link AS l WHERE career_id = %s'''
    sql = '%s%s%s' % (sql, map.get(link_type.upper(), ' '), 'ORDER BY l.index')
    try:
        cursor.execute(sql, (career_id, ))
        data = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)
