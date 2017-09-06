# -*- coding: utf-8 -*-
from db.api.apiutils import dec_get_cache, APIResult, dec_make_conn_cursor
from db.cores.cache import cache
from utils.logger import logger as log
from utils.tool import dec_timeit


def get_page_name_seo(page_name):
    if not isinstance(page_name, basestring):
        log.warn("page_name is not a string")
        return APIResult(code=True)
    redis_key = 'get_page_name_seo_%s' % page_name

    @dec_timeit('get_page_name_seo')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT
                    ps.seo_title,
                    ps.seo_description,
                    ps.seo_keyword
                FROM
                    mz_common_pageseoset AS ps
                WHERE ps.page_name = %s;
            """
            cursor.execute(sql, page_name)
            page_name_seo = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set(redis_key, page_name_seo, 60 * 5)

        return APIResult(result=page_name_seo)

    return main(_enable_cache=True)
