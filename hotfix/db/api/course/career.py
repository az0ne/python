# -*- coding: utf-8 -*-
from db.api.apiutils import dec_get_cache, APIResult, dec_make_conn_cursor
from db.cores.cache import cache
from utils.logger import logger as log
from utils.tool import dec_timeit


def get_career():
    @dec_timeit("get_career")
    @dec_get_cache("get_career")
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT
                    id,
                    name,
                    short_name,
                    is_default_show
                FROM
                    mz_course_newcareer
                ORDER BY
                    `index`;
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set("get_career", result, 60 * 5)

        return APIResult(result=result)

    return main(_enable_cache=True)


def get_career_name(catagory):
    if not isinstance(catagory, basestring):
        log.warn("catagory is not a string")
        return APIResult(code=True)
    redis_key = 'get_career_name_%s' % catagory

    @dec_timeit('get_career_name')
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
                    mz_course_newcareer
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