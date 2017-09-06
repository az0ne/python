#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils.logger import logger as log

# @dec_timeit
# @dec_make_conn_cursor
# def insert_wechat_menu(conn, cursor, dict):
#     """
#         returns:
#         result():True/False
#         iserror():True/False
#     """
#     try:
#         cursor.execute(
#             """
#                 insert into mz_wechat_menu(type,`key`,name,location_x,location_y) values (%s,%s,%s,%s,%s);
#             """, (dict['type'],dict['key'],dict['name'],dict['location_x'],dict['location_x'],))
#         cursor.execute(
#             """
#                 select last_insert_id() as newMenuId;
#             """)
#         newMenuId = cursor.fetchone()["newMenuId"]
#         conn.commit()
#     except Exception as e:
#         log.warn(
#             "execute exception: %s. "
#             "statement: %s" % (e, cursor.statement))
#         raise e
#
#     return APIResult(result=newMenuId)


@dec_timeit
@dec_make_conn_cursor
def insert_wechat_menu_reply(conn, cursor, type, content, menu_id):
    """
        returns:
        result():True/False
        iserror():True/False
    """
    try:
        cursor.execute(
            """
                INSERT INTO mz_wechat_reply ( `type`, `content`)
                VALUES (%s, %s)
            """, (type, content,))
        cursor.execute(
            """
                select last_insert_id() as newId;
            """)
        reply_id = cursor.fetchone()["newId"]
        cursor.execute(
            """
                insert into mz_wechat_reply_menu(wechat_menu_id,wechat_reply_id) values (%s,%s);
            """, (menu_id,reply_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_wechat_menu_by_id(conn, cursor, dict):
    """
    更新微信菜单
    :param conn:
    :param cursor:
    :return: result():True/False
    """

    try:
        cursor.execute(
                """
                UPDATE mz_wechat_menu set type=%s,`key`=%s,name=%s
                WHERE id=%s;
                """, (dict['type'],dict['key'],dict['name'],dict['id']))
        conn.commit()
    except Exception as e:
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


# @dec_timeit
# @dec_make_conn_cursor
# def delete_wechat_menu_by_id(conn, cursor, _id):
#     """
#     删除微信菜单
#     :param conn:
#     :param cursor:
#     :return: result():True/False
#     """
#
#     try:
#         cursor.execute(
#                 """
#                DELETE FROM mz_wechat_menu WHERE id = %s
#                 """, (_id,))
#         conn.commit()
#     except Exception as e:
#         log.warn(
#                 "execute exception: %s. "
#                 "statement:%s" % (e, cursor.statement))
#         raise e
#     return APIResult(result=True)

# @dec_timeit
# @dec_make_conn_cursor
# def delete_wechat_menu_reply_by_menu_id(conn, cursor, _id):
#     """
#     删除微信菜单及reply
#     :param conn:
#     :param cursor:
#     :return: result():True/False
#     """
#
#     try:
#         cursor.execute(
#                 """
#                DELETE reply_menu,menu,reply FROM mz_wechat_menu as menu
#                LEFT JOIN mz_wechat_reply_menu as reply_menu ON reply_menu.wechat_menu_id=menu.id
#                LEFT JOIN mz_wechat_reply as reply ON reply_menu.wechat_reply_id=reply.id
#                WHERE menu.id = %s
#                 """, (_id,))
#         conn.commit()
#     except Exception as e:
#         log.warn(
#                 "execute exception: %s. "
#                 "statement:%s" % (e, cursor.statement))
#         raise e
#     return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_wechat_menu_by_id(conn, cursor, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
        cursor.execute(
                """
                SELECT id,type,`key`,name,location_x,location_y
                FROM mz_wechat_menu
                WHERE id=%s;
                """, (_id,))
        menu = cursor.fetchone()
    except Exception as e:
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=menu)


@dec_timeit
@dec_make_conn_cursor
def get_wechat_menu_reply_by_id(conn, cursor, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
        cursor.execute(
                """
                SELECT reply.id,reply.type,reply.content
                FROM mz_wechat_reply_menu as reply_menu
                LEFT JOIN mz_wechat_reply as reply ON reply_menu.wechat_reply_id=reply.id
                WHERE reply_menu.wechat_menu_id=%s;
                """, (_id,))
        menu = cursor.fetchall()
    except Exception as e:
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=menu)

@dec_timeit
@dec_make_conn_cursor
def list_wechat_menu(conn, cursor,):
    """
    获取所有的微信菜单
    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
        cursor.execute(
                """
                SELECT id, type,`key`,name,location_x,location_y
                FROM mz_wechat_menu
                ORDER BY location_x ,location_y
                """,)
        menu = cursor.fetchall()
    except Exception as e:
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=menu)


@dec_timeit
@dec_make_conn_cursor
def delete_wechat_menu_reply(conn, cursor, menu_id, reply_id):
    """
    删除微信菜单
    :param conn:
    :param cursor:
    :return: result():True/False
    """

    try:
        cursor.execute(
                """
               DELETE FROM mz_wechat_reply WHERE id = %s
                """, (reply_id,))
        cursor.execute(
                """
               DELETE FROM mz_wechat_reply_menu WHERE wechat_menu_id = %s and wechat_reply_id=%s
                """, (menu_id, reply_id))
        conn.commit()
    except Exception as e:
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_replys_by_menu_id(conn, cursor, menu_id):
    """
    根据菜单id删除所以的回复及关联信息
    :param conn:
    :param cursor:
    :param menu_id:
    :return:
    """
    try:
        cursor.execute(
            """
           DELETE reply_menu, reply FROM mz_wechat_reply_menu  as reply_menu
           LEFT JOIN mz_wechat_reply as reply ON reply_menu.wechat_reply_id=reply.id
           WHERE reply_menu.wechat_menu_id = %s
            """, (menu_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)
