# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("get_banners")
@dec_make_conn_cursor
def get_banners(conn, cursor):
    """
    @brief 获取banner
    :param conn:
    :param cursor:
    :return:
    """

    sql = '''
        SELECT *
        FROM mz_wechat_banner
        ORDER BY `index`, id;
    '''

    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)
