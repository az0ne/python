# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor

def list_book(name,skip):

    _sql = """
    select id,name,author,description,pic
    from mz_lps_career_book
    where name like %s or %s=''
    limit %s,%s
    """

    _sql_count = """
    select count(*) from mz_lps_career_book
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(_sql, ("%"+name+"%",name,skip['limit'],skip['offset']))
            infos = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)

            cursor.execute(_sql_count)
            rowsCount = cursor.fetchone().values()[0]
        except Exception as e:
            print e
            raise e

        result = {
            "books":infos,
            "rowsCount":rowsCount
        }


        return APIResult(result=result)

    return main()

def add_book(name,author,description,pic):

    _sql = """
    insert into mz_lps_career_book
    (name,author,description,pic)
    value(%s,%s,%s,%s)
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(_sql, (name, author, description, pic))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e


        return APIResult(code=True)

    return main()
