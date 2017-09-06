# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor

# 雇用教师信息api集


# 删除api
@dec_timeit
@dec_make_conn_cursor
def delete_employteacher_by_id(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
               DELETE FROM mz_employ_teacher WHERE id=%s;
            """, (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)



# 搜索api
@dec_timeit
@dec_make_conn_cursor
def list_employteacher_by_resume(conn, cursor, resume, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT id,teacher_type,teacher_catagory,name,career,work_time,resume,mobile,create_time,qq
            FROM mz_employ_teacher
            WHERE resume like %s
            ORDER BY id DESC
            limit %s,%s
            """, (resume, start_index, page_size,))
        employteacher = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_employ_teacher WHERE resume LIKE %s
            """, (resume,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": employteacher,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)



# 列表API
@dec_timeit
@dec_make_conn_cursor
def list_employteacher_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id,teacher_type,teacher_catagory,name,career,work_time,resume,mobile,create_time,qq
                FROM mz_employ_teacher
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        employteacher = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_employ_teacher

            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": employteacher,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)



# 查看API
@dec_timeit
@dec_make_conn_cursor
def get_employteacher_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id,teacher_type,teacher_catagory,name,career,work_time,resume,mobile,create_time,qq
                FROM mz_employ_teacher WHERE id = %s
            """, (_id,))
        employteacher = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=employteacher)



