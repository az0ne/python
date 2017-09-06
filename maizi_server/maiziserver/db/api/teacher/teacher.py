# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor

def list_teacher_can_use():

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                select id,
                        name,
                        phone,
                        qq,
                        is_delete
                from mz_server_teacher
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

def list_teacher():

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
                from mz_server_teacher
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

def get_teacher_by_id(teacher_id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select id,
                        name,
                        phone,
                        qq,
                        is_delete
                from mz_server_teacher
                where id=%s
                """

        try:
            cursor.execute(sql, (teacher_id,))
            info = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=info)

    return main()


def start(teacher_id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_teacher
                set is_delete = 0
                where id=%s
                """
        try:
            cursor.execute(sql, (teacher_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()

def stop(teacher_id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_teacher
                set is_delete = 1
                where id=%s
                """

        try:
            cursor.execute(sql, (teacher_id,))
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
                insert into mz_server_teacher(name,
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

def update(teacher_id,name,phone,qq):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_teacher set
                            name=%s,
                            phone=%s,
                            qq=%s
                where id =%s
                """

        try:
            cursor.execute(sql, ( name, phone, qq, teacher_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()