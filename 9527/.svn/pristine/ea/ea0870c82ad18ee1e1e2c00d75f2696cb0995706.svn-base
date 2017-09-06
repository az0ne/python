# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor




# 列表API
@dec_timeit
@dec_make_conn_cursor
def list_homepagelink_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id,title,url,`index`
                FROM mz_homepage_link
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        homepagelink = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_homepage_link

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
        "result": homepagelink,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)


# 删除api
@dec_timeit
@dec_make_conn_cursor
def delete_homepagelink_by_id(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
               DELETE FROM mz_homepage_link WHERE id=%s;
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
def get_homepagelink_by_title(conn, cursor, title, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT id,title,url,`index`
            FROM mz_homepage_link
            WHERE title like %s
            ORDER BY id DESC
            limit %s,%s
            """, (title, start_index, page_size,))
        homepagelink = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_homepage_link WHERE title LIKE %s
            """, (title,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": homepagelink,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)



#添加API
@dec_timeit
@dec_make_conn_cursor
def insert_homepagelink(conn, cursor, title, url, index):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_homepage_link (title, url, `index`) values (%s,%s,%s);
            """, (title,url,index,))
        cursor.execute(
            """
                select last_insert_id() as homepagelink_id;
            """)
        homepagelink = cursor.fetchone()["homepagelink_id"]
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=homepagelink)


@dec_timeit
@dec_make_conn_cursor
def updatehomepageink(conn, cursor,_id,title,url,index):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                  UPDATE mz_homepage_link set title=%s, url=%s, `index`=%s WHERE id = %s;
            """, (title,url,index, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)




@dec_timeit
@dec_make_conn_cursor
def get_homepageink_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT  id ,title,url,`index`
                FROM mz_homepage_link WHERE id = %s
            """, (_id,))
        homepagelink = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=homepagelink)