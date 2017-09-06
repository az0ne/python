# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor

@dec_timeit
@dec_make_conn_cursor
def insert_menu(conn, cursor, name, url):
    """
        returns:
        result():
        iserror():True/False
    """
    try:
        cursor.execute(
            """
                insert into mz_back_menu (name,url) values (%s,%s,%s);
            """, (name,url,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=newItemId)


@dec_timeit
@dec_make_conn_cursor
def list_menu_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  id ,name,url,parent_id
                FROM mz_back_menu
                limit %s,%s
            """, (start_index, page_size,))
        menus = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_back_menu
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    menus_dict = {
        "result": menus,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=menus_dict)

@dec_timeit
@dec_make_conn_cursor
def list_menus(conn, cursor):
     """
     """
     try:
         cursor.execute(
            """
                SELECT id ,name, url, parent_id
                FROM mz_back_menu
            """,)
         AdminMenus = cursor.fetchall()
     except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
     return APIResult(result=AdminMenus)


@dec_timeit
@dec_make_conn_cursor
def count_role_have_the_menu(conn, cursor, role_id):

     try:
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_back_role_menu
                WHERE role_id=%s
            """, (role_id,))
        count = cursor.fetchone()["count"]
     except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

     return APIResult(result=count)

@dec_timeit
@dec_make_conn_cursor
def delete_role_menu_by_role_id(conn, cursor, role_id):

     try:
        cursor.execute(
            """
               DELETE FROM mz_back_role_menu WHERE role_id=%s;
            """, (role_id,))
        conn.commit()
     except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

     return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def insert_role_menu(conn, cursor, role_id, menu_id):
    """
        returns:
        result():
        iserror():True/False
    """
    try:
        cursor.execute(
            """
                insert into mz_back_role_menu (role_id,menu_id) values (%s,%s);
            """, (role_id,menu_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def get_menu_by_id(conn, cursor, _id):
    """
    """
    try:
         cursor.execute(
            """
            SELECT id,name,url,parent_id
            FROM mz_back_menu
            WHERE id=%s;
            """,(_id,))
         menus = cursor.fetchall()
    except Exception as e:
         print e
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=menus)

@dec_timeit
@dec_make_conn_cursor
def get_had_menus_by_role_id(conn, cursor, role_id):
    """
    """
    try:
         cursor.execute(
            """
            SELECT role_menu.menu_id as menu_id, menu.name as menu_name,menu.parent_id as parent_id
            FROM mz_back_role_menu as role_menu
            LEFT JOIN mz_back_menu as menu ON role_menu.menu_id=menu.id
            WHERE role_id=%s;
            """,(role_id,))
         menus = cursor.fetchall()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=menus)


@dec_timeit
@dec_make_conn_cursor
def update_menu_by_id(conn, cursor,name,url, menu_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                update mz_back_menu set name=%s,url=%s WHERE id=%s;
            """, (name, url, menu_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)