# -*- coding: utf-8 -*-
from db.api.apiutils import dec_get_cache, APIResult, dec_make_conn_cursor
from db.cores.cache import cache
from utils.logger import logger as log
from utils.tool import dec_timeit


def get_catagory():
    @dec_timeit("get_catagory")
    @dec_get_cache("get_catagory")
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT
                    id,
                    name,
                    short_name
                FROM
                    mz_course_newcareercatagory;
            """
            cursor.execute(sql)
            catagory = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set("get_catagory", catagory, 60 * 5)

        return APIResult(result=catagory)

    return main(_enable_cache=True)


def get_catagory_name(catagory):
    if not isinstance(catagory, basestring):
        log.warn("catagory is not a string")
        return APIResult(code=True)
    redis_key = 'get_catagory_name_%s' % catagory

    @dec_timeit('get_catagory_name')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT
                    name
                FROM
                    mz_course_newcareercatagory
                WHERE
                    short_name = %s;
            """
            cursor.execute(sql, catagory)
            catagory_tag = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set('get_tag_name', catagory_tag, 60 * 5)

        return APIResult(result=catagory_tag)

    return main(_enable_cache=True)
