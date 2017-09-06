# -*- coding: utf-8 -*-

"""
与tag相关的接口
"""

__author__ = 'changfu'

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


def get_tag(is_hot=False):

    redis_key = 'get_hot_tag' if is_hot else 'get_all_tag'

    @dec_timeit('get_tag')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def _fun(conn, cursor, is_hot_tag=is_hot):  # todo conn无用,是否可以考虑去掉这个参数?
        sql = '''
            SELECT id, name FROM mz_course_tag
            '''
        if is_hot_tag:
            sql = '%s WHERE is_hot_tag = 1' % sql

        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            log.debug('query:%s' % cursor._last_executed)
        except Exception as e:
            log.warn(
                'execute exception: %s. '
                'statement:' % (e, cursor._last_executed))
            raise e

        # todo 跟王琦讨论，将设置缓存一块加入装饰器
        # cache.set("get_homepage_article_types", data)

        return APIResult(result=data)

    return _fun()

@dec_timeit('get_tag_by_id')
@dec_get_cache('get_tag_by_id')
@dec_make_conn_cursor
def get_tag_by_id(conn, cursor, tag_id):
    sql = '''
        SELECT id, name FROM mz_course_tag WHERE id = %s
        '''
    try:
        cursor.execute(sql, (tag_id, ))
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement:' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)
