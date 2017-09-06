# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor

@dec_timeit
@dec_make_conn_cursor
def insert_AdminUsr(conn, cursor,user_id, name, remark, pwd):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_back_admin (id,name,remark,pwd) values (%s,%s,%s,%s);
            """, (user_id, name,remark, pwd,))
        cursor.execute(
            """
                insert into mz_back_admin_role (user_id) values (%s);
            """, (user_id,))
        conn.commit()
    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_remark_AdminUsr(conn, cursor, _id ,remark):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                  UPDATE mz_back_admin set remark=%s WHERE id = %s;
            """, (remark, _id,))
        conn.commit()
    except Exception as e:
        print 'in except',e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)




@dec_timeit
@dec_make_conn_cursor
def delete_AdminUsr(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_back_admin WHERE id=%s;
            """, (_id,))
        cursor.execute(
            """
                DELETE FROM mz_back_admin_role WHERE user_id=%s;
            """, (_id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_AdminUsr(conn, cursor):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id ,name ,pwd
                FROM mz_back_admin
            """)
        adminUsrs = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=adminUsrs)


@dec_timeit
@dec_make_conn_cursor
def list_AdminUsr_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  admin.id ,admin.name,admin.remark,admin_role.role_id as role_id
                FROM mz_back_admin as admin
                LEFT JOIN mz_back_admin_role as admin_role ON admin_role.user_id=admin.id
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        AdminUsrs = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_back_admin
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    adminUsr_dict = {
        "result": AdminUsrs,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=adminUsr_dict)


@dec_timeit
@dec_make_conn_cursor
def get_AdminUsr_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT  id ,name,remark,pwd
                FROM mz_back_admin WHERE id = %s
            """, (_id,))
        AdminUsr = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=AdminUsr)

@dec_timeit
@dec_make_conn_cursor
def get_AdminUsr_by_name(conn, cursor, name):
    """
    """
    try:
        cursor.execute(
            """
                SELECT  id, name,pwd
                FROM mz_back_admin WHERE name=%s
            """, (name,))
        AdminUsr = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=AdminUsr)
    
@dec_timeit
@dec_make_conn_cursor
def get_AdminUsr_by_name_or_id(conn, cursor, name, _id):
    """
    """
    try:
        cursor.execute(
            """
                SELECT  id,name
                FROM mz_back_admin WHERE name = %s or id = %s
            """, (name,_id,))
        AdminUsr = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=AdminUsr)

@dec_timeit
@dec_make_conn_cursor
def update_pwd_AdminUsr(conn, cursor, _id , pwd):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                  UPDATE mz_back_admin set pwd=%s WHERE id = %s;
            """, ( pwd, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def get_AdminUsr_by_keyword(conn, cursor, page_index, page_size,keyword):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  admin.id ,admin.name,admin.remark,admin_role.role_id as role_id
                FROM mz_back_admin as admin
                LEFT JOIN mz_back_admin_role as admin_role ON admin_role.user_id=admin.id
                WHERE admin.name LIKE %s or admin.remark LIKE %s or admin.id LIKE %s
                ORDER BY admin.id DESC
                limit %s,%s
            """, (keyword,keyword,keyword,start_index, page_size,))
        AdminUsrs = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_back_admin
                WHERE name LIKE %s or remark LIKE %s or id LIKE %s
            """,(keyword,keyword,keyword,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    adminUsr_dict = {
        "result": AdminUsrs,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=adminUsr_dict)


@dec_timeit
@dec_make_conn_cursor
def get_menus_by_urser_id(conn, cursor, user_id):
    """
    """
    try:
        cursor.execute(
            """
                SELECT  menu.id,menu.name,menu.url,menu.parent_id
                FROM mz_back_menu as menu
                LEFT JOIN mz_back_role_menu as role_menu ON  menu.id=role_menu.menu_id
                LEFT JOIN mz_back_role as role ON role.id=role_menu.role_id
                LEFT JOIN mz_back_admin_role as admin_role ON admin_role.role_id=role.id
                WHERE admin_role.user_id = %s
            """, (user_id,))
        menus = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=menus)


@dec_make_conn_cursor
@dec_timeit
def get_role_by_user_id(conn, cursor, user_id):
    """
    根据user_id查询role
    :param conn:
    :param cursor:
    :param user_id:
    :return:
    """

    sql = """
        SELECT
            role.*
        FROM
            mz_back_role AS role
        INNER JOIN mz_back_admin_role AS ar ON ar.role_id = role.id
        WHERE
            ar.user_id = %s
    """

    try:
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=result)
