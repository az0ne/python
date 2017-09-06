# -*- coding: utf-8 -*-
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("wechat_menu")
@dec_make_conn_cursor
def wechat_menu(conn, cursor):
    """
    获取微信菜单设置
    :param conn:
    :param cursor:
    :return:
    """
    sql = """
            SELECT menu.key,reply.type AS type,reply.content
                  FROM mz_wechat_menu AS menu
                  INNER JOIN mz_wechat_reply_menu AS reply_menu ON reply_menu.wechat_menu_id = menu.id
                  INNER JOIN mz_wechat_reply AS reply ON reply_menu.wechat_reply_id=reply.id
            WHERE menu.type = 2
            """
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)


@dec_timeit("wechat_message")
@dec_make_conn_cursor
def wechat_message(conn, cursor):
    """
    获取微信回复设置
    :param conn:
    :param cursor:
    :return:
    """
    sql = """
            SELECT message.type AS message_type, message.key, message.match_type, reply.type AS type, reply.content
            FROM mz_wechat_message AS message
            INNER JOIN mz_wechat_reply_message AS reply_message ON reply_message.wechat_message_id = message.id
            INNER JOIN mz_wechat_reply AS reply ON reply_message.wechat_reply_id = reply.id

            """
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
                'execute exception: %s. '
                'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)
