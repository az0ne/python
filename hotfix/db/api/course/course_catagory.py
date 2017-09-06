# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_timeit("get_course_catagories")
@dec_get_cache("get_course_catagories")
@dec_make_conn_cursor
def get_course_catagories(conn, cursor):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id, career_catagory_id, name, is_hot_tag
                FROM mz_course_coursecatagory
            """)
        course_catagories = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:" % (e, cursor._last_executed))
        raise e

    course_catagory_dict = {
        "result": course_catagories,
    }
        
    # set cache
    cache.set("get_course_catagories", course_catagory_dict)

    return APIResult(result=course_catagory_dict)