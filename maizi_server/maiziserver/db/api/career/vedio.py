# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor

# 操作vedio
def list_vedio(name,skip):
    sql = """
    select id,url,name from mz_lps_vedio
    where name like %s or %s=''
    limit %s,%s
    """

    sql_count = """
    select count(id) from
    mz_lps_vedio
    where name like %s or %s=''
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql_count,("%"+name+"%",name))
            rows_count = cursor.fetchone()

            cursor.execute(sql, ("%"+name+"name",name,skip['limit'],skip['offset']))
            vedios = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)

        except Exception as e:
            print e
            raise e

        result_dict = {
        "info":vedios,
        "rows_count":rows_count.values()[0]
        }

        return APIResult(result=result_dict)

    return main()

def page_vedio():
    sql = """
    select count(id) from mz_lps_vedio
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(sql)
            rowsCount = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e
        return APIResult(result=rowsCount)

    return main()

def get_vedio(resource_id):
    sql = """
    select id,url,name from mz_lps_vedio where id=%s
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,resource_id)
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def vedio_add(url,name,item_id):
    sql = """
    insert into mz_lps_vedio (url,name) values (%s,%s)"""

    sql_insert_item = """
    update mz_lps_item set resource_id=%s where id=%s
    """

    sql_last_resource_id = """select last_insert_id()"""

    @dec_make_conn_cursor
    def main(conn,cursor):

        try:
            cursor.execute(sql,(url,name))
            conn.commit()

            cursor.execute(sql_last_resource_id)
            result = cursor.fetchone()
            vedio_id = result.values()[0]

            cursor.execute(sql_insert_item,(vedio_id,item_id))
            conn.commit()
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def update_vedio(veido_id,name,url):
    sql = """
    update mz_lps_vedio set url=%s,name=%s where id=%s"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,(url,name,veido_id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()
