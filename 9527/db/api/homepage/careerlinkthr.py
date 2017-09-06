# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


# 删除api
@dec_timeit
@dec_make_conn_cursor
def delete_careerlink_by_id(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
               DELETE FROM mz_career3_link WHERE id=%s;
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
def get_careerlink_by_title(conn, cursor, title, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT id,title,url,career_id,`index`
            FROM mz_career3_link
            WHERE title like %s
            ORDER BY id DESC
            limit %s,%s
            """, (title, start_index, page_size,))
        careerlink = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_career3_link WHERE title LIKE %s
            """, (title,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": careerlink,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)



# 列表API
@dec_timeit
@dec_make_conn_cursor
def list_careerlink_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT mz_career3_link.id,title,url,career_id,mz_career3_link.`index`,name
                FROM mz_career3_link,mz_course_careercourse
                WHERE mz_career3_link.career_id=mz_course_careercourse.id
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        careerlink = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_career3_link

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
        "result": careerlink,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)




#编辑API
@dec_timeit
@dec_make_conn_cursor
def get_careerlink_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT  id,title,url,career_id,`index`
                FROM mz_career3_link WHERE id = %s
            """, (_id,))
        careerlink = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerlink)




#添加API
@dec_timeit
@dec_make_conn_cursor
def insert_careerlink(conn, cursor, title, url, index, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_career3_link (title, url, `index`, career_id) values (%s,%s,%s,%s);
            """, (title,url,index,career_id))
        cursor.execute(
            """
                select last_insert_id() as careerlink_id;
            """)
        careerlink = cursor.fetchone()["careerlink_id"]
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerlink)



#编辑确认API
@dec_timeit
@dec_make_conn_cursor
def updatecareerlink(conn, cursor,_id,title,url,index,career_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                  UPDATE mz_career3_link set title=%s, url=%s, `index`=%s, career_id=%s WHERE id = %s;
            """, (title,url,index,career_id, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)