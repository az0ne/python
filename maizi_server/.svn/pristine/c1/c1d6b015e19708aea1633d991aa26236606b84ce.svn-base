# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor


def list_note():
    sql = """
    select * from mz_lps_note
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=result)

    return main()

def get_note(item_id,knowledge_id,course_id):
    sql = """
    select * from
    mz_lps_note
    where
    item_id=%s
    and
    knowledge_id=%s
    and
    course_id=%s
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(sql,(item_id, knowledge_id, course_id))
            result = cursor.fetchall()
            log.info("db execute:" + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def add_note(content,item_id,knowledge_id,course_id):
    _sql = """
    insert into mz_lps_note
    (content,item_id,knowledge_id,course_id)
    values
    (%s,%s,%s,%s)
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(_sql, (content,item_id,knowledge_id,course_id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def get_note_by_id(note_id):
    _sql = """
    select id,content from mz_lps_note
    where id=%s
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(_sql,note_id)
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def update_note(content,note_id):

    _sql = """
    update mz_lps_note
    set content=%s
    where id=%s
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(_sql,( content,note_id))
            conn.commit()
            log.info("db execute :" + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()
