# coding: utf-8

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor

@dec_timeit
@dec_make_conn_cursor
def get_city_name_by_city_id(conn, cursor, city_id):
    try:
        cursor.execute(
            """
                SELECT city.name as city_name,province.name as province_name
                FROM mz_user_citydict as city
                LEFT JOIN mz_user_provincedict as province
                ON city.province_id=province.id
                WHERE city.id=%s
            """, (city_id,))
        ops = cursor.fetchone()
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=ops)