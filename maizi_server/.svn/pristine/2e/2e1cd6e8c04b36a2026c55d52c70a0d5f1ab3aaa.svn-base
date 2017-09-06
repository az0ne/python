# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor


def add_author(name,head_url,info):
    sql = """
    insert into mz_lps_author
    (name,
    head_url,
    info)
    values
    (%s,%s,%s)
    """
    #
    # sql_get_author_id = """
    # select last_insert_id()
    # """
    #
    # sql_insert_course = """
    # update mz_lps_course set teacher=%s where id=%s
    # """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,(name,head_url,info))
            conn.commit()
            log.info("db execute :" + cursor._last_executed)

            # cursor.execute(sql_get_author_id)
            # last_id = cursor.fetchone().values[0]
            # log.info("db execute: " + cursor._last_executed)
            #
            # cursor.execute(sql_insert_course,(last_id,course_id))
            # conn.commit()
            # log.info("db execute :" + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def update_author(id,name,head_url,info):
    sql = """
    update mz_lps_author
    set name =%s,
    head_url=%s,
    info=%s
    where id=%s
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(sql,(name,head_url,info,id))
            conn.commit()
            log.info("db execute :" + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def get_author_by_id(id):
    sql = """
    select id,name,info,head_url from mz_lps_author where id=%s
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,id)
            result = cursor.fetchone()
            log.info("db execute :" + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def list_author(name,skip):

    sql_count = """
    select
    count(id)
    from
    mz_lps_author
    where name like %s or %s=''
    """

    sql = """
    select
    id,
    name,
    head_url,
    info
    from
    mz_lps_author
    where
    name like %s or %s=''
    limit %s,%s
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql_count, ("%" + name + "%", name))
            rowsCount = cursor.fetchone()

            cursor.execute(sql, (
            "%" + name + "%",
            name,
            skip["limit"],
            skip["offset"]
            ))
            print "*"*100
            print skip['limit']
            print skip['offset']

            info = cursor.fetchall()

        except Exception as e:
            raise e
            print e

        result = {
            "info":info,
            "rowsCount":rowsCount.values()[0],
        }

        return APIResult(result=result)

    return main()
