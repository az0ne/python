# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_role(conn, cursor, name):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_back_role (name) values (%s);
            """, (name,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def update_role_by_id(conn, cursor, role_id, role_name):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                update mz_back_role set name=%s WHERE id=%s;
            """, (role_name,role_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def list_role_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  id ,name
                FROM mz_back_role
                limit %s,%s
            """, (start_index, page_size,))
        AdminRole = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_back_role
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    adminRole_dict = {
        "result": AdminRole,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=adminRole_dict)


@dec_timeit
@dec_make_conn_cursor
def get_role_by_id(conn, cursor, _id):
    """
    """
    try:
         cursor.execute(
            """
            SELECT id ,name
            FROM mz_back_role
            WHERE id=%s;
            """,(_id,))
         AdminRoles = cursor.fetchall()
    except Exception as e:
         print e
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=AdminRoles)

@dec_timeit
@dec_make_conn_cursor
def list_roles(conn, cursor):
     """
     """
     try:
         cursor.execute(
            """
                SELECT  id ,name
                FROM mz_back_role
            """,)
         AdminRoles = cursor.fetchall()
     except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
     return APIResult(result=AdminRoles)




@dec_timeit
@dec_make_conn_cursor
def list_role_and_admin(conn, cursor):
     """
     """
     try:
         cursor.execute(
            """
                SELECT  role.id ,role.name,admin_role.user_id
                FROM mz_back_admin_role as admin_role
                LEFT JOIN mz_back_role as role ON admin_role.role_id=role.id
            """,)
         AdminRoles = cursor.fetchall()
     except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
     return APIResult(result=AdminRoles)


@dec_timeit
@dec_make_conn_cursor
def update_admin_role_by_user(conn, cursor, role_id,user_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                update mz_back_admin_role set role_id=%s WHERE user_id=%s;
            """, (role_id,user_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_roles_by_keyword(conn, cursor, page_index, page_size,keyword):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  id ,name
                FROM mz_back_role
                WHERE name LIKE %s
                limit %s,%s
            """, (keyword,start_index, page_size,))
        roles = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_back_role
                WHERE name LIKE %s
            """,(keyword,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    roles_dict = {
        "result": roles,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=roles_dict)


@dec_timeit
@dec_make_conn_cursor
def count_have_role_name(conn, cursor,name):

     try:
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_back_role
                WHERE name=%s
            """, (name,))
        count = cursor.fetchone()["count"]
     except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

     return APIResult(result=count)