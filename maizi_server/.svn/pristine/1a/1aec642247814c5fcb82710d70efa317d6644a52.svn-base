# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor

def list_assistant_can_use():

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                select id,
                        name,
                        phone,
                        qq,
                        is_delete
                from mz_server_assistant
                where is_delete = 0
                """

        try:
            cursor.execute(sql)
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
        }

        return APIResult(result=result_dict)

    return main()

def list_assistant():

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                select id,
                        name,
                        phone,
                        qq,
                        is_delete,
                        case is_delete
                        when 0 then '正常'
                        else '禁用'
                        end as state
                from mz_server_assistant
                """

        try:
            cursor.execute(sql)
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
        }

        return APIResult(result=result_dict)

    return main()

def get_assistant_by_id(assistant_id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select id,
                        name,
                        phone,
                        qq,
                        is_delete
                from mz_server_assistant
                where id=%s
                """

        try:
            cursor.execute(sql, (assistant_id,))
            info = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=info)

    return main()


def start(assistant_id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_assistant
                set is_delete = 0
                where id=%s
                """
        try:
            cursor.execute(sql, (assistant_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()

def stop(assistant_id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_assistant
                set is_delete = 1
                where id=%s
                """

        try:
            cursor.execute(sql, (assistant_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()

def add(name,phone,qq):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                insert into mz_server_assistant(name,
                            phone,
                            qq)
                values (%s,%s,%s)
                """

        try:
            cursor.execute(sql, (name, phone, qq,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()

def update(assistant_id,name,phone,qq):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_assistant set
                            name=%s,
                            phone=%s,
                            qq=%s
                where id =%s
                """

        try:
            cursor.execute(sql, ( name, phone, qq, assistant_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()