# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor

#mz_questionnaire表ajax
@dec_timeit
@dec_make_conn_cursor
def ajax_questionnaire(conn, cursor):
    try:
        cursor.execute(
            """
                SELECT * FROM mz_free_questionnaire;
            """)
        questionnaire = cursor.fetchall()
    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    employ_dict = {
        "questionnaireajax": questionnaire,
    }
    return APIResult(result=employ_dict)



# 删除api
@dec_timeit
@dec_make_conn_cursor
def delete_questionnairequery_item_by_id(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
               DELETE FROM mz_free_questionnaire_record WHERE id=%s;
            """, (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)



# 搜索api
@dec_timeit
@dec_make_conn_cursor
def get_questionnaire_item_by_stem(conn, cursor, stem, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT
                    q.*, COUNT(DISTINCT qi.id) AS itemquantity,
                    COUNT(DISTINCT qr.id) AS ques_count
                FROM
                    mz_free_questionnaire AS q
                LEFT JOIN mz_free_questionnaire_item AS qi ON qi.questionnaire_id = q.id
                LEFT JOIN mz_free_questionnaire_record AS qr ON qr.questionnaire_id = q.id
                WHERE name = %s
                GROUP BY
                    q.id
                limit %s,%s
            """, (stem, start_index, page_size,))
        questionnaireitem = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_free_questionnaire_item WHERE stem LIKE %s
            """, (stem,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": questionnaireitem,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)



# 列表API
@dec_timeit
@dec_make_conn_cursor
def list_questionnairequery_item_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """

                SELECT
                    q.*, COUNT(DISTINCT qi.id) AS itemquantity,
                    COUNT(DISTINCT qr.id) AS ques_count
                FROM
                    mz_free_questionnaire AS q
                LEFT JOIN mz_free_questionnaire_item AS qi ON qi.questionnaire_id = q.id
                LEFT JOIN mz_free_questionnaire_record AS qr ON qr.questionnaire_id = q.id
                GROUP BY
                    q.id
                limit %s,%s
            """, (start_index, page_size,))
        questionnairequery = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_free_questionnaire_item

            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    employ_dict = {
        "result": questionnairequery,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)







#添加API
@dec_timeit
@dec_make_conn_cursor
def query_questionnaireitem(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                SELECT stem,ques_options FROM mz_free_questionnaire_item WHERE questionnaire_id = %s
            """, (_id,))
        questionnaireitem = cursor.fetchall()
        cursor.execute(
        """
            SELECT
            a.questionnaire_id AS '所属问卷ID',
            a.questionnaire_item_id AS belongques,
            a.record AS belonganw,
            COUNT(*) AS chocount,
            b.*
            FROM
            mz_free_questionnaire_record a
            LEFT JOIN mz_free_questionnaire_item b ON a.questionnaire_item_id = b.id
            WHERE
            a.questionnaire_id = %s
            GROUP BY
            a.questionnaire_item_id,
            a.record

        """, (_id,))
        questionnaireinfo = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    employ_dict = {
        "result": questionnaireitem,
        "resultoth": questionnaireinfo,
    }
    return APIResult(result=employ_dict)


