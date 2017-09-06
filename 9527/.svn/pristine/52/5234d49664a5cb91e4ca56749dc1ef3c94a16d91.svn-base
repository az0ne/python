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
                SELECT id,name FROM mz_free_questionnaire;
            """)
        questionnaire = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=questionnaire)



# 删除api
@dec_timeit
@dec_make_conn_cursor
def delete_questionnaire_item_by_id(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
               DELETE FROM mz_free_questionnaire_item WHERE id=%s;
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
            SELECT mz_free_questionnaire_item.id,stem,ques_options,ques_index,name
            FROM mz_free_questionnaire_item,mz_free_questionnaire
            WHERE mz_free_questionnaire_item.questionnaire_id = mz_free_questionnaire.id AND stem like %s
            ORDER BY id DESC
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
def list_questionnaire_item_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT mz_free_questionnaire_item.id,stem,ques_options,ques_index,name
                FROM mz_free_questionnaire_item,mz_free_questionnaire
                WHERE mz_free_questionnaire_item.questionnaire_id = mz_free_questionnaire.id
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        questionnaireitem = cursor.fetchall()
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
        "result": questionnaireitem,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)







#添加API
@dec_timeit
@dec_make_conn_cursor
def insert_questionnaire_item(conn, cursor, ques_stem, ques_anw, ques_ind, ques_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_free_questionnaire_item (stem, ques_options, ques_index, questionnaire_id) values (%s,%s,%s,%s);
            """, (ques_stem,ques_anw,ques_ind,ques_id))
        cursor.execute(
            """
                select last_insert_id() as questionnaire_id;
            """)
        questionnaire = cursor.fetchone()["questionnaire_id"]
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=questionnaire)


@dec_timeit
@dec_make_conn_cursor
def counttwoques_id(conn, cursor):
    try:
        cursor.execute(
            """
                SELECT COUNT(id) AS counttwoques FROM mz_free_questionnaire_item WHERE questionnaire_id = 2
            """
        )
        questionnaireitem = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=questionnaireitem)

