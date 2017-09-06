# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor

@dec_timeit("get_career_catagories")
@dec_get_cache("get_career_catagories")
@dec_make_conn_cursor
def get_career_catagories(conn, cursor):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id, name
                FROM mz_course_newcareercatagory
                ORDER BY `index`
            """)
        career_catagories = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e

    # set cache
    cache.set("get_career_catagories", career_catagories)

    return APIResult(result=career_catagories)