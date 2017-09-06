# -*- coding: utf-8 -*-
from db.api.apiutils import dec_get_cache, APIResult, dec_make_conn_cursor
from db.cores.cache import cache
from utils.logger import logger as log
from utils.tool import dec_timeit


def get_catagory_tag_course(catagory_id, tag_id):
    if not isinstance(catagory_id, basestring):
        log.warn("catagory is not a string")
        return APIResult(code=True)
    if not isinstance(tag_id, basestring):
        log.warn("tag_id is not a string")
        return APIResult(code=True)
    if tag_id:
        redis_key = 'get_tag_course_%s' % tag_id
        where_clause = 'AND t.name = "%s"' % tag_id
    elif catagory_id:
        redis_key = 'get_catagory_course_%s' % catagory_id
        where_clause = 'AND ncc.name = "%s"' % catagory_id
    else:
        redis_key = 'get_course'
        where_clause = ''

    @dec_timeit('get_catagory_tag_course')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """

        try:
            sql = """
                SELECT DISTINCT
                    otr.obj_id,
                    c.name,
                    c.image,
                    c.date_publish,
                    c.student_count,
                    c.favorite_count,
                    c.click_count
                FROM
                    mz_common_objtagrelation AS otr
                JOIN mz_course_course AS c ON c.id = otr.obj_id
                JOIN mz_course_newcareercatagory AS ncc ON ncc.id = otr.careercatagory_id
                JOIN mz_course_tag AS t ON t.id = otr.tag_id
                WHERE
                    otr.obj_type = 'COURSE'
                %s;
            """ % where_clause
            cursor.execute(sql)
            course = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set(redis_key, course, 60 * 5)

        return APIResult(result=course)

    return main(_enable_cache=True)
