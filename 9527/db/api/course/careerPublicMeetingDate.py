# -*-coding:utf-8-*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def list_career_public_meeting_date_by_page(conn, cursor, page_index, page_size):
    """
    分页查询
    :param conn:
    :param cursor:
    :param page_index:
    :param page_size:
    :return:
    """
    page_start = tool.get_page_info(page_index, page_size)
    base_sql = """
                select {field} from mz_career_public_meeting_date as cpmd
                INNER JOIN mz_career_page as cp ON cp.id=cpmd.career_id
    """
    limit = "limit {0},{1}".format(page_start, page_size)
    page_sql = base_sql.format(field="cpmd.id,cp.name,cpmd.mobile,cpmd.enter_date,cpmd.class_time,qq_group") + limit
    total_sql = base_sql.format(field="count(cpmd.id) as count")
    try:
        cursor.execute(page_sql)
        result = cursor.fetchall()

        log.debug("query: %s" % cursor.statement)

        cursor.execute(total_sql)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

        log.debug("query: %s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s"
            "statement: %s" % (e, cursor.statement)
        )
    res_dict = {
        "result": result,
        "rows_count": rows_count['count'],
        "page_count": page_count
    }

    return APIResult(result=res_dict)


@dec_timeit
@dec_make_conn_cursor
def list_career_public_meeting_date_by_career_id(conn, cursor, career_id, page_index, page_size):
    """
    根据职业课程ID查询数据
    :param conn:
    :param cursor:
    :param career_id: 课程ID
    :param page_index:
    :param page_size:
    :return:
    """
    page_start = tool.get_page_info(page_index, page_size)

    base_sql = "select {field} from mz_career_public_meeting_date as cpmd " \
               "INNER JOIN mz_career_page as cp ON cp.id=cpmd.career_id " \
               "where career_id = {career_id} "

    limit = "limit {0},{1}".format(page_start, page_size)
    page_sql = base_sql.format(field="cpmd.id,cp.name,cpmd.mobile,cpmd.enter_date,cpmd.class_time,cpmd.qq_group",
                               career_id=career_id) + limit
    total_sql = base_sql.format(field="count(cpmd.id) as count", career_id=career_id)

    try:
        cursor.execute(page_sql)
        result = cursor.fetchall()

        log.debug("query: %s" % cursor.statement)

        cursor.execute(total_sql)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

        log.debug("query: %s" % cursor.statement)

    except Exception as e:
        log.warn(
            "execute exception: %s"
            "statement: %s" % (e, cursor.statement)
        )

    res_dict = {
        "result": result,
        "rows_count": rows_count['count'],
        "page_count": page_count,
    }

    return APIResult(result=res_dict)


@dec_timeit
@dec_make_conn_cursor
def delete_career_public_meeting_date_by_id(conn, cursor, _id):
    """
    删除职业课程公布会议日期，根据id
    :param conn:
    :param cursor:
    :param _id: 职业课程公布会议日期ID
    :return:
    """
    sql = "delete from mz_career_public_meeting_date WHERE id={0}".format(_id)

    try:
        cursor.execute(sql)
        conn.commit()
        log.debug("query: %s" % cursor.statement)

    except Exception as e:
        log.warn(
            "execute exception: %s"
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)
