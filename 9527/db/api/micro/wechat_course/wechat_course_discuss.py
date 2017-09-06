# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor
from db.cores.mongodbconn import get_mongo_db
from django.conf import settings


@dec_timeit
@dec_make_conn_cursor
def list_wechat_parent_discuss(conn, cursor, page_index, page_size):
    start_index = get_page_info(page_index, page_size)
    sql = """
            SELECT discuss.id, course_id, union_id, parent_id, nick_name, content, date_time, course.name
            FROM mz_wechat_course_discuss as discuss
            LEFT JOIN mz_wechat_course as course
            ON course.id = discuss.course_id
            WHERE discuss.parent_id=0
            ORDER by course_id DESC ,id DESC
            limit %s, %s
         """
    try:
        cursor.execute(sql, (start_index, page_size,))
        wechat_discuss = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wechat_course_discuss
                WHERE parent_id=0
            """, )
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    wechat_discuss_dict = {
        "result": wechat_discuss,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=wechat_discuss_dict)


@dec_timeit
@dec_make_conn_cursor
def list_wechat_parent_discuss_by_search(conn, cursor, page_index, page_size, keyword):
    start_index = get_page_info(page_index, page_size)
    sql = """
            SELECT discuss.id, course_id, union_id, parent_id, nick_name, content, date_time, course.name
            FROM mz_wechat_course_discuss as discuss
            LEFT JOIN mz_wechat_course as course
            ON course.id = discuss.course_id
            WHERE course.name LIKE %s and discuss.parent_id=0
            ORDER by course_id DESC ,id DESC
            limit %s, %s
         """
    try:
        cursor.execute(sql, (keyword, start_index, page_size,))
        wechat_discuss = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wechat_course_discuss as discuss
                LEFT JOIN mz_wechat_course as course
                ON course.id = discuss.course_id
                WHERE course.name LIKE %s and discuss.parent_id=0
            """, (keyword,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    wechat_discuss_dict = {
        "result": wechat_discuss,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=wechat_discuss_dict)


@dec_timeit
@dec_make_conn_cursor
def list_all_child_discuss(conn, cursor, parent_id):
    sql = """
            select id, course_id, union_id, parent_id, nick_name, content, date_time
            from mz_wechat_course_discuss
            WHERE parent_id = %s
          """
    try:
        cursor.execute(sql, (parent_id,))
        child_discuss = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=child_discuss)


@dec_timeit
@dec_make_conn_cursor
def get_discuss_by_id(conn, cursor, parent_id):
    sql = """
            SELECT discuss.id, course_id, union_id, parent_id, nick_name, content, date_time, course.name
            FROM mz_wechat_course_discuss as discuss
            LEFT JOIN mz_wechat_course as course
            ON course.id = discuss.course_id
            WHERE discuss.id = %s
        """
    try:
        cursor.execute(sql, (parent_id,))
        discuss = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=discuss)


@dec_timeit
@dec_make_conn_cursor
def del_parent_discuss_by_id(conn, cursor, _id):
    sql1 = """
            delete from mz_wechat_course_discuss WHERE id=%s
          """
    sql2 = """
            delete from mz_wechat_course_discuss WHERE parent_id=%s
            """
    try:
        cursor.execute(sql1, (_id,))
        cursor.execute(sql2, (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def del_child_discuss_by_id(conn, cursor, _id):
    sql = """
            delete from mz_wechat_course_discuss WHERE id=%s
          """
    try:
        cursor.execute(sql, (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def insert_discuss_by_id(conn, cursor, discuss_dict):
    sql = """
            insert into mz_wechat_course_discuss (course_id, parent_id,nick_name, content, date_time)
            VALUES (%s,%s,%s,%s,now())
          """
    try:
        cursor.execute(sql, (discuss_dict["course_id"], discuss_dict["parent_id"],
                             discuss_dict["nick_name"], discuss_dict["content"]))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
def get_reply_count(course_id, union_id):
    """
    获取回复次数并归零
    数据格式为：
    {
        "user_id": union_id,
        "course": {
            "reply_count":
                {
                    str(course_id): value
                }
        }
    }
    :param course_id:
    :param union_id:
    :return:
    """

    db = get_mongo_db(settings.MONGO_DB_NAME)

    try:
        field = "course.reply_count.{0}".format(course_id)
        count = db.wechat_user_info.find_one({"user_id": union_id},  {field: 1})
        if not count:
            count = 0
        else:
            count = count.get('course', {}).get('reply_count', {}).get(str(course_id), 0)
        # 归零
        db.wechat_user_info.update(
            {"user_id": union_id}, {"$set": {field: 0}}, upsert=True)

    except Exception as e:
        count = 0

    return APIResult(result=count)


@dec_timeit
def update_reply_count(course_id, union_id):
    """
    更新回复次数
    :param course_id:
    :param union_id:
    :return:
    """

    db = get_mongo_db(settings.MONGO_DB_NAME)

    try:
        field = "course.reply_count.{0}".format(course_id)
        db.wechat_user_info.update(
            {"user_id": union_id}, {"$inc": {field: 1}}, upsert=True)

    except Exception as e:
        return APIResult(result=False)

    return APIResult(result=True)
