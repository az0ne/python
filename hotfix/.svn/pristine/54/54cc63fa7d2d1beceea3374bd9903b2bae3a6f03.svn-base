# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("save_user")
@dec_make_conn_cursor
def save_user(conn, cursor, open_id, union_id, nick_name, avatar):
    """
    保存微信用户open_id union_id
    """
    seletc_sql = """
        SELECT 1 FROM mz_wechat_user WHERE open_id=%s AND union_id=%s FOR UPDATE
    """
    insert_sql = """
        INSERT INTO mz_wechat_user (open_id, union_id, nick_name, avatar) VALUE (%s,%s,%s,%s)
    """
    update_sql = """
        UPDATE mz_wechat_user SET nick_name=%s, avatar=%s WHERE open_id=%s AND union_id=%s
    """
    try:
        cursor.execute(seletc_sql, (open_id, union_id))
        is_exists = cursor.fetchone()
        if not is_exists:
            cursor.execute(insert_sql, (open_id, union_id, nick_name, avatar))
        else:
            cursor.execute(update_sql, (nick_name, avatar, open_id, union_id))
        conn.commit()

        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_timeit("get_user_by_union_id")
@dec_make_conn_cursor
def get_user_by_union_id(conn, cursor, union_id):
    """
    根据union_id获取用户
    """

    sql = """
        SELECT * FROM mz_wechat_user WHERE union_id = %s;
    """

    try:
        cursor.execute(sql, (union_id,))
        data = cursor.fetchone()

        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data) if data else APIResult(code=False)
