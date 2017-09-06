# -*- coding:utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor

def list_project(name,skip):
    sql = """
    select
    id,
    url,
    name
    from mz_lps_career_project
    where name like %s or %s=''
    limit %s,%s
    """

    sql_count = """
    select
    count(id)
    from mz_lps_career_project
    where name like %s or %s=''
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(
            sql, ("%"+name+"%", name,skip['limit'], skip['offset'])
            )
            infos = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)

            cursor.execute(sql_count, ("%"+name+"%",name))
            rowsCount = cursor.fetchone()
            log.info("db execute :" + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        result = {
        "info":infos,
        "rowsCount":rowsCount.values()[0]
        }

        return APIResult(result=result)

    return main()

def get_project(resource_id):

    sql = """
    select id,url,name from mz_lps_career_project where id=%s
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql, resource_id)
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def add_project(item_id,name,url):
    sql = """
    insert into mz_lps_career_project
    (name,url)
    values(%s,%s)
    """

    sql_last_insert_id = """
    select last_insert_id()
    """

    sql_update_item = """
    update mz_lps_item
    set resource_id =%s
    where id=%s
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(sql, (name, url))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)

            cursor.execute(sql_last_insert_id)
            lastInsertId = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
            lastInsertId = lastInsertId.values()[0]

            cursor.execute(sql_update_item,(lastInsertId, item_id))
            conn.commit()
            log.info("db execute:" + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def get_project_by_id(project_id):

    _sql = """
    select
    id,
    name,
    url
    from mz_lps_career_project
    where id=%s
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(_sql, project_id)
            result = cursor.fetchone()
            log.info("db execute :" + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def update_project(url,name,project_id):
    _sql = """
    update mz_lps_career_project
    set
    url=%s,
    name =%s
    where id=%s
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(_sql,(url, name, project_id))
            conn.commit()
            log.info("db execute :" + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()
