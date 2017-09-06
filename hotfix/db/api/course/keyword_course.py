# -*- coding: utf-8 -*-
from db.api.apiutils import dec_get_cache, APIResult, dec_make_conn_cursor
from db.cores.cache import cache
from utils.logger import logger as log
from utils.tool import dec_timeit


def get_keyword_course(keyword):
    if not isinstance(keyword, basestring):
        log.warn("keyword is not a string")
        return APIResult(code=True)

    @dec_timeit('get_keyword_course')
    @dec_get_cache('get_keyword_course_%s' % keyword)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """

        try:
            sql = """
                SELECT DISTINCT
                    oti.obj_id,
                    c.name,
                    c.image,
                    c.student_count,
                    c.date_publish,
                    c.student_count,
                    c.favorite_count,
                    c.click_count
                FROM
                    mz_common_objtagindex AS oti
                JOIN mz_course_course AS c ON c.id = oti.obj_id
                WHERE
                    oti.obj_type = 'COURSE'
                AND oti.keywords = '%s'
            """ % str(keyword)
            cursor.execute(sql)
            keyword_course = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set('get_keyword_course_%s' % keyword, keyword_course, 60 * 5)

        return APIResult(result=keyword_course)

    return main(_enable_cache=True)
