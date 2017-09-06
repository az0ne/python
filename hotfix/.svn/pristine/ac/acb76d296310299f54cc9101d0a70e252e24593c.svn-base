# -*- coding: utf-8 -*-
from db.api.apiutils import dec_get_cache, APIResult, dec_make_conn_cursor
from db.cores.cache import cache
from utils.logger import logger as log
from utils.tool import dec_timeit


def get_type_ad(ad_type):
    if not isinstance(ad_type, basestring):
        log.warn("ad_type is not a string")
        return APIResult(code=True)
    redis_key = 'get_type_ad_%s' % ad_type

    @dec_timeit('get_type_ad')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        """
        """
        try:
            sql = """
                SELECT
                    a.title,
                    a.callback_url,
                    a.image_url
                FROM
                    mz_common_ad AS a
                WHERE a.type = %s;
            """
            cursor.execute(sql, ad_type)
            type_ad = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set(redis_key, type_ad, 60 * 5)

        return APIResult(result=type_ad)

    return main(_enable_cache=True)
