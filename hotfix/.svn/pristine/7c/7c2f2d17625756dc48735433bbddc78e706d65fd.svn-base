# -*- coding: utf-8 -*-
from db.api.apiutils import dec_get_cache, APIResult, dec_make_conn_cursor
from db.cores.cache import cache
from utils.logger import logger as log
from utils.tool import dec_timeit


def get_catagory_tag(catagory_id):
    if not isinstance(catagory_id, basestring):
        log.warn("catagory is not a string")
        return APIResult(code=True)
    if catagory_id:
        redis_key = 'get_catagory_tag_%s' % catagory_id
        where_clause = ('WHERE ncc.name = "%s"' % catagory_id) if catagory_id else ''
    else:
        redis_key = 'get_catagory_tag'
        where_clause = ''

    @dec_timeit('get_catagory_tag')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT DISTINCT
                    ctr.careercatagory_id,
                    t.id,
                    t.name
                FROM
                    mz_course_careertagrelation AS ctr
                JOIN mz_course_tag AS t ON t.id = ctr.tag_id
                JOIN mz_course_newcareercatagory AS ncc ON ncc.id = ctr.careercatagory_id
                %s;
            """ % where_clause
            cursor.execute(sql)
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
