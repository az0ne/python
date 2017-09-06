# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_timeit('get_seo_by_obj_id')
@dec_make_conn_cursor
def get_seo_by_obj_id(conn, cursor, obj_id, obj_type):
    """
    获取seo
    :return: ''
    """
    sql = """
        SELECT
            id,
            obj_id,
            obj_type,
            seo_title,
            seo_keywords,
            seo_description
        FROM
            mz_common_objseo
        WHERE
            obj_id = %s
        AND obj_type = %s
    """
    try:
        cursor.execute(sql, (obj_id, obj_type))
        seo = cursor.fetchone()
        log.info("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=seo)
