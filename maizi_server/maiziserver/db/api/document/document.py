# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor

def list_document(document_type,name):

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                select a.id,
                        a.name,
                        a.file_name,
                        a.type,
                        case a.type
                        when 0 then '教务'
                        when 1 then '教学'
                        when 2 then '销售'
                        when 3 then '运营'
                        end as type_name,
                        a.author,
                        a.extension
                from mz_server_inner_document as a
                where is_delete = 0
                and (a.type = %s or %s = '')
                and (a.name like %s or %s = '')
                """

        try:
            cursor.execute(sql, (document_type,
                                 document_type,
                                 '%' + name + '%',
                                 name))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        result_dict = {
            "result": info,
        }

        return APIResult(result=result_dict)

    return main()

def delete(id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_inner_document
                set is_delete = 0
                where id=%s
                """
        try:
            cursor.execute(sql, (career_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()

def add(name,file_name,author,uploader,type,extension):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                insert into mz_server_inner_document
                (name,
                 file_name,
                 author,
                 uploader,
                 type,
                 extension)
                values (%s,%s,%s,%s,%s,%s)
                """

        try:
            cursor.execute(sql, (name,file_name,author,uploader,type,extension,))
            conn.commit()
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()

def get_document_by_id(id):

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                select a.id,
                        a.name,
                        a.file_name,
                        a.type,
                        a.author,
                        a.extension
                from mz_server_inner_document as a
                where id = %s
                """

        try:
            cursor.execute(sql, (id,))
            info = cursor.fetchone()
        except Exception as e:
            raise e

        return APIResult(result=info)

    return main()
