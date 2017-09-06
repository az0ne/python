# -*- coding: utf-8 -*-
from db.api.apiutils import dec_get_cache, APIResult, dec_make_conn_cursor
from db.cores.cache import cache
from utils.logger import logger as log
from utils.tool import dec_timeit


def get_catagory_tag(catagory_name):
    if not isinstance(catagory_name, basestring):
        log.warn("catagory is not a string")
        return APIResult(code=True)
    redis_key = 'get_catagory_tag_%s' % catagory_name

    @dec_timeit('get_catagory_tag')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT DISTINCT
                    ctr.career_id,
                    t.id,
                    t.name,
                    t.short_name
                FROM
                    mz_course_careertagrelation AS ctr
                JOIN mz_course_tag AS t ON t.id = ctr.tag_id
                JOIN mz_course_newcareer AS ncc ON ncc.id = ctr.career_id
                WHERE ncc.short_name = %s;
            """
            cursor.execute(sql, catagory_name)
            catagory_tag = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set(redis_key, catagory_tag, 60 * 5)

        return APIResult(result=catagory_tag)

    return main(_enable_cache=True)


def get_tag():
    @dec_timeit('get_tag')
    @dec_get_cache('get_tag')
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT DISTINCT
                    ctr.career_id,
                    t.id,
                    t.name,
                    t.short_name
                FROM
                    mz_course_careertagrelation AS ctr
                JOIN mz_course_tag AS t ON t.id = ctr.tag_id
                JOIN mz_course_newcareer AS ncc ON ncc.id = ctr.career_id;
            """
            cursor.execute(sql)
            catagory_tag = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set('get_tag', catagory_tag, 60 * 5)

        return APIResult(result=catagory_tag)

    return main(_enable_cache=True)


def get_tag_name(tag):
    if not isinstance(tag, basestring):
        log.warn("tag is not a string")
        return APIResult(code=True)
    redis_key = 'get_tag_name_%s' % tag

    @dec_timeit('get_tag_name')
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
                    mz_course_tag
                WHERE
                    short_name = %s;
            """
            cursor.execute(sql, tag)
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


def get_tag_having_career_id():
    @dec_timeit('get_tag_having_career_id')
    @dec_get_cache('get_tag_having_career_id')
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT
                  ctr.career_id,
                  t.id,
                  t.name,
                  t.short_name
                FROM mz_course_careertagrelation AS ctr
                JOIN mz_course_tag AS t ON t.id = ctr.tag_id;
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
        cache.set('get_tag_having_career_id', result, 60 * 5)

        return APIResult(result=result)

    return main(_enable_cache=True)

