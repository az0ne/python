# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor


def list_user(user_name, real_name, skip):
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql_count = """
                        select count(*) as count from mz_server_admin
                        where (user_name like  %s or %s ='')
                        and (real_name like  %s or %s ='')
                        """

        sql = """
                select id,
                        user_name,
                        real_name,
                        remark,
                        is_delete,
                        case is_delete
                        when 0 then '正常'
                        else '禁用'
                        end as state

                from mz_server_admin
                where (user_name like  %s or %s ='')
                and (real_name like  %s or %s ='')
                limit %s,%s
                """

        try:

            cursor.execute(sql_count, ('%' + user_name + '%',
                                       user_name,
                                       '%' + real_name + '%',
                                       real_name,))
            rows_count = cursor.fetchone()

            log.info("db execute: " + cursor._last_executed)

            cursor.execute(sql, ('%' + user_name + '%',
                                 user_name,
                                 '%' + real_name + '%',
                                 real_name,
                                 skip["limit"], skip["offset"]))
            info = cursor.fetchall()

            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            "rows_count": rows_count["count"],
        }

        return APIResult(result=result_dict)

    return main()


def get_user_by_id(user_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select id,
                        user_name,
                        real_name,
                        password,
                        remark,
                        is_delete from mz_server_admin
                where id=%s
                """

        try:
            cursor.execute(sql, (user_id,))
            info = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=info)

    return main()


def get_user_by_name(user_name):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select id,
                        user_name,
                        real_name,
                        password,
                        remark,
                        is_delete from mz_server_admin
                where user_name=%s
                """

        try:
            cursor.execute(sql, (user_name,))
            info = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=info)

    return main()


def start(user_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_admin
                set is_delete = 0
                where id=%s
                """
        try:
            cursor.execute(sql, (user_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def stop(user_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_admin
                set is_delete = 1
                where id=%s
                """

        try:
            cursor.execute(sql, (user_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def add(user_name, real_name, password, remark):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                insert into mz_server_admin(user_name,
                            real_name,
                            password,
                            remark)
                values (%s,%s,%s, %s)
                """

        try:
            cursor.execute(sql, (user_name, real_name, password, remark,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def update(user_id, user_name, real_name, password, remark):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_admin set
                            real_name=%s,
                            password=%s,
                            remark=%s
                where id =%s and user_name=%s
                """

        try:
            cursor.execute(sql, (real_name, password, remark, user_id, user_name,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()
