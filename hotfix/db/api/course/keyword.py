# -*- coding: utf-8 -*-
from db.api.apiutils import dec_get_cache, APIResult, dec_make_conn_cursor
from db.cores.cache import cache
from utils.logger import logger as log
from utils.tool import dec_timeit


def get_keyword(obj_type='COURSE'):
    @dec_timeit('get_keyword')
    @dec_get_cache('get_keyword')
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT
                    oti.obj_id,
                    oti.keywords
                FROM
                    mz_common_objtagindex AS oti
                WHERE obj_type = %s;
            """
            cursor.execute(sql, obj_type)
            keyword = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set('get_keyword', keyword, 60 * 5)

        return APIResult(result=keyword)

    return main(_enable_cache=True)
